#!/usr/bin/env python
# coding: utf-8

# # Similarity between Songs
# 
# In this example, we use the official and other versions of _I'll Be There_ to illustrate similarity measurements between songs.
# 
# ## Using Audio Fingerprinting
# 
# Assume that our database contains the official released _I'll Be There_ by Jess Glynne ([YouTube video](https://www.youtube.com/watch?v=iQp1_GfDhwQ)). Given a 10-second fragment as a query (clipped from 0:40 to 0:50 in the video and saved as `fragment-10s-from-official.wav`), our audio fingerprinting model can successfully recognise it along with the timestamp information. Following code block demonstrates the calculation using 1 CPU with 7.5 GB memory.

# In[1]:


query_filenames = ["fragment-10s-from-official.wav"]
query_filepaths = ["../../example-audio/i-will-be-there/fragment-10s-from-official.wav"]
database_filenames = ["official-by-jess-glynne.m4a"]
database_filepaths = ["../../example-audio/i-will-be-there/official-by-jess-glynne.m4a"]

import sys, os, time
sys.path.append("../../dv-audio-models/audio-fingerprint")
import fingerprint as fp

def get_minsec(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    minsec = "{:02d}:{:02d}".format(m, s)
    return minsec

start_time = time.time()

print("==> Get inverted fingerprint hashes from database of {} songs".format(len(database_filepaths)))
db_songs = []
for filename, filepath in zip(database_filenames, database_filepaths):
    audio_input = [filename, filepath]
    hashes = fp.fingerprint(audio_input)
    invert = fp.get_invert_from_hashes(hashes)
    db_songs.append(invert)

database_hash_time = time.time()
print("    using {} seconds".format(round(database_hash_time - start_time, 3)))

print("==> Get fingerprint hashes from queries of {} fragments".format(len(query_filepaths)))
query_songs_hashes = []
for filename, filepath in zip(query_filenames, query_filepaths):
    audio_input = [filename, filepath]
    hashes = fp.fingerprint(audio_input)
    query_songs_hashes.append(hashes)

query_hash_time = time.time()
print("    using {} seconds".format(round(query_hash_time - database_hash_time, 3)))
    
query_matches = []
for query_hashes in query_songs_hashes:
    query_matches.append(fp.find_matches(query_hashes, db_songs))
    
for audio, match in zip(query_filepaths, query_matches):
    print("==> Query: {}".format(audio))
    most_match = fp.find_most_match_seconds(match, 256/22050)
    top1_match = most_match["top1_match"]
    top1_score = most_match["top1_score"]
    top1_starttime = most_match["top1_starttime"]
    query_matchstart = most_match["query_matchstart"]
    query_matchend = most_match["query_matchend"]
    query_matchdur = query_matchend - query_matchstart 
    if query_matchdur == 0 or top1_score < 10 * query_matchdur:
        print("  - no match")
    else: 
        print("  - top1 match: {}".format(top1_match))
        print("  - top1's {} match query's {}".format(get_minsec(top1_starttime), get_minsec(query_matchstart)))
        print("  - match till query's {}s (about {})".format(query_matchend, get_minsec(query_matchend)))

index_time = time.time()
print("==> Index using {} seconds".format(round(index_time - query_hash_time, 3)))


# ## Using Version Identification
# 
# Since audio fingerprinting is highly sensitive to identify a particular version of a piece of music, if any of the following versions are used as queries, no match will be returned, unless our database already contains fingerprints of these versions.
# - `violin-by-barbara-koba.m4a` ([Youtube video](https://www.youtube.com/watch?v=HZsNvx1bAzU)): original vocal parts are performed by violin;
# - `cover-by-kimberly-fransens.m4a` ([Youtube video](https://www.youtube.com/watch?v=VEQsJR7jK0c)): a cover song performed by another singer with guitar accompaniment.
# - `guitar-by-shoestringkaraoke.m4a` ([Youtube video](https://www.youtube.com/watch?v=e0c5V0gRxuI)): an instrumental version played by guitar.
# 
# In this case, we can obtain the audio embeddings of the above 3 songs and then compare with our database, which contains the embedding of the official release (`official-by-jess-glynne.m4a`) and other 2023 songs randomly obtained from YouTube. If pairwise similarity measurement returns a distance score smaller than 0.45, the input query can be considered as a version candidate. Following code block demonstrates the calculation using 1 CPU with 7.5 GB memory.

# In[2]:


sys.path.append("../../dv-audio-models/audio-embedding")
import models
from embedding import *
import numpy as np
from tqdm.notebook import tqdm

# query info
query_filenames = ["violin-by-barbara-koba.m4a", 
                   "cover-by-kimberly-fransens.m4a", 
                   "guitar-by-shoestringkaraoke.m4a"]
query_list = ["../../example-audio/i-will-be-there/violin-by-barbara-koba.m4a", 
              "../../example-audio/i-will-be-there/cover-by-kimberly-fransens.m4a", 
              "../../example-audio/i-will-be-there/guitar-by-shoestringkaraoke.m4a"]
# database info
official_filenames = ["official-by-jess-glynne.m4a"]
official_list = ["../../example-audio/i-will-be-there/official-by-jess-glynne.m4a"]
embeddings_2023 = np.load("../../dv-audio-models/audio-embedding/demo_data/embeddings_2023.npy")
audiofile_2023 = np.load("../../dv-audio-models/audio-embedding/demo_data/audiofile_2023.npy").tolist()

start_time = time.time()

print("==> Step 1: audio pre-processing")
audio_representation_list = []
for audio_path in tqdm(query_list + official_list):
    audio_representation = get_audio_representation(audio_path)
    audio_representation_list.append(audio_representation)

print()
step1_time = time.time()
    
print("==> Step 2: obtain embeddings")
data = Dataset(audio_representation_list, out_length=None)
dataloader = DataLoader(data, 1, shuffle=False, num_workers=0)
model = load_model(models)
embeddings = get_norm_embedding(model, dataloader)

embedding_official = embeddings[-1]
embeddings_query = embeddings[:len(query_list)]
embeddings_database = np.vstack((embedding_official, embeddings_2023))

print()
step2_time = time.time()

print("==> Step 3: embedding distance beetween {} queries and official-by-jess-glynne.m4a".format(len(query_list)))
for idx, embedding_query in enumerate(embeddings_query):
    dis = 1 - np.matmul(embedding_query, embedding_official.T)
    print("  - {} vs. official: {:.4f}".format(query_filenames[idx], dis))

print()    
step3_time = time.time()

print("==> Step 4: similarity ranking")
print("  Measure the distance between {} queries and database of".format(len(query_list)))
print("  total {} songs in a pairwise fashion. If distance<0.45,".format(len(embeddings_database)))
print("  present rank | distance | filename of the database song.")

audiofiles_database = official_filenames + audiofile_2023
labels_database = [1] * len(official_filenames) + [0] * len(audiofile_2023)
audio2label = dict()
for audio, label in zip(audiofiles_database, labels_database):
    audio2label[audio] = label

for idx, embedding_query in enumerate(embeddings_query):
    print("--> Query: {}".format(query_filenames[idx]))
    dis_list = 1 - np.matmul(embedding_query, embeddings_database.T)

    row = []
    for dis, audio in zip(dis_list, audiofiles_database):
        row.append([dis, audio])
    row.sort(key=lambda x: x[0])
    n_database = len(row)
    for i, (dis, audio) in enumerate(row):
        label = audio2label[audio]
        rank = i + 1
        if label:
            print("  - {}/{} | {:.4f} | {}".format(rank, n_database, dis, audio))
        else:
            if dis < 0.45:
                print("  * {}/{} | {:.4f} | {}".format(rank, n_database, dis, audio))  

print()
step4_time = time.time()

print("==> Calculation time (seconds) using 1 CPU with 7.5 GB memory")
print("  - Step 1 audio pre-processing: {:.3f} ".format(step1_time - start_time))
print("  - Step 2 obtain embeddings: {:.3f} ".format(step2_time - step1_time))
print("  - Step 3 embedding distance: {:.3f} ".format(step3_time - step2_time))
print("  - Step 4 similarity ranking: {:.3f} ".format(step4_time - step3_time))
print("  - Total: {:.3f}".format(time.time() - start_time))


# We can observe from the results in Step 4 that using the current thresholding value may retrieve songs not related to the query. In real-world applications, the notion of similarity used to compare different audio recordings largely depends on the respective application as well as the user requirements. Therefore this thresholding value can be adjusted according to the application scenarios.
