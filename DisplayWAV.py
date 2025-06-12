import wave
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.widgets import Button

def read_wav_file(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        # Get the wave file's parameters
        params = wav_file.getparams()
        sample_rate = wav_file.getframerate()
        num_channels = wav_file.getnchannels()
        frames = wav_file.readframes(params.nframes)
        
        # Convert to numpy array and normalize to voltage (-1 to 1 range)
        data = np.frombuffer(frames, dtype=np.int16)
        
        # If stereo, take average of channels
        if num_channels == 2:
            data = data.reshape(-1, 2)
            data = data.mean(axis=1)
        
        # Convert to float and normalize to -1 to 1 range (typical voltage range)
        normalized_data = data.astype(np.float32) / 32768.0
        return normalized_data, sample_rate, num_channels

def play_audio(file_path):
    """Play the audio file using system default player"""
    try:
        print(f"Attempting to play audio file: {file_path}")
        if sys.platform == 'darwin':  # macOS
            os.system(f'afplay "{file_path}"')
        elif sys.platform == 'win32':  # Windows
            os.system(f'start wmplayer "{file_path}"')
        else:  # Linux
            os.system(f'aplay "{file_path}"')
        print("Audio playback command sent successfully")
    except Exception as e:
        print(f"Error during audio playback: {str(e)}")
        import traceback
        traceback.print_exc()

class AudioPlayer:
    def __init__(self, file_path, fig):
        self.file_path = file_path
        self.fig = fig
        self.is_playing = False
        
    def play(self, event=None):
        print("Play button clicked!")
        if not self.is_playing:
            self.is_playing = True
            play_audio(self.file_path)
            self.is_playing = False
    
    def on_key(self, event):
        if event.key == ' ':  # Spacebar
            print("Spacebar pressed - playing audio")
            self.play()

def plot_voltage_samples(data, sample_rate, num_channels, file_path):
    """
    Plot voltage samples over time for the entire file with playback button
    """
    # Create figure with extra space at bottom for button
    fig = plt.figure(figsize=(15, 7))
    
    # Create main plot area
    ax = fig.add_axes([0.1, 0.2, 0.8, 0.7])  # [left, bottom, width, height]
    
    # Calculate total duration and create time axis
    total_duration = len(data) / sample_rate
    time = np.linspace(0, total_duration, len(data))
    
    # Plot the voltage data
    ax.plot(time, data, 'b-', linewidth=0.5, alpha=0.7)
    
    # Add grid and labels
    ax.grid(True, alpha=0.3)
    ax.set_ylabel('Voltage (normalized)')
    ax.set_xlabel('Time (seconds)')
    ax.set_title(f'Audio Waveform: {os.path.basename(file_path)}')
    
    # Set y-axis limits to show full voltage range
    ax.set_ylim(-1.1, 1.1)
    
    # Add text box with file information
    info_text = (f'Sample Rate: {sample_rate} Hz\nDuration: {total_duration:.2f}s\n'
                f'Channels: {num_channels}\nSamples: {len(data)}\n'
                f'Press spacebar or click button to play')
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Create button axes and button
    button_ax = fig.add_axes([0.4, 0.05, 0.2, 0.075])  # [left, bottom, width, height]
    player = AudioPlayer(file_path, fig)
    
    # Create button with custom style
    button = Button(button_ax, 'Play Audio (Spacebar)', 
                   color='lightblue', hovercolor='skyblue')
    button.on_clicked(player.play)
    
    # Add keyboard event handler
    fig.canvas.mpl_connect('key_press_event', player.on_key)
    
    # Keep a reference to prevent garbage collection
    fig.player = player
    
    return fig, ax

def main(input_file=None):
    try:
        # If no input file specified, use default
        if input_file is None:
            input_file = os.path.join('InputWAVS', 'Input2.wav')
        
        # Verify the file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Could not find the input file at: {input_file}")
            
        # Read the audio file
        data, sample_rate, num_channels = read_wav_file(input_file)
        
        print(f"File loaded successfully: {input_file}")
        print(f"Data shape: {data.shape}")
        print(f"Sample rate: {sample_rate}")
        print(f"Number of channels: {num_channels}")
        print("\nTip: You can play audio by clicking the button or pressing spacebar")
        
        # Plot voltage samples with playback button
        fig, ax = plot_voltage_samples(data, sample_rate, num_channels, input_file)
        plt.show()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

