import boto3
import pandas as pd
from collections import defaultdict
from main.similarity_score import get_word2vec_doc_embedding, get_bert_embedding, get_similarity
import json
import numpy as np
import redis
import transformers 

def put_updated_feed(user_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName='Users',
        Key={
            'user_id': {'S': user_id}
        }
    )
    user_data = response['Item']
    feed_value = user_data['feed']['L']
    visited_images = []
    if 'visited_images' in user_data:
        visited_images = user_data['visited_images']['L']
    visited_images.extend(feed_value)
    dynamodb.update_item(
        TableName='Users',
        Key={
            'user_id': {'S': user_id}
        },
        UpdateExpression='SET visited_images = :val',
        ExpressionAttributeValues={
            ':val': {'L': visited_images}
        }
    )
    visited_images = [image['S'] for image in visited_images]
    liked_images = []
    if 'liked_images' in user_data:
        liked_images = user_data['liked_images']['L']
        liked_images = [image['S'] for image in liked_images]
        
    chosen_tags = []
    if 'chosen_tags' in user_data:
        chosen_tags = user_data['chosen_tags']['M']
        chosen_tags = [tag for tag, value in chosen_tags.items() if value['BOOL']]

    new_feed= generate_feed(visited_images,liked_images, chosen_tags)
    update_feed(user_id, new_feed)


def update_feed(user_id, feed):
    dynamodb = boto3.resource('dynamodb')
    table_name = "Users"
    table = dynamodb.Table(table_name)
    user_item = table.get_item(Key={'user_id': user_id})['Item']
    user_item['feed'] = feed
    table.put_item(Item = user_item)

def generate_feed(visited_images, liked_images, chosen_tags):
    """
    get feed using embeds from npz file for given user query
    """
    SIMILARITY_WEIGHT = 0.7
    LIKES_WEIGHT = 0.1
    COMMENTS_WEIGHT = 0.2
    r = redis.Redis(host='localhost', port=6379, db=0)
    csv_file = "/Users/ramsankar/Documents/ISR/OnlyMemes/MemeRec/MemeRec/Recommender/embeddings42.csv"
    embeddings_data=pd.read_csv(csv_file)
    embeddings_data = embeddings_data[embeddings_data['is_video']==False]
    embeddings_data = embeddings_data.reset_index()
    bert_model = transformers.AutoModel.from_pretrained('bert-base-uncased', from_tf = False)
    bert_tokenizer = transformers.AutoTokenizer.from_pretrained('bert-base-uncased')
    hashtags_list = embeddings_data['hastags'].apply(json.loads)
    hashtags_dict=dict(zip(embeddings_data['file'], hashtags_list))
    user_dict=defaultdict(int)
    for c in chosen_tags:
        user_dict[c]+=1
    for li in liked_images:
        for i in hashtags_dict[li]:
            user_dict[i]+=1
    print(user_dict)      
    visited=dict.fromkeys(visited_images,1)
    feed=[]
    user_doc_embed = get_word2vec_doc_embedding(user_dict,r)
    user_bert_embed = get_bert_embedding(' '.join(user_dict.keys()),bert_tokenizer, bert_model)    
    embeddings_data['doc_embedding'] = embeddings_data['doc_embedding'].apply(lambda x: np.array(json.loads(x)))
    embeddings_data['bert_embedding'] = embeddings_data['bert_embedding'].apply(lambda x: np.array(json.loads(x)))
    embed_size=embeddings_data['doc_embedding'].size
    
    for i in range(embed_size):
        if embeddings_data.loc[i,'file'] in visited:
            continue
        meme_bert_embed = embeddings_data.loc[i,'bert_embedding']
        meme_doc_embed = embeddings_data.loc[i,'doc_embedding']
        sim = get_similarity(user_bert_embed, user_doc_embed, meme_bert_embed, meme_doc_embed)
        score = sim * SIMILARITY_WEIGHT + embeddings_data.loc[i,'norm_likes'] * LIKES_WEIGHT + embeddings_data.loc[i,'norm_comments'] * COMMENTS_WEIGHT
        feed.append([embeddings_data.loc[i,'file'],score])
        # feed.append([embeddings_data.loc[i,'file'], sim, embeddings_data.loc[i,'likes'], embeddings_data.loc[i,'comments'], embeddings_data.loc[i,'hastags'], score])
    feed.sort(key=lambda x:x[1], reverse=True)
    feed=[x[0] for x in feed]
    return feed[:20]
