import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter, spectrogram

# Step 1: Load Noisy Audio
def load_audio(file_path):
    sample_rate, audio_data = wavfile.read(file_path)
    # Convert stereo to mono if necessary
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1).astype(audio_data.dtype)
    return sample_rate, audio_data

# Step 2: Analyze the Noise Spectrum
def plot_spectrum(audio_data, sample_rate):
    frequencies, times, Sxx = spectrogram(audio_data, sample_rate, nperseg=1024)
    plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
    plt.title("Spectrogram")
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")
    plt.colorbar(label="Intensity (dB)")
    plt.show()

# Step 3: Design a Filter
# Step 3: Design a High-Pass Filter (instead of band-stop)
def high_pass_filter(cutoff, sample_rate, order=4):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high')
    return b, a

# Apply the high-pass filter to the audio data
def apply_high_pass_filter(audio_data, cutoff, sample_rate):
    b, a = high_pass_filter(cutoff, sample_rate)
    return lfilter(b, a, audio_data)
# Step 4: Evaluate the Effectiveness
def compare_audio(original, processed, sample_rate):
    plt.figure(figsize=(10, 6))
    time = np.linspace(0, len(original) / sample_rate, num=len(original))
    plt.plot(time, original, label="Original Audio")
    plt.plot(time, processed, label="Processed Audio", alpha=0.7)
    plt.title("Audio Signal Comparison")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()

# Main Function
def main():
    # Load noisy audio file
    sample_rate, audio_data = load_audio(r"C:\Users\ABDO\Downloads\Telegram Desktop\noisy_audio2.wav")
    print(f"Sample Rate: {sample_rate} Hz")

    # Analyze noise spectrum
    print("Analyzing Noise Spectrum...")
    plot_spectrum(audio_data, sample_rate)

    # Apply a high-pass filter (remove low-frequency noise)
    cutoff = 100.0  # Example: remove frequencies below 100 Hz
    print(f"Applying High-Pass Filter ({cutoff} Hz)...")
    filtered_audio = apply_high_pass_filter(audio_data, cutoff, sample_rate)

    # Evaluate effectiveness
    print("Comparing Original and Processed Audio...")
    compare_audio(audio_data, filtered_audio, sample_rate)

    # Save the processed audio
    wavfile.write("processed_audio.wav", sample_rate, filtered_audio.astype(np.int16))
    print("Processed audio saved as 'processed_audio.wav'.")

if __name__ == "__main__":
    main()