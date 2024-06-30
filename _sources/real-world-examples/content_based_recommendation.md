# Content-based Recommendation

Collaborative Filtering (CF) is a commonly used method that can infer similarities between items for recommendation. While CF performs well when historical data are available for each item, it suffers from the cold start problem for novel or unpopular items. New track releases will not be recommended unless their similarities can be learned directly from the audio content. This has motivated researchers to improve content-based recommendation system.

The audio embeddings previously introduced have been incorporated into the content-based recommendation system in [QQ Music](https://y.qq.com/) to recommend newly released or unpopular songs to the users (related patents filed in CN113032616A and CN113051425A). 

Here are two examples showing which top-2 songs among a collection of 200k songs at QQ Music are most audio-content-related to a given candidate. It's noted that the correlation is purely based on the cosine similarity between audio embeddings of every two songs.

::::{tab-set}
:::{tab-item} Example 1
Candidate song: [Billie Eilish - bad guy](https://www.youtube.com/watch?v=DyDfgMOUjCI)
- top-1: [Luna Shadows - lowercase](https://www.youtube.com/watch?v=SO_XQvN9nfg)
- top-2: [Vallis Alps - Young](https://www.youtube.com/watch?v=yoZPVMEsbeQ)
:::
:::{tab-item} Example 2
Candidate song: [DJ Wegun (DJ 웨건) - Venom (Feat. nafla 나플라)](https://www.youtube.com/watch?v=x5kt5EAVIAo)
- top-1: [BewhY (비와이) - In Trinity](https://www.youtube.com/watch?v=fZmjD3oV9gc)
- top-2: [6IX9INE - Kooda](https://www.youtube.com/watch?v=yz7Cn3pHibo)
:::
::::

If a higher specificity is required for similarity measurement, the audio embedding from version identification models can be used to explore songs that share similar harmonic progression. For example, using [Keenan Te - dependent](https://www.youtube.com/watch?v=H0USk7DX7ZM) as a candidate song, [Beyoncé - Halo](https://www.youtube.com/watch?v=bnVUHWCynig) will be returned.