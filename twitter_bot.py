import tweepy
import time
import requests
from datetime import datetime, timedelta
import json
from PIL import Image

def status_time(user_id, api):
    # Check last status date
    timeline = api.user_timeline(id = user_id, include_rts=False, count = 1)
    if (datetime.now() - timedelta(hours=3)) < timeline[0].created_at:
        return False
    return True

def fav_media(user_id, pic_id, api):
    # Find the most fav status
    timeline = api.user_timeline(id = user_id, include_rts=False, count = 6)
    fav_status = timeline[0]
    new_status = True
    for Status in timeline:
        if Status.id == pic_id:
            new_status = False
        if fav_status.favorite_count < Status.favorite_count:
            fav_status = Status
    if status_time('loaki_bot', api) == False:
        new_status = False
    if new_status == True:
        pic_id = fav_status.id
    fav_pic = fav_status.entities['media'][0]['media_url']
    return fav_pic, pic_id, new_status

def merge_image(im1, im2):
    im1 = Image.open(im1)
    im2 = Image.open(im2)
    w1, h1 = im1.size
    w2, h2 = im2.size
    size = (w2, h2)
    im3 = Image.new('RGB',size)
    pix1 = im1.load()
    pix2 = im2.load()
    pix3 = im3.load()
    data_file = open('data.json', 'r+')
    n_im =json.load(data_file) 
    for i in range(size[0]):
        for j in range(size[1]):
            i1 = float(i) / float(size[0]) * w1
            i2 = float(i) / float(size[0]) * w2
            j1 = float(j) / float(size[1]) * h1
            j2 = float(j) / float(size[1]) * h2
            pix3[i,j] = int((pix1[i1,j1][0] + pix2[i2,j2][0]) / 2), int((pix1[i1,j1][1] + pix2[i2,j2][1]) / 2), int((pix1[i1,j1][2] + pix2[i2,j2][2]) / 2)
    im3.save('merge.jpg')
    data_file = open('data.json', 'w+')
    json.dump(n_im + 1, data_file)

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

try:
    pic_id = 0
    date_min = datetime.now().strftime("%M")
    while 1:
        # Run once every 10 min
        if datetime.now().strftime("%M") != date_min and int(datetime.now().strftime("%M")) % 10 == 0:
            date_min = datetime.now().strftime("%M")
            fav_pic, pic_id, new_status = fav_media('archillect', pic_id, api)
            if new_status == True:
                dl_image(fav_pic)
                merge_image('merge.jpg', 'dl.jpg')
                api.update_with_media('merge.jpg')
            time.sleep(60)
finally:
    api.send_direct_message(api.get_user('loaki_').id, 'bot got killed')