import numpy as np
import gensim
from gensim.models import KeyedVectors
import transformers
import redis
import torch
import boto3
import pickle
import json

def get_word2vec_embedding(word):
    """
    Get word2vec embedding for a word
    """
    try:
        embedding = wv_model[word]
    except KeyError:
        embedding = np.zeros((300,))
    return embedding

def put_embedding(key, value):
    value = value.tolist()
    value = ','.join([str(val) for val in value])
    print(value)
    # print(len(val.split(',')))
    # val = pickle.dumps(val.encode('utf-8'))
    r.set(key, value)

def get_all_hashtags():
    hashtags = set()
    dynamodb = boto3.resource('dynamodb')
    table_name = "memes_metadata"
    table = dynamodb.Table(table_name)
    response = table.scan()
    while 'LastEvaluatedKey' in response:
        for item in response['Items']:
            taglist = json.loads(item['hastags'])
            taglist = [tag.split('#')[-1] for tag in taglist]
            # print(taglist)
            hashtags = hashtags | set(taglist)
        # break
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    # print(len(hashtags))
    return hashtags

def main():
    hashtags = get_all_hashtags()
    # print(hashtags)
    for tag in hashtags:
        try:
            wv = get_word2vec_embedding(tag)
            print(f'embed of {tag} success')
            print(f'{wv.shape}')
        except Exception as e:
            print(f"embed of {tag} failed")
        try:
            put_embedding(tag, wv)
            print(f'put of {tag} success')
        except Exception as e:
            print(f"put of {tag} failed")
            print(e)



if __name__ == '__main__':
    wv_model = KeyedVectors.load_word2vec_format('~/Downloads/GoogleNews-vectors-negative300.bin.gz', binary=True)
    r = redis.Redis(host='localhost', port=6379, db=0)
    main()

