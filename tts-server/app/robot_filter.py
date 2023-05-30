import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import io
from stftpitchshift import StftPitchShift

def highpass_filter(input_signal, sample_rate, cutoff_frequency, attenuation):
    # Create the filter coefficients
    b, a = signal.cheby1(5, attenuation, cutoff_frequency, btype='highpass', fs=sample_rate)

    # Apply the filter to the input signal
    filtered_signal = signal.lfilter(b, a, input_signal)

    return filtered_signal

def ring_modulator(input_signal, sample_rate, frequency, rectify, mix):
    # Create the carrier signal
    t = np.arange(len(input_signal)) / sample_rate
    carrier_signal = np.sin(2 * np.pi * frequency * t)

    # Rectify the carrier signal
    if rectify > 0:
        carrier_signal = np.abs(carrier_signal)

    # Mix the carrier signal with the input signal
    output_signal = (1 - mix) * input_signal + mix * carrier_signal

    return output_signal

def apply_robot_voice(input_file):

    # Load the audio file
    sample_rate, audio_data = wav.read(input_file)

    # Apply the highpass filter
    filtered_audio_data = highpass_filter(audio_data, sample_rate, 90, 18)

    # Declare the pitch shift object
    semitones = 4
    pitchshifter = StftPitchShift(1024, 256, sample_rate)
    pitch_shift_factor = 2 ** (semitones / 12)  # Shifting by 4 semitones
    shifted_audio_data = pitchshifter.shiftpitch(filtered_audio_data, pitch_shift_factor)

    # Apply the ring modulator
    ring_modulated_audio_data = ring_modulator(shifted_audio_data, sample_rate, 112, 0.22, 0.39)

    # Save the pitch shifted audio file
    output_file = io.BytesIO()
    wav.write(output_file, sample_rate, shifted_audio_data.astype(np.int16))
    output_file.seek(0)

    # Read the contents of the WAV file
    audio_file = output_file.read()

    return audio_file