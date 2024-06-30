# Music Identification

Since 2000, there have been multiple services that help users identify the audio recording and deliver suitable content information. A typical scenario is that a user, also called the client, records a short audio fragment of the unknown song using a smartphone. The audio fragment is then converted into so-called **audio fingerprints**, which are compact and descriptive audio features. These fingerprints are transmitted to the identification service, also called the server. The server hosts various data resources including a fingerprint database that covers all music recordings to be identified, as well as a metadata database that contains content information linked to these recordings. The server receives the query fingerprints sent by the client and compares them with the fingerprints contained in the database. This step is typically realized by an efficient database look-up supported by suitable index structures. In the case of a successful identification, the server retrieves the content information linked to the identified fingerprints and sends back the desired metadata to the client. The following figure presents a schematic overview of the underlying client–server model {cite}`Mueller15_FMP_SPRINGER`.

```{figure} ../figures/am-af-flowchart.png
---
width: 600px
align: center
name: am-af-flowchart
---
Schematic overview of the client–server model of the described music identification service.
```

There are various ways to design and compute fingerprints. In real-world applications, these fingerprints need to fulfil certain requirements including high specificity (to distinguish an audio fragment from millions of others), robustness (against background noise and signal distortions), compactness (to be easily transmitted, stored, and indexed), and scalability (for millions of recordings).

## Peak-based Fingerprints

Audio fingerprint based on the concept of spectral peaks consists of a sparse set of characteristic points in the time–frequency plane. Such peaks often remain unchanged even in the presence of noise and additional sound sources. This peak-based fingerprint, which was introduced by Avery Wang {cite}`Wang03_Shazam_ISMIR`, is now successfully used in commercial audio identification systems. 

```{figure} ../figures/am-af-constellation.png
---
width: 600px
align: center
name: am-af-constellation
---
Illustration of the identification system using peak-based fingerprints.
```

{numref}`am-af-constellation` illustrates the basic retrieval concept of the identification system using peak-based fingerprints. The extracted peaks are superimposed to the STFT spectrograms for an example database document (30 seconds of the recording) and a query fragment (10 seconds), as seen in (a) and (b), respectively. The peak-picking step reduces the complex spectrogram to a “constellation map”, a low-dimensional sparse representation of the original signal by means of a small set of time-frequency points, see (c) and (d). Finally, for the database look-up, the constellation map for a query fragment is locally compared to the one for all database fragments of the same size by counting peaks that occur in both constellation maps. This procedure is illustrated in (e) showing the superposition of the database fingerprints and time-shifted query fingerprints. Both constellation maps show a high consistency at a fragment of the database document starting at time position 10 seconds, which indicates a hit. 

In the matching processes described above, the query needs to be compared against all sections of all documents contained in the database. Obviously, such an exhaustive search strategy is not feasible for large databases containing millions of recordings. To facilitate fast information access without sacrificing the accuracy of the retrieval results, indexing technique is typically used. It optimises speed and performance by cutting down the search space through suitable look-up operations. In our fingerprinting context, peak pairs are considered as hashes to construct index. Pairs are formed of the anchor and each peak in the target zone, and a hash value is obtained for each pair of peaks as a combination of both frequency values and the time difference between the peaks as indicated in {numref}`am-af-hash`. We do not further describe the indexing steps here. For details, we refer to Section 7.1.3 of {cite}`Mueller15_FMP_SPRINGER` and {cite}`Wang03_Shazam_ISMIR`.

```{figure} ../figures/am-af-hash.png
---
width: 600px
align: center
name: am-af-hash
---
Illustration of the peak pairing strategy.
```

## Embedding-based Fingerprints

Google proposed _Now Playing_ {cite}`gfeller2017now`, a music recognizer using a pre-trained neural network which generates compact and discriminative fingerprints at a rate of one 96 dimensional embedding per second. Since each embedding is a fix-length vector, existing similarity search libraries can be used in the matching process. This improves both the computational speed of the audio fingerprints as well as reduce their size while maintaining the accuracy.


## Beyond Fingerprints for Version Identification

Although robust to many kinds of signal distortions, the discussed fingerprints are designed to be highly sensitive to a particular version of a piece of music. They are not designed for handling temporal or melodic deformations. This means if the query is another version, such as cover songs and instrumental recordings, audio fingerprinting will fail to identify the underlying music. Therefore, one needs other techniques to identify different versions of a given recording to protect copyrights of not only the actual sound recording, but also the musical composition.

Given a music recording of a musical piece, version identification aims at automatically retrieving all recorded versions (cover songs, instrumental, remixes, etc.) of the same piece from a music collection. Here, the query typically consists of an entire recording, as opposed to audio fingerprinting, where the query is only a small audio fragment. Therefore, version identification is usually considered **a song-level retrieval task**, where a single similarity measure is used to globally compare entire songs.

The basic assumption in version identification is that the original and a derivative version of a piece of music typically share some common characteristics. However, due to possible structural differences between these versions, it is not clear where these common elements occur. In view of the many possible kinds of modifications that may be applied when creating new versions, it is not realistic to assume that one can deal with all the resulting variations by using a single technique. **We focus on the scenario where the versions to be identified share a similar melodic or harmonic progression.** On the other side, we allow differences in aspects such as tempo, instrumentation, timbre, and the overall musical structure. 

In our system, we can represent an audio recording as a neural network embedding, which is able to capture tonal elements of music recordings while showing a high degree of invariance with regard to a wide range of modifications. Given a music recording of arbitrary length as the input query, fixed-length embedding is obtained and used for similarity measurement as follows:

- First, the input audio recording is processed into a time-frequency representation $|X(t, f)|$.
- Second, $|X(t, f)|$ is fed into the trained neural network to obtain audio embedding, which is an array with fixed length $e \in \mathbb{R}^{L}$.
- Third, a distance matrix (or similarity matrix) is computed by comparing $e \in \mathbb{R}^{L}$ to the embedding database in a pairwise fashion. Here we use cosine distance for measurement.
- Finally, given the distance scores between the query and every song in the database, candidates of versions are decided using a threshold. The smaller the distance, the greater the degree of similarity. Therefore any songs with a distance smaller than the threshold are considered as identified versions.

Compared to alignment-based systems used in cover song identification tasks, such as _Qmax_ proposed in {cite}`Serr_2009`, embedding-based system can remarkably improve computation efficiency without sacrificing the accuracy, thus feasible for large databases. For example, this system can achieve a mean average precision (MAP) of 0.88 on the [_cover80_](https://labrosa.ee.columbia.edu/projects/coversongs/covers80/) dataset, and the runtime is at least 10 times faster than _Qmax_. For a more detailed investigation, we refer to {cite}`yesiler2021investigating`.
