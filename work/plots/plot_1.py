# This will be a script that will plot the data from a wave file given the file name as an argument

import matplotlib.pyplot as plt
import sys
import numpy as np
import wave

# Get the file name
fileName = sys.argv[1]

# Open the wave file
waveFile = wave.open(fileName, 'r')

# Get the number of frames
numFrames = waveFile.getnframes()

# Get the sample rate
sampleRate = waveFile.getframerate()

# Get the number of channels
numChannels = waveFile.getnchannels()

# Get the sample width
sampleWidth = waveFile.getsampwidth()

# Get the number of bytes per frame
bytesPerFrame = numChannels * sampleWidth

# Get the number of bytes per second
bytesPerSecond = bytesPerFrame * sampleRate

# Get the number of seconds
numSeconds = numFrames / sampleRate

# Get the number of bytes
numBytes = numFrames * bytesPerFrame

# Get the data
data = waveFile.readframes(numFrames)

# Close the wave file
waveFile.close()

# Convert the data to a numpy array
data = np.frombuffer(data, dtype=np.int16)

# Get the number of samples
numSamples = len(data)

# Ask for the title of the plot
title = input("Enter the title of the plot: ")

# Plot the data with levels on the y-axis (Amplitude) and time on the x-axis (in seconds)
plt.plot(data)

# Set the x-axis label
plt.xlabel("Samples")

# Set the y-axis label
plt.ylabel("Amplitude")

# Set the title of the plot
plt.title(title)

# Show the plot
plt.show()

# Close the plot
plt.close()

# End of file
