#import all the liberaries
import time
import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
from PIL import Image

#globally declare the access token and base url
APP_ACCESS_TOKEN='4387757580.5a17879.298d623be23f4041a218ef05ff4306b4'
BASE_URL='https://api.instagram.com/v1/'

#function fetch and print the information of accesss token's owner
def self_info():
    request_url=(BASE_URL+'users/self/?access_token=%s') %(APP_ACCESS_TOKEN)
    print ('GET request url:%s') %(request_url)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print ('Username:%s') %(user_info['data']['username'])
            print ('No.of followers:%s') %(user_info['data']['counts']['followed_by'])
            print ('No.of people you are following:%s') %(user_info['data']['counts']['follows'])
            print ('No. of posts:%s') %(user_info['data']['counts']['media'])
        else:
            print 'User dosen\'t exist'
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)
#function fetch and return the user id of the user
def get_user_id(insta_username):
    request_url=(BASE_URL+'users/search/?q=%s&access_token=%s') %(insta_username,APP_ACCESS_TOKEN)
    print ('GET request url:%s') %(request_url)
    user_info=requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if user_info['data']:
            return user_info['data'][0]['id']
        else:
            print 'User_id can\'t found'
            exit()
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)

#function gets the profile info of the user
def get_user_info(insta_username):
    user_id=get_user_id(insta_username)
    if user_id==None:
        print 'User doesn\'t Exist'
        exit()
    else:
        request_url=(BASE_URL+'users/%s/?access_token=%s') %(user_id,APP_ACCESS_TOKEN)
        print ('GET request url:%s') %(request_url)
        user_info=requests.get(request_url).json()
        if user_info['meta']['code'] == 200:
            if (user_info['data']):
                print ('Username:%s') % (user_info['data']['username'])
                print ('No.of followers:%s') % (user_info['data']['counts']['followed_by'])
                print ('No.of people you are following:%s') % (user_info['data']['counts']['follows'])
                print ('No. of posts:%s') % (user_info['data']['counts']['media'])
            else:
                print 'User dosen\'t exist'
        else:
            print 'Status code recieved other then 200'
    time.sleep(5)

#function downloads the recent media of access token's owner
def get_own_post():
    request_url=(BASE_URL+'users/self/media/recent/?access_token=%s') %(APP_ACCESS_TOKEN)
    print ('GET request url:%s') %(request_url)
    own_media=requests.get(request_url).json()
    if own_media['meta']['code']==200:
        if len(own_media['data']):
            image_name=own_media['data'][0]['id']+'.jpeg'
            image_url=own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print 'Your image have been downloaded successfully'
            time.sleep(5)
            return own_media['data'][0]['id']
        else:
            print 'Post doesn\'t exist'
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)
    return None

#function downloads the recent media of the user
def get_user_post(insta_username):
    user_id=get_user_id(insta_username)
    if user_id==None:
        print 'User doesn\'t exist'
        exit()
    request_url=(BASE_URL+'users/%s/media/recent/?access_token=%s') %(user_id,APP_ACCESS_TOKEN)
    print ('GET request url:%s') %(request_url)
    user_post=requests.get(request_url).json()
    if user_post['meta']['code']==200:
        if len(user_post['data']):
            image_name = user_post['data'][0]['id'] + '.jpeg'
            image_url = user_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image have been downloaded successfully'
            time.sleep(5)
            return user_post['data'][0]['id']
        else:
            print 'There is no recent post'
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)
    return None
#function prints the url of recent media liked by the owner of access token
def post_likes():
    request_url=(BASE_URL+'users/self/media/liked/?access_token=%s') %(APP_ACCESS_TOKEN)
    print ('GET request url:%s\n') %(request_url)
    own_post_likes=requests.get(request_url).json()
    if own_post_likes['meta']['code']==200:
        if len(own_post_likes):
            print own_post_likes['data'][0]['images']['standard_resolution']['url']
        else:
            print 'Post doesn\'t exist'
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)
    return None

