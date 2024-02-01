from PIL import Image
import numpy as np
import matplotlib.pyplot as plt 
import cv2 
import pytesseract
import boto3
import os

def get_meme_text(image):
    text = None
    try:
        im = np.array(Image.open(image))
        im= cv2.bilateralFilter(im,5, 55,60)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        _, im = cv2.threshold(im, 240, 255, 1)  
        text = pytesseract.image_to_string(im, lang='eng')
        print(f"extracted text from {image}")
    except Exception as e:
        print(f"unable to extract text from {image}")
        print (e)
    finally:
        return text

def put_item(image, meme_text):
    global table
    response = table.put_item(
    Item={
        'image_name': image,
        'meme_text': meme_text
    }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'{image} uploaded successfully')
    else:
        print(f'unable to upload {image}')


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('decoded_memes')
    image_dir = '/scratch/user/rkoripal_97/OnlyMemes/media/'
    for img in os.listdir(image_dir):
        meme_text = get_meme_text(image_dir+img)
        #print(meme_text)
        put_item(img, meme_text)
        break
    


