# This will be a script that will plot the data from a wave file given the file name as an argument

import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.io import wavfile

# Get the file name
fileName = sys.argv[1]

# Open the wave file
fs, data = wavfile.read(fileName)


# Get the number of samples
numSamples = len(data)

# Apply FFT
fft_out = np.fft.fft(data)

# Calculate power spectrum
power_spectrum = np.abs(fft_out)**2

power_spectrum_db = 10 * np.log10(power_spectrum)
n = len(data)
freq = np.fft.fftfreq(n, 1/fs)

# Ask for the title of the plot
title = input("Enter the title of the plot: ")

fig, (ax1, ax2) = plt.subplots(2, 1)

# Plot the data with levels on the y-axis (Amplitude) and time on the x-axis (in seconds)
ax1.plot(data)

# Plot the fourier transform on a separate plot
ax2.semilogx(freq[:n//2], power_spectrum_db[:n//2])

# Set the x-axis label
ax1.set_xlabel("Samples")

# Set the y-axis label
ax1.set_ylabel("Amplitude")

# Set the title of the plot
ax1.set_title(title)

# Set the x-axis label
ax2.set_xlabel("frequency")

# Set the y-axis label
ax2.set_ylabel("Amplitude")

# Set the title of the plot
ax2.set_title("")

# Show the plot
plt.show()

# Close the plot
plt.close()

# End of file
