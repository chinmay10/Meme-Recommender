import numpy as np
import gensim.downloader as api
import transformers as tf
from sklearn.metrics.pairwise import cosine_similarity
import torch
# Load word2vec model
wv_model = api.load('word2vec-google-news-300')

# Load BERT model and tokenizer
bert_model = tf.AutoModel.from_pretrained('bert-base-uncased',from_tf=True)
bert_tokenizer = tf.AutoTokenizer.from_pretrained('bert-base-uncased',from_tf=True)

def get_word2vec_embedding(word):
    """
    Get word2vec embedding for a word
    """
    try:
        embedding = wv_model[word]
    except KeyError:
        embedding = np.zeros((300,))
    return embedding

def get_word2vec_doc_embedding(doc):
    """
    Get word2vec document embedding for a dictionary of words
    """
    word_embeddings = []
    for word, freq in doc.items():
        embedding = get_word2vec_embedding(word)
        word_embeddings.append(embedding * freq)
    doc_embedding = np.sum(word_embeddings, axis=0) / sum(doc.values())
    return doc_embedding

def get_bert_embedding(text):
    """
    Get BERT embedding for a text
    """
    input_ids = bert_tokenizer.encode(text, return_tensors='pt', padding=True)
    with torch.no_grad():
        output = bert_model(input_ids)[0]
    embedding = np.mean(output.numpy(), axis=1).squeeze()
    return embedding

def get_soft_cosine_similarity(doc1, doc2):
    """
    Get Soft Cosine Similarity between two documents
    """
    doc1_embedding = get_word2vec_doc_embedding(doc1)
    doc2_embedding = get_word2vec_doc_embedding(doc2)
    bert_doc1_embedding = get_bert_embedding(' '.join(doc1.keys()))
    bert_doc2_embedding = get_bert_embedding(' '.join(doc2.keys()))
    similarity_matrix = cosine_similarity([bert_doc1_embedding], [bert_doc2_embedding])
    soft_cosine_similarity = np.dot(similarity_matrix, cosine_similarity([doc1_embedding], [doc2_embedding])[0])
    return soft_cosine_similarity[0]

# Example usage
user_query = {'dog': 1, 'cat': 1, 'pet':1}
document = {'dog': 1, 'cat': 1, 'pet': 1}
score = get_soft_cosine_similarity(user_query, document)
print('Soft Cosine Similarity score:', score)
