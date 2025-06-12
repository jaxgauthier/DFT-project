import sounddevice as sd
import numpy as np
import time

print("Testing audio system...")

# Print audio device information
print("\nAvailable audio devices:")
print(sd.query_devices())

# Generate a simple test tone
duration = 1.0  # seconds
frequency = 440  # Hz (A4 note)
sample_rate = 44100  # Hz
t = np.linspace(0, duration, int(sample_rate * duration), False)
test_tone = 0.5 * np.sin(2 * np.pi * frequency * t)

print("\nPlaying test tone...")
try:
    sd.play(test_tone, sample_rate)
    sd.wait()
    print("Test tone played successfully!")
except Exception as e:
    print(f"Error playing test tone: {e}")

print("\nTest complete!") 