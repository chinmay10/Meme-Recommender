import json
import os
import re
import boto3

def extract_metadata(json_file):
    pattern = r'\#\w+'
    data = None
    with open(json_file,'r') as jf:
        d = json.load(jf)
        caption = d['node']['edge_media_to_caption']['edges'][0]['node']['text']
        hashtags = re.findall(pattern, caption)
        owner = d['node']['owner']['username']
        likes = d['node']['edge_media_preview_like']['count']
        comments = d['node']['edge_media_to_comment']['count']
        timestamp = d['node']['taken_at_timestamp']
        is_video = d['node']['is_video']
        page_likes = d['node']['owner']['edge_followed_by']['count']
        data = {
            'file' : json_file.split('/')[-1],
            'caption': caption,
            'hastags': json.dumps(hashtags),
            'owner' : owner,
            'page_likes' : page_likes,
            'likes' : likes,
            'comments' : comments,
            'timestamp' : timestamp,
            'is_video' : is_video
        }
    return data


def put_item(table,metadata):
    response = table.put_item(
    Item= metadata
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"{metadata['file']} upload success")
    else:
        print(f"{metadata['file']} upload failed")


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('memes_metadata')
    for file in os.listdir('json_docs'):
        try:
            metadata = extract_metadata('json_docs/'+file)
            put_item(table, metadata)
        except Exception as e:
            print(f"unable to process and upload {file}")
            print(e)