#function fetch and returns the media id
def get_post_id(insta_username):
    user_id=get_user_id(insta_username)
    request_url=BASE_URL+'users/%s/media/recent/?access_token=%s' %(user_id,APP_ACCESS_TOKEN)
    print 'Get request id: %s' %(request_url)
    media_id=requests.get(request_url).json()

    if media_id['meta']['code']==200:
        if media_id['data']:
            return media_id['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)

# function likes on the users post
def like_a_post(insta_username):
    media_id=get_post_id(insta_username)
    request_url=BASE_URL+'media/%s/likes' %(media_id)
    payload={"access_token": APP_ACCESS_TOKEN}
    print ('POST request url:%s') \
          %(request_url)
    post_a_like=requests.post(request_url,payload).json()
    if post_a_like['meta']['code']==200:
        print 'Like was successful.'
    else:
        print 'Like was unsuccesful.'
    time.sleep(5)

#function post a comment on the users post
def post_a_comment(insta_username):
    media_id=get_post_id(insta_username)
    request_url=BASE_URL+'media/%s/comments' %(media_id)
    comment=raw_input('What is your comment:')
    payload={'access_token':APP_ACCESS_TOKEN,'text':comment}
    comment_a_post=requests.post(request_url,payload).json()
    if comment_a_post['meta']['code']==200:
        print 'comment successful.'
    else:
        print 'comment unsuccessful'
    time.sleep(5)

#function prints the list of commments on the users post
def list_of_comment(insta_username):
    media_id=get_post_id(insta_username)
    request_url=(BASE_URL+'media/%s/comments?access_token=%s') %(media_id,APP_ACCESS_TOKEN)
    print ('GET request url: %s') %(request_url)
    comment_list=requests.get(request_url).json()
    if comment_list['meta']['code']==200:
        if  comment_list['data']:
            for x in range(0,len(comment_list['data'])):
                comment_text=comment_list['data'][x]['text']
                print comment_text
                print '\n Fetch comment list successfully'
        else:
            print'comment doesn\'t exist'
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)

#function prints the list of users who liked the post of access token's owner
def list_of_likes():
    media_id=get_media_id()
    request_url=BASE_URL+'media/%s/likes?access_token=%s' %(media_id,APP_ACCESS_TOKEN)
    print 'GET request url:%s' %(request_url)
    likes_list=requests.get(request_url).json()
    if likes_list['meta']['code']==200:
        if likes_list['data']:
            for x in range(0,len(likes_list['data'])):
                likes=likes_list['data'][x]['username']
                print likes
        else:
            print 'likes doesn\'t exist'
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)

#function fetch and returns the media id
def get_media_id():
    request_url=(BASE_URL+'users/self/media/recent/?access_token=%s') %(APP_ACCESS_TOKEN)
    print ('GET request url:%s') %(request_url)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200:
        if user_info['data']:
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)

#function deletes the negative comments from the post of user
def delete_comments():
    media_id=get_media_id()
    request_url=BASE_URL+'media/%s/comments?access_token=%s' %(media_id,APP_ACCESS_TOKEN)
    print 'GET request url:%s' %(request_url)
    comment_info=requests.get(request_url).json()

    if comment_info['meta']['code']==200:
        if len(comment_info['data']):

            for x in range(0,len(comment_info['data'])):
                comment_id=comment_info['data'][x]['id']
                comment_text=comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print 'Negative comment:%s' %(comment_text)
                    delete_url=BASE_URL+'media/%s/comments/%s?access_token=%s' %(media_id,comment_id,APP_ACCESS_TOKEN)
                    print 'DELETE request url:%s' %(delete_url)
                    delete_comment=requests.delete(delete_url).json()
                    if delete_comment['meta']['code']==200:
                        print 'Delete comment successfuly.'
                    else:
                        print 'Unable to delete'
                else:
                    print 'Positive comment:%s' %(comment_text)
        else:
            print 'There no existing comment on post'
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)

