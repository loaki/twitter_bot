import tweepy
import os
import requests
from datetime import datetime
from PIL import Image

def fav_media(id):
    timeline = api.user_timeline(id, include_rts=False)
    fav_status = timeline[0]
    for Status in timeline:
        if fav_status.favorite_count < Status.favorite_count:
            fav_status = Status
    fav_media = fav_status.entities['media'][0]['media_url']
    return fav_media

def merge_image(im1, im2):
    im1 = Image.open(im1)
    im2 = Image.open(im2)
    w1, h1 = im1.size
    w2, h2 = im2.size
    size = (min(w1, w2), min(h1, h2))
    im3 = Image.new('RGB',size)
    pix1 = im1.load()
    pix2 = im2.load()
    pix3 = im3.load()
    for i in range(size[0]):
        for j in range(size[1]):
            i1 = float(i) / float(size[0]) * w1
            i2 = float(i) / float(size[0]) * w2
            j1 = float(j) / float(size[1]) * h1
            j2 = float(j) / float(size[1]) * h2
            pix3[i,j] = ((pix1[i1,j1][0] + pix2[i2,j2][0]) / 2, (pix1[i1,j1][1] + pix2[i2,j2][1]) / 2, (pix1[i1,j1][2] + pix2[i2,j2][2]) / 2) 
    im3.save('merge.jpg')

def dl_image(url):
    filename = 'dl.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    else:
        print("Unable to download image")

# Authenticate to Twitter
auth = tweepy.OAuthHandler("3mdV9PUlft7Bxj2M4yyZTvIL7", "cyHM0m6tuE8ncDkFydt1TJXVwJETPMvCoSTabM9sgG35iteWVC")
auth.set_access_token("1305165317564493824-MPx4QIvv0q2IKTZrtkGGBsJL1Hznpr", "VrCnxrVbA9Pk8GttVkfQZ1na7eTYQq39TeUjZsKk7igqV")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
except:
    print("Error during authentication")
    exit()

while 1:
    time = datetime.now().strftime("%M")
    if time%5 == 0:
        fav_media = fav_media('archillect')
        dl_image(fav_media)
        merge_image('merge.jpg', 'dl.jpg')
        api.update_with_media('merge.jpg')