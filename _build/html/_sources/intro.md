# Introduction

One important topic in music information retrieval (MIR) is concerned with the development of search engines that enable users to explore music collections in a flexible and intuitive way. Traditional search engines are text-based retrieval systems. In the case that such textual descriptions are not available, one requires content-based retrieval strategies which only utilize the raw audio material. These strategies usually follow **the query-by-example paradigm: given an audio query, the task is to retrieve all songs that are somehow similar or related to the query**. 

Beici has been developing various audio content-based retrieval strategies to handle different application scenarios. They all use audio embeddings, in other words, feature vectors from a signal processing or machine learning model, to represent music content explicitly or implicitly. Related songs can be returned by comparing their audio embeddings that represent genres, melodies, and other music characteristics from the audio contents. In this book, following models and examples are demonstrated:

::::{grid} 2
:::{grid-item-card} Audio Models
**[](audio-models/music_classification.md)**: Fragment-level classification of audio into different categories such as content types, genres and so on.

**[](audio-models/music_identification.md)**: Identification of a particular recording that is the source of the query, or the underlying music given a recording of a derivative version.

**[](audio-models/audio_embedding.md)**: A novel representation of the whole song as a fixed-length feature vector to be used in different downstream tasks.
:::
:::{grid-item-card} Real World Examples
**[](real-world-examples/content_based_recommendation)**: What songs will be recommended based on the audio content correlation to the given candidate song.

**[](real-world-examples/similarity_between_songs)**: At different levels of specificity and granularity, learn how to measure the similarity between the query and the database songs to be retrieved.

**[](real-world-examples/identification_in_podcasts)**: Given an episode from a podcast, learn how to detect the presence of music to obtain music clips, and identify corresponding songs.
:::
::::

:::{admonition} To illustrate the subtle but crucial differences between the retrieval strategies, a classification scheme based on specificity and granularity is used. 
:class: tip, dropdown

**Specificity** refers to the degree of similarity between the query and the database songs. For example, audio fingerprinting is a highly specific retrieval system that matches exact or near copies of the query, while specificity in genre classification is relatively low.

**Granularity** refers to the temporal level considered in the retrieval scenario. In fragment-level scenarios, the query consists of a short fragment of an audio recording, and the goal is to retrieve all related fragments that are contained in the database songs. In contrast, in song-level scenarios, the query reflects characteristics of an entire song and is respectively compared with entire songs of the database. 

For a further overview of content-based audio retrieval, please refer to {cite}`GroscheMS12_ContentBasedMusicRetrieval_DagstuhlFU`.
:::