#function compare between positive and negative comments and plot pie chart
def compare():
    positive=0
    negative=0
    media_id = get_media_id()
    request_url = BASE_URL + 'media/%s/comments?access_token=%s' % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url:%s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):

                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.classification=='pos':
                    positive=positive+1
                else:
                    negative=negative+1
        else:
            print 'There no existing comment on post'
        labels = 'Positive', 'Negative'
        sizes = [positive, negative]
        colors = ['green', 'red']
        explode = (0.1, 0)  # explode 1st slice
        # Plot
        plt.pie(sizes,explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.show()
    else:
        print 'Status code recieved other then 200'
    time.sleep(5)

#function ask you the index number to get the user's post
def getpost_in_creative_way(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User doesn\'t exist'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print ('GET request url:%s') % (request_url)
    user_post = requests.get(request_url).json()

    if user_post['meta']['code']==200:
        if user_post['data']:
            index = int(raw_input('Which post do you want to get(index position):'))
            print user_post['data'][index]['images']['standard_resolution']['url']+':',
            if user_post['data'][index]['caption'] !='null':
                print user_post['data'][index]['caption']['text']
            else:
                print 'Caption doesn\'t available'
        else:
            print 'Post doesn\'t exist'
    else:
        print 'status code other then 200 recieved'
    time.sleep(5)

#function make the wordcloud of trends and subtrends
def word_cloud(insta_username):

    user_id = get_user_id(insta_username)
    request_url = BASE_URL + 'users/%s/media/recent/?access_token=%s' % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url:%s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            if user_info['data'][0]['caption']['text'] == None:
                print 'Caption not available.'
                exit()
            text = user_info['data'][0]['caption']['text'] + ' ' + user_info['data'][1]['caption']['text'] + ' ' + \
            user_info['data'][2]['caption']['text']
            mask = np.array(Image.open("C:\\Mridul\\DSC_0064.JPG"))
            image_colors = ImageColorGenerator(mask)
            wordcloud_final = WordCloud(
                font_path='C:\\Windows\\Fonts\\cour.ttf',
                background_color='white',
                width=1800,
                height=1400,
                mask=mask
            ).generate(text)
            plt.imshow(wordcloud_final.recolor(color_func=image_colors))
            plt.axis("off")
            plt.show()
        else:
            print 'tags doesnt available'
    else:
        print 'status code other then 200 recived'

#Menu present in this function
def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:\n'
        print "a.Get your own details"
        print "b.Get details of a user by username"
        print "c.Get your own recent post"
        print "d.Get the recent post of a user by username"
        print "e.Get a list of people who have liked the recent post of a user"
        print "f.Like the recent post of a user"
        print "g.Get a list of comments on the recent post of a user"
        print "h.Make a comment on the recent post of a user"
        print "i.Delete negative comments from the recent post of a user"
        print "j.Media liked by the user"
        print "k.Compare between positive and negative comment"
        print "l.Get post in some creative way"
        print "m.Get the wordcloud of trends and sub trends"
        print "n.Exit"
        choice=raw_input("Enter you choice: ")
        choice=choice.lower()
        if choice=="a":
            #declaration of self_info function
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            # declaration of get_user_info function
            get_user_info(insta_username)
        elif choice=="c":
            # declaration of get_own_post function
            get_own_post()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            # declaration of get_user_post function
            get_user_post(insta_username)
        elif choice=="e":
            # declaration of list_of_likes function
            list_of_likes()
        elif choice=="f":
            insta_username = raw_input("Enter the username of the user: ")
            # declaration of like_a_post function
            like_a_post(insta_username)
        elif choice=="g":
            insta_username=raw_input("Enter the username of the user:")
            # declaration of list_of_comment function
            list_of_comment(insta_username)
        elif choice=="h":
            insta_username = raw_input("Enter the username of the user: ")
            # declaration post_a_comment function
            post_a_comment(insta_username)
        elif choice=="i":
            # declaration of delete_comments function
            delete_comments()
        elif choice=="j":
            # declaration of post_likes function
            post_likes()
        elif choice == "k":
            # declaration of compare function
            compare()
        elif choice=="l":
            insta_username = raw_input("Enter the username of the user: ")
            # declaration of getpost_in_creative_way function
            getpost_in_creative_way(insta_username)
        elif choice == "m":
            insta_username = raw_input("Enter the username of the user: ")
            # declaration of word_cloud function
            word_cloud(insta_username)
        elif choice == "n":
            exit()
        else:
            print "wrong choice"
#declare the start_bot function
start_bot()