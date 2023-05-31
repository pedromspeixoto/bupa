import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import io
from stftpitchshift import StftPitchShift
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile

# Define Constants
FILE_FORMAT = '.wav'

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

# Apply a reverb using pedalboard
def apply_reverb(input_file, target_sr=44100.0, room_size=0.5, damping=0.5, wet_level=0.33, dry_level=0.4, width=1.0, freeze_mode=0.0):
    # Read in a whole file, resampling to our desired sample rate:
    sample_rate = target_sr
    with AudioFile(input_file).resampled_to(sample_rate) as f:
        audio = f.read(f.frames)

    # Define pedalboard
    board = Pedalboard([
        Reverb(room_size=room_size,
            damping=damping,
            wet_level=wet_level,
            dry_level=dry_level,
            width=width,
            freeze_mode=freeze_mode),
    ])

    # Run the audio through the pedalboard
    effected = board(audio, sample_rate)

    # Write the audio back as a wav file
    output_file = io.BytesIO()
    with AudioFile(output_file, 'w', sample_rate, effected.shape[0], format=FILE_FORMAT) as f:
        f.write(effected)

    return output_file

def apply_default_voice(input_file):

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

def apply_god_robot_voice(input_file):
    # Load the audio file
    sample_rate, audio_data = wav.read(input_file)

    # Apply the highpass filter
    filtered_audio_data = highpass_filter(audio_data, sample_rate, 90, 18)

    # Declare the pitch shift object
    semitones = -6
    pitchshifter = StftPitchShift(1024, 256, sample_rate)
    pitch_shift_factor = 2 ** (semitones / 12)  # Shifting by -6 semitones
    shifted_audio_data = pitchshifter.shiftpitch(filtered_audio_data, pitch_shift_factor)

    # Apply the ring modulator
    ring_modulated_audio_data = ring_modulator(shifted_audio_data, sample_rate, 220, 0.22, 0.39)

    # Save the pitch shifted audio file
    effects_file = io.BytesIO()
    wav.write(effects_file, sample_rate, shifted_audio_data.astype(np.int16))

    # Apply the reverb
    reverb_file = apply_reverb(effects_file)

    # Read the contents of the WAV file
    reverb_file.seek(0)
    audio_file = reverb_file.read()

    return audio_file
