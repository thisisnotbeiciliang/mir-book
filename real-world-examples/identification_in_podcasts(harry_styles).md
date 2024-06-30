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
- Step 1: given a podcast episode, [content type detection](../audio-models/content_type_detection.md) can highlight which parts contain music. Non-music parts can be removed in order to increase the efficiency of music identification in the following steps. 
- Step 2: using the music clips obtained from Step 1, [audio fingerprinting](../audio-models/audio_fingerprinting.md) can look up our fingerprint database and identify the particular music recording that is the source of the clip.
- Step 3: the remaining unidentified clips will be examined using [version identification](../audio-models/version_identification.md).

Let's take an episode from [NPR's Tiny Desk Concerts](https://www.npr.org/podcasts/510306/tiny-desk-concerts-audio) as an example! We choose [this one](https://www.npr.org/2020/03/16/815556266/harry-styles-tiny-desk-concert) featuring Harry Styles, who performed 4 songs including _Cherry_, _Watermelon Sugar_, _To Be So Lonely_ and _Adore You_. The corresponding video can be seen on [YouTube](https://www.youtube.com/watch?v=jIIuzB11dsA), where shows only one song in "music in this video" claimed by one of YouTube’s copyright management tools, like Content ID.

Step 1 returns non-music vs. music results as shown in {numref}`rwe-iip-step1`. The non-music parts correspond to small chats between songs. By removing these non-music parts, we can obtain 4 music clips from time positions 0-204, 303-489, 639-834, and 918-1128 seconds, respectively.

```{figure} ../figures/rwe-iip-step1-harry-styles.png
---
width: 800px
align: center
name: rwe-iip-step1
---
Non-music vs. music results obtained from Step 1.
```

By running audio fingerprinting on the 4 music clips stored as wavform files, we can get results from Step 2 as follows:

```
==> Query: ./harry-styles/npr_0-204.wav
  - no match
==> Query: ./harry-styles/npr_303-489.wav
  - no match
==> Query: ./harry-styles/npr_639-834.wav
  - no match
==> Query: ./harry-styles/npr_918-1128.wav
  - no match
```

Our database contains fingerprints of the official-released version of the 4 songs. The “no match” results show that audio fingerprinting is highly sensitive to identify a particular version of a piece of music. These 4 songs played at the NPR Tiny Desk Concert are live versions of the official ones. Therefore version identification is required to identify the 4 music clips. 

The following results from Step 3 present the distance between embeddings of each music clip and 4 official-released songs stored as mp3 files.

```
==> Distance for npr_0-204.wav
  * 0.2447 vs. cherry.m4a
  - 0.9246 vs. watermelon_sugar.m4a
  - 0.8516 vs. to_be_so_lonely.m4a
  - 0.7729 vs. adore_you.m4a
==> Distance for npr_303-489.wav
  - 0.8904 vs. cherry.m4a
  * 0.2077 vs. watermelon_sugar.m4a
  - 0.7374 vs. to_be_so_lonely.m4a
  - 0.6880 vs. adore_you.m4a
==> Distance for npr_639-834.wav
  - 0.9142 vs. cherry.m4a
  - 0.7441 vs. watermelon_sugar.m4a
  * 0.1798 vs. to_be_so_lonely.m4a
  - 0.5792 vs. adore_you.m4a
==> Distance for npr_918-1128.wav
  - 0.7170 vs. cherry.m4a
  - 0.7801 vs. watermelon_sugar.m4a
  - 0.7000 vs. to_be_so_lonely.m4a
  * 0.2911 vs. adore_you.m4a
```

Star symbol (`*`) indicates the distance is less than 0.35, which implies a high similarity. Since no other songs in our database obtain such degree of similarity, we conclude that the 4 music clips are identified as:
- 00:00-03:24 clip (npr_0-204.wav) is [_Cherry_](https://www.youtube.com/watch?v=rGeJ73yAAhQ) (`cherry.m4a`).
- 05:03-08:09 clip (npr_303-489.wav) is [_Watermelon Sugar_](https://www.youtube.com/watch?v=E07s5ZYygMg) (`watermelon_sugar.m4a`).
- 10:39-13:54 clip (npr_639-834.wav) is [_To Be So Lonely_](https://www.youtube.com/watch?v=6PPK-6FeJ9A) (`to_be_so_lonely.m4a`).
- 15:18-18:48 clip (npr_918-1128.wav) is [_Adore You_](https://www.youtube.com/watch?v=iquhBgM-Qv0) (`adore_you.m4a`).

{numref}`rwe-iip-step3` annotates the distance results from version identification by superimposing to {numref}`rwe-iip-step1`.

```{figure} ../figures/rwe-iip-step3-harry-styles.png
---
width: 800px
align: center
name: rwe-iip-step3
---
Distance results from version identification.
```