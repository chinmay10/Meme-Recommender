from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytesseract

im = np.array(Image.open('meme.jpg'))
"""
plt.figure(figsize=(10,10))
plt.title('PLAIN IMAGE')
plt.imshow(im); plt.xticks([]); plt.yticks([])
plt.savefig('img1.png')
"""
im= cv2.bilateralFilter(im,5, 55,60)
"""
plt.figure(figsize=(10,10))
plt.title('BILATERAL FILTER')
plt.imshow(im); plt.xticks([]); plt.yticks([])
plt.savefig('img2.png',bbox_inches='tight')
"""
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
"""
plt.figure(figsize=(10,10))
plt.title('GRAYSCALE IMAGE')
plt.imshow(im, cmap='gray'); plt.xticks([]); plt.yticks([])
plt.savefig('img3.png',bbox_inches='tight')
"""
_, im = cv2.threshold(im, 240, 255, 1) 
"""
plt.figure(figsize=(10,10))
plt.title('IMMAGINE BINARIA')
plt.imshow(im, cmap='gray'); plt.xticks([]); plt.yticks([])
plt.savefig('img4.png',bbox_inches='tight')
"""
text = pytesseract.image_to_string(im, lang='eng')
print(text.replace('\n', ''))
