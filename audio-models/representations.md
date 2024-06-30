# Representing Audio

Representing audio is an essential preprocessing step, the parameters of which can have an impact on the performance of content-based retrieval. We’ll first start talking about waveforms, arguably the most fundamental representation of audio, then we’ll move onto some common time-frequency representations. 

## Waveforms

```{figure} ../figures/am-ra-richter.gif
---
width: 600px
align: center
name: waveform-gif
---
A waveform shown at many different time scales. Each value is sampled at a uniform rate and quantized. Image by <a href="https://jvbalen.github.io/notes/waveform.html">Jan Van Balen</a>.
```

A _waveform_ is shorthand for a digitized audio signal, which is most similar to what the sound is like physically. For an acoustic sound, the air pressure of over time changes, and is recorded by a microphone, which converts the changes in air pressure to an electrical signal. The voltage of this signal is sampled at a regular time interval, quantized, and converted to a digital array in a computer. This digital array is what we call the waveform. Of course, this description glosses over a lot of details in the realm of physics, acoustics, and signal processing. What's important to know is that a continuous-time signal is discretized in both time and amplitude. We say a signal is monophonic, or mono, if there is only one audio channel, i.e., this array has shape $x \in \mathbb{R}^{t \times 1}$. We say a signal is stereophonic, or stereo, if the array has two channels, i.e., this array has shape $x \in \mathbb{R}^{t \times 2}$.

An important aspect of the waveform is the sample rate, which describes how many measurements, or samples, happen per second and is measured in Hertz, or Hz. For a signal with sample rate $sr$, the maximum frequency that can be reliably represented is $f_N=\frac{sr}{2}$, which is called the [Nyquist frequency](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem). For example, if a signal has a sample rate of 44.1 kHz, the highest possible frequency is 22.05 kHz.

Many retrieval systems would reduce the sample rate of their input signals (called downsampling) to reduce the computational load. Downsampling removes high frequency information from a signal. For example, if a system expects a signal at 16 kHz, then all input audio should be resampled to 16 kHz before using it.

## Time-Frequency (TF) Representations

```{figure} ../figures/am-ra-tf.png
---
width: 600px
align: center
name: tf-repr
---
A time-frequency representation. One dimension is indexed by time, another is indexed by frequency, and values in the matrix represent the energy of the sound at that particular time and frequency.
```

A Time-Frequency {cite}`smith2011spectral` representation is a 2 dimensional matrix that represents the frequency contents of an audio signal over time. There are many types of time-frequency representations out in the world, but we will only discuss those that are most frequently used for music recognition here.

We call a specific entry in this matrix a TF bin. We can visualize a TF Representation using a heatmap, which has time along the x-axis and frequency along the y-axis. Each TF bin in the heatmap represents the amplitude of the signal at that particular time and frequency. Some heatmaps have a colorbar alongside them that shows which colors indicate high amplitude values and which colors indicate low amplitude values. If there is no color bar, it is usually safe to assume that brighter colors indicate higher amplitudes than darker colors.

**Below we will outline some of the most popular and fundamental time-frequency representations.**

### Short-time Fourier Transform (STFT)

```{figure} ../figures/am-ra-stft.png
---
width: 600px
align: center
name: stft
---
The process of computing a short-time Fourier transform of a waveform. Imaged by <a href="https://bryan-pardo.github.io/">Bryan Pardo</a>.
```

Many of the time-frequency representations start out as a Short-time Fourier Transform or STFT. An STFT is calculated from a waveform representation by computing a [discrete Fourier transform](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) (DFT) of a small, moving window across the duration of the window. The location of each entry in an STFT determines its time (x-axis) and frequency (y-axis). The absolute value of a TF bin $|X(t, f)|$ at time $t$ and frequency $f$ determines the amount of energy heard from frequency $f$ at time $t$.

Each bin in our STFT is _complex_, meaning each entry contains both a magnitude component and a phase component. Both components are needed to convert an STFT matrix back to a waveform. This invertable process is called the inverse Short-time Fourier Transform or iSTFT.

Here are some important parameters to consider when computing an STFT:
- window type, which determines the shape of the short-time window that will segment the audio into short segments before applying the DFT. The shape of this window will affect which frequencies get emphasized or attenuated in the DFT.
- window length, which determines how many samples are included in each short-time window. Due to how the DFT is computed, this parameter also determines the resolution of the frequency axis of the STFT. The longer the window, the higher the frequency resolution and vice versa.
- hop length, which determines the distance, in samples, between any two adjacent short-time windows. 

### Magnitude, Power, and Log Spectrograms

```{figure} ../figures/am-ra-specs.png
---
width: 600px
align: center
name: specs
---
A visual comparison of the four types of spectrograms discussed in this section. Each has a different scaling function applied to the loudness, which is reflected in the colors of the heatmap plots.
```

The term "spectrogram" is mostly used to describe a TF Representation that does not explicitly represent phase in each TF bin. A visualization of four types of spectrograms is shown in {numref}`specs`. 

**Magnitude Spectrogram** 
For a complex-valued STFT, $X \in \mathbb{C}^{T \times F}$, the Magnitude Spectrogram is calculated by taking the absolute value of each element in the STFT, $|X| \in \mathbb{R}^{T \times F}$. 

**Power Spectrogram**
For a complex-valued STFT, $X \in \mathbb{C}^{T \times F}$, the Power Spectrogram is calculated by squaring  each element in the STFT, $|X|^2 \in \mathbb{R}^{T \times F}$.

**Log Spectrogram**
Human hearing is logarithmic with regards to amplitude. For a complex-valued STFT, $X \in \mathbb{C}^{T \times F}$, the Log Spectrogram is calculated taking the log of the absolute value of each element in the STFT, $\log{|X|} \in \mathbb{R}^{T \times F}$.

**Log Power Spectrogram**
For a complex-valued STFT, $X \in \mathbb{C}^{T \times F}$, the Log Spectrogram is calculated taking the log of the square of each element in the STFT, $\log{|X|^2} \in \mathbb{R}^{T \times F}$.

### Mel-spaced Spectrograms

```{figure} ../figures/am-ra-melspecs.png
---
width: 600px
align: center
name: melspecs
---
A visual comparison of linear-scaled vs mel-spaced y axies. Lower frequencies have a larger representation in a mel-spaced spectrogram.
```

Human hearing is also logarithmic with regards to frequencies. The [Mel scale](https://en.wikipedia.org/wiki/Mel_scale) approximates this property and is a quick way to make the frequency axis of a spectrogram quasi-logarithmic. This is also commonly used to reduce the computational load, because the number of Mel-spaced frequency bins is often lower than the number of linear-scaled frequency bins.

A visual comparison is shown in {numref}`melspecs`. Notice the how the y-axis in the Mel-spaced spectrogram is quasi-logarithmic, squishing higher frequencies and leaving more space for lower frequencies.

## Other Representations

A few other representations have been explored in the literature, such as Constant-Q Transform (CQT) {cite}`brown1991calculation,brown1992efficient`, 2-Dimensional Fourier Transform (2DFT) {cite}`seetharaman2017music`, and so on. 

Content-based retrieval systems commonly operate on TF representations. Even still, determining which spectrogram works best depends on the actual application scenarios and should be evaluated across different datasets. In the following sections, different TF representations are used in our audio models.
