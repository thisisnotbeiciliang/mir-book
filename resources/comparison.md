# Technology Comparison

There are a range of content identification technologies as shown in the table below, where "effectiveness" refers to "how much of the targeted content can be matched".

::::{tab-set}
:::{tab-item} File Name
Matches words contained in file name
- Effectiveness: <5%
- Estimated cost per file: <0.001€
- Comment: High false negative and false positive rates.
:::

:::{tab-item} File Hash
Matches file bits exactly
- Effectiveness: <10%
- Estimated cost per file: <0.0001€
- Comment: Not a good filter unless paired with other technologies.
:::

:::{tab-item} Watermark
Matches embedded mark either visual or audible
- Effectiveness: <10%
- Estimated cost per file: <0.01-.05€
- Comment: Good for identifying premium content. Little content is watermarked.
:::

:::{tab-item} Fingerprint
Matches perceptual characteristics compared to original
- Effectiveness: 80-99%
- Estimated cost per file: <0.005-.05€
- Comment: Standard today for production. Range of accuracy among technologies.
:::

:::{tab-item} Human Review
Manual review
- Effectiveness: <50%
- Estimated cost per file: >1€
- Comment: Not practical for large-scaled identification process. Good for counter-notice.
:::
::::

**Existing services in the market for content-based music identification are based on [audio fingerprinting](../audio-models/music_identification.md)**. They can identify unknown audio by matching the fingerprints of unknown content to known fingerprints registered in the reference database. Although robust to many kinds of signal distortions, audio fingerprinting is not designed for detecting composition similarities between music tracks. Therefore, it fails to identify the underlying original music from derivative versions, which may differ from the original recording in many ways, possibly including significant changes in timbre, instrumentation, tempo, key, harmony, melody, lyrics, and musical structure. 

Audio fingerprinting from companies such as [Audible Magic](https://www.audiblemagic.com/), [Soundmouse](https://app.soundmouse.com/), [TuneSat](https://tunesat.com/tunesatportal/home), [BMAT](https://www.bmat.com/) and [Kobalt](https://www.kobaltmusic.com/) have been in use for many years throughout the world to identify music that is broadcast on radio and television, or played in public venues. The technology is essential for the accurate logging of songs used to properly compensate the musicians.

**To identify derivative works, music representations beyond audio fingerprints and robust to the main musical changes are required.** _Content ID_ developed by Google/Youtube and _ByteCover_ {cite}`du2021bytecover` proposed by ByteDance AI Lab have been used for industry-scaled cover song identification (CSI). However, they are kept in-house for taking down videos with potential copyright infringement.

**There is no existing service that directly empowers music creators with intellectual property rights (IPR) protection using statistically informed similarity algorithms for all types of derivative works.** This motivates us to develop multi-hierarchical embeddings to represent audio content in multiple musical dimensions. Such embeddings can also be used in recommendation systems to explore similar songs within the same embedding cluster. 

Since we can output song-level embeddings that are fixed-length vectors where the length is unrelated to the original music track, the similarity between embeddings can be directly measured by Euclidean or Cosine distance, and therefore **the embeddings can be efficiently indexed and retrieved using existing nearest-neighbour search libraries such as [FAISS](https://faiss.ai/), suitable for a large dataset**. This is not possible in systems where the similarity estimation between two songs is performed using a local alignment algorithm (e.g., a CSI system using _2DFTM_ {cite}`seetharaman2017cover` patented in [US20180189390A1](https://patents.google.com/patent/US20180189390A1/en?oq=US20180189390) by [Gracenote](https://www.gracenote.com/auto/music-recognition-auto/)).