# Music Classification

Music classification is a MIR task whose objective is the computational understanding of music semantics. For a given song, the classifier predicts relevant musical attributes. Based on the task definition, there are a nearly infinite number of classification tasks – from genres, moods, and instruments to broader concepts including music similarity and musical preferences. The retrieved information can be further utilized in many applications including music recommendation, curation, playlist generation, and semantic search.

Here I present two tasks: content type classification and genre classification.

## Content Type Classification

Audio contents can consist of various signals, such as music, speech, and sound effects. Given an audio document, automatically segmenting and labelling it to indicate where music is present can be helpful for fast and robust music identification.

I trained a Convolutional Neural Network (CNN) that categorises every 3 seconds of the input audio into 6 content types, including:
- `speech`: speech only;
- `speech_acc`: speech with music accompaniment;
- `vocal`: vocal music without accompaniment, such as solo and choir performances;
- `vocal_acc`: vocal music with accompaniment;
- `instrumental`: music instruments only, no human voice at all;
- `other`: not music, can be sound effects, noises, etc.

In the preprocessing stage, Mel-scaled Log Spectrogram is calculated to represent the raw audio. It is then fed into our trained CNN to obtain fragment-level results (3 seconds as a fragment). By concatenating these results, we can obtain a 2 dimensional matrix that represents the content-type results of the input audio over time. One dimension is indexed by time, another is indexed by 6 content types, and values in the matrix represent the detection probability at that particular time and content type. 

Here I use the first 3-minute audio in the [Anderson .Paak & The Free Nationals: NPR Music Tiny Desk Concert](https://www.youtube.com/watch?v=ferZnZ0_rSM) as an example to illustrate the CNN output. The 2D matrix can be plotted as shown in the figure below.

```{figure} ../figures/am-ctd-6types.png
---
width: 600px
align: center
name: types
---
Content-type classification probability over time of the first 3-minute audio in the example video. Brighter colors indicate higher probability than darker colors.
```

{numref}`types` indicates that content type in 0:00-0:09 is speech, 0:09-0:33 is instrumental, 0:33-2:36 is speech with music accompaniment, 2:36-2:57 is instrumental, and 2:57-3:03 is other. These results correspond to the actual content types in the video. Since the song _Come Down_ performed here is more hip-hop style, it's detected as `speech_acc` instead of `vocal_acc`.

Based on the above matrix, we can further process it to obtain `music` vs. `no_music` fragments as shown in {numref}`musicsegs`. We can conclude that, in the first 3 minutes of the video, music is present from 0:09 to 2:57.

```{figure} ../figures/am-ctd-musicsegs.png
---
width: 600px
align: center
name: musicsegs
---
Presence of music over time of the first 3-minute audio in the example video.
```

## Genre Classification

Another CNN is trained to categorise every 3 seconds of the input audio into 10 genres, including: rock, pop, classical, rap/hip-hop, country, folk, metal, electronic, rhythm music (such as blues, R&B, etc.), and world/other music.

Using the audio in the [official video of _Come Down_](https://www.youtube.com/watch?v=-OqrcUvrbRY) by Anderson .Paak as an example, the genre classifier can return a 2D matrix presenting the 10 genre values over time. This matrix can be plotted as shown in the figure below.

```{figure} ../figures/am-gc-10genres.png
---
width: 600px
align: center
name: genres
---
Genre classification probability over time of the song Come Down by Anderson .Paak. Brighter colors indicate higher probability than darker colors.
```

If we take the average probability of each genre over time, the top-3 results are: rap (0.5640), rhythm (0.2983) and pop (0.1426).
