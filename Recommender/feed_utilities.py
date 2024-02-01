import boto3
import pandas as pd
from collections import defaultdict
from similarity_score import get_word2vec_doc_embedding, get_bert_embedding, get_similarity
import json

def copy_feed(user_id):
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
    if 'liked_images' in user_data:
        liked_images = user_data['liked_images']['L']

    if 'chosen_tags' in user_data:
        chosen_tags = user_data['chosen_tags']['L']

    generate_feed(visited_images,liked_images, chosen_tags)



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
    SIMILARITY_WEIGHT = 0.8
    LIKES_WEIGHT = 0.1
    COMMENTS_WEIGHT = 0.1

    embeddings_data=pd.read_csv('/content/drive/MyDrive/ISR/embeddings4.csv')
    hashtags_list = embeddings_data['hastags'].apply(json.loads)
    hashtags_dict=dict(zip(embeddings_data['file'], hashtags_list))

    #generating user query from liked images
    user_dict=defaultdict(int)
    for c in chosen_tags:
        user_dict[c]+=1

    for li in liked_images:
        for i in hashtags_dict[li]:
            user_dict[i]+=1
    print(user_dict)      
    visited=dict.fromkeys(visited_images,1)

    #generating feed
    feed=[]
    user_doc_embed = get_word2vec_doc_embedding(user_dict)
    user_bert_embed = get_bert_embedding(' '.join(user_dict.keys()))

    
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