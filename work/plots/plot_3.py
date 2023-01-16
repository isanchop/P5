# Plot two wave files

import matplotlib.pyplot as plt
import numpy as np
import wave
from scipy.io import wavfile


fs, data = wavfile.read('work/waves/do_synth_1_2_3.wav')
# Open the wave files
spf = wave.open('work/waves/do_synth_1_2_3.wav', 'r')
spf2 = wave.open('work/waves/do_synth_1_4_6.wav', 'r')

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')

signal2 = spf2.readframes(-1)
signal2 = np.fromstring(signal2, 'Int16')

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(signal)
plt.show()

plt.figure(2)
plt.title('Signal Wave...')
plt.plot(signal2)
plt.show()

# Close the wave files
spf.close()
spf2.close()


