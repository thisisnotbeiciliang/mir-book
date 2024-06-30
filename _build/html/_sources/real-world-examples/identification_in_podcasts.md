# Identification in Podcasts

According to the definition by [BBC Sound](https://www.bbc.com/sounds/help/questions/getting-started-with-bbc-sounds/what-are-podcasts), a **podcast** is an edited piece of content which can be a complete radio programme, an edited extract or highlights from a programme, or completely unique content with a particular theme made to be subscribed and listened to as a series. 

Podcasts are growing exceptionally fast, and the production quality is constantly improving. Many podcasters use music. However, some may throw caution to the wind and just use music without licensing. In this context, music identification services can be helpful to protect the copyright holder by automatically spotting the song used in the podcasts. We proposed a system that utilizes our audio models together. A schematic overview is presented in the figure below.

```{figure} ../figures/rwe-iip-flowchart.png
---
width: 800px
align: center
name: rwe-iip-flowchart
---
Schematic overview of the proposed music identification system for podcasts.
```

The proposed system mainly consists of 3 steps:
- Step 1: given a podcast episode, [content type classification](../audio-models/music_classification.md) can highlight which parts contain music. Non-music parts can be removed in order to increase the efficiency of music identification in the following steps. 
- Step 2: using the music clips obtained from Step 1, [audio fingerprinting](../audio-models/music_identification.md) can look up our fingerprint database and identify the particular music recording that is the source of the clip.
- Step 3: the remaining unidentified clips will be examined using [version identification](../audio-models/music_identification.md).

Let's take an episode from [NPR's Tiny Desk Concerts](https://www.npr.org/podcasts/510306/tiny-desk-concerts-audio) as an example! We choose [this one featuring Anderson .Paak and the Free Nationals](https://www.npr.org/2016/08/12/489769830/anderson-paak-the-free-nationals-tiny-desk-concert), who performed 4 songs including _Come Down_, _Heart Don't Stand A Chance_, _Put Me Thru_ and _Suede_. The corresponding video can be seen on [YouTube](https://www.youtube.com/watch?v=ferZnZ0_rSM), where presents an incorrect "music in this video" claimed by one of YouTube’s copyright management tools, like Content ID.

Step 1 returns non-music vs. music results as shown in {numref}`rwe-iip-step1`. The non-music parts correspond to small chats between songs. By removing these non-music parts, we can obtain 4 music clips from time positions 0-177, 225-408, 456-642, and 720-906 seconds, respectively.

```{figure} ../figures/rwe-iip-step1.png
---
width: 800px
align: center
name: rwe-iip-step1
---
Non-music vs. music results obtained from Step 1.
```

By running audio fingerprinting on the 4 music clips stored as waveform files, we can get results from Step 2 as follows:

```
==> Query: paak_npr_0-177.wav
  - no match
==> Query: paak_npr_225-408.wav
  - no match
==> Query: paak_npr_456-642.wav
  - no match
==> Query: paak_npr_720-906.wav
  - no match
```

Our database contains fingerprints of the official-released version of the 4 songs. The “no match” results show that audio fingerprinting is highly sensitive to identify a particular version of a piece of music. These 4 songs played at the NPR Tiny Desk Concert are live versions of the official ones. Therefore version identification is required to identify the 4 music clips. 

The following results from Step 3 present the distance between embeddings of each music clip and 4 official-released songs stored as mp3 files.

```
==> Distance of paak_npr_0-177.wav vs. 4 official mp3s
  * 0.3995 vs. paak_come_down.mp3
  - 0.8798 vs. paak_heart_dont_stand_a_chance.mp3
  - 0.6774 vs. paak_put_me_thru.mp3
  - 0.7150 vs. paak_suede.mp3
==> Distance of paak_npr_225-408.wav vs. 4 official mp3s
  - 0.8573 vs. paak_come_down.mp3
  * 0.4444 vs. paak_heart_dont_stand_a_chance.mp3
  - 0.8746 vs. paak_put_me_thru.mp3
  - 0.7780 vs. paak_suede.mp3
==> Distance of paak_npr_456-642.wav vs. 4 official mp3s
  - 0.6188 vs. paak_come_down.mp3
  - 0.8092 vs. paak_heart_dont_stand_a_chance.mp3
  * 0.2486 vs. paak_put_me_thru.mp3
  - 0.5723 vs. paak_suede.mp3
==> Distance of paak_npr_720-906.wav vs. 4 official mp3s
  - 0.5981 vs. paak_come_down.mp3
  - 0.7284 vs. paak_heart_dont_stand_a_chance.mp3
  - 0.6291 vs. paak_put_me_thru.mp3
  * 0.4045 vs. paak_suede.mp3
```

Star symbol (`*`) indicates the distance is less than 0.45, which implies a high similarity. Since no other songs in our database obtain such degree of similarity, we conclude that the 4 music clips are identified as:
- 00:00-02:57 clip (paak_npr_0-177.wav) is [_Come Down_](https://www.youtube.com/watch?v=-OqrcUvrbRY) (`paak_come_down.mp3`).
- 03:45-06:48 clip (paak_npr_225-408.wav) is [_Heart Don't Stand A Chance_](https://www.youtube.com/watch?v=O5mcLhuUfG0) (`paak_heart_dont_stand_a_chance.mp3`).
- 07:36-10:42 clip (paak_npr_456-642.wav) is [_Put Me Thru_](https://www.youtube.com/watch?v=pK2-XuLByuQ) (`paak_put_me_thru.mp3`).
- 12:00-15:06 clip (paak_npr_720-906.wav) is [_Suede_](https://www.youtube.com/watch?v=zNTNbNtft9g) (`paak_suede.mp3`).

{numref}`rwe-iip-step3` annotates the distance results from version identification by superimposing to {numref}`rwe-iip-step1`.

```{figure} ../figures/rwe-iip-step3.png
---
width: 800px
align: center
name: rwe-iip-step3
---
Distance results from version identification.
```