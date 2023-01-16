import scipy.io.wavfile as wavfile
import numpy as np
from scipy.fftpack import fft, fftshift
import seaborn as sns
import matplotlib.pyplot as plt

audios  =['work/waves/do_synth_1_2_3.wav','work/waves/do_synth_10_7_3.wav', 'work/waves/do_synth_3_4_6.wav']

for audio in audios:
    fs, data = wavfile.read(audio)

    # Apply FFT
    fft_out = np.fft.fft(data)

    # Calculate power spectrum
    power_spectrum = np.abs(fft_out)**2

    power_spectrum_db = 10 * np.log10(power_spectrum)
    n = len(data)
    freq = np.fft.fftfreq(n, 1/fs)
    sns.lineplot(x=freq[:n//2], y=power_spectrum_db[:n//2], label = audio.split('/')[-1])

plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dB)')
plt.grid(True)
plt.legend()
plt.title("Comparación FM spectrums")
plt.show()



