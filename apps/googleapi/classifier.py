from sentence_transformers import SentenceTransformer, util
import numpy as np
import itertools

model = SentenceTransformer('bert-base-nli-mean-tokens')

list1 = ["I love python programming", "Python is versatile", "Python is easy to learn"]
list2 = ["Machine learning is exciting", "Python is used in machine learning", "I want to learn about AI"]
list3 = ["Java is another programming language", "I prefer Python over Java", "Python has a large community"]
list4 = ["I like hiking in the mountains", "Nature is beautiful", "Hiking is good for health"]


# Encode the sentences into embeddings for all 100 lists
all_embeddings = [model.encode(lst, convert_to_tensor=True) for lst in [list1, list2, ..., list100]]
all_sentences = [list1, list2, list3, list4]

# Calculate the similarity between all combinations of one sentence from each list
max_sim = 0.0
max_sentences = None

for sentences in itertools.product(*all_sentences):
    print(sentences)
    embeddings = [model.encode(sentence, convert_to_tensor=True) for sentence in sentences]
    # avg_sim = util.pytorch_cos_sim(embeddings, embeddings).mean().item()
    # if avg_sim > max_sim:
    #     max_sim = avg_sim
    #     max_sentences = sentences

# Print the most similar sentences first
# if max_sentences is not None:
#     print(f"Highest Similarity: {max_sim:.4f}")
#     print("\n".join(max_sentences))

