import requests
#from pprint import pprint
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer



response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']      #access token of a instagram
BASE_URL ="https://api.instagram.com/v1/"         #base url of instagram

#=======================================================================================================================

def owner_info():              #This function is used to get the information of the owner information

    response = requests.get("%susers/self/?access_token=%s"%(BASE_URL,APP_ACCESS_TOKEN)).json()
    if response['meta']['code']==200:                    #It is used to check the data is coming or not
        print 'username : %s' %(response['data']['username'])
        print 'No of followers : %s' % (response['data']['counts']['followed_by'])
        print 'No of people you are following : %s' % (response['data']['counts']['follows'])
        print 'No of people : %s'% (response['data']['counts']['media'])
    else:
        print "wroung informaton"

#=======================================================================================================================


def owner_recent_post():            ##This function is used to get the recent post of the profile owner
    response = requests.get("%susers/self/media/recent/?access_token=%s" % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        if len(response['data'])> 0:
            name= response['data'][0]['id'] + ".jpg"
            url = response['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(url,name)
            print url
            print "Image downloaded"
        else:
            print "user have no data"
    else:
        print "wroung informaton"

#=======================================================================================================================

def get_user_id(username):   #This function is used to get the id of the profile owner
    response = requests.get("%susers/search?q=%s&access_token=%s" % (BASE_URL, username, APP_ACCESS_TOKEN)).json()
    if len(response['data']):
        return response['data'][0]['id']
    else:
        print 'user not exist'

#=======================================================================================================================

def Otheruser_info(username):         #This function is used to get the information of the other user
    user_id = get_user_id(user_name)
    response = requests.get("%susers/%s/?access_token=%s"%(BASE_URL,user_id,APP_ACCESS_TOKEN)).json()
    if response['meta']['code']==200:
            print 'username : %s' %(response['data']['username'])
            print 'No of followers : %s' % (response['data']['counts']['followed_by'])
            print 'No of people you are following : %s' % (response['data']['counts']['follows'])
            print 'No of people : %s'% (response['data']['counts']['media'])
    else:
        print "wroung informaton"

#=======================================================================================================================
def Otheruser_recentpost(username):     #This function is used to get the recent post of the other user
    user_id = get_user_id(user_name)
    response = requests.get("%susers/%s/media/recent/?access_token=%s" % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        if len(response['data'])> 0:
            name = response['data'][0]['id'] + ".jpg"
            url = response['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(url, name)
            print "Image downloaded"
        else:
            print "user have no data"
    else:
        print "wroung informaton"


#=======================================================================================================================

def get_media_id(username):        #This function is used to get the id of the other user
    user_id = get_user_id(username)
    response = requests.get("%susers/%s/media/recent/?access_token=%s" % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        if len(response['data']) > 0:
            return response['data'][0]['id']
        else:
            print "user have no data"
    else:
        "Code recive other than 200"


#========================================================================================================================

def like_on_post(username):     #This function is used to get the info about the likes of a post of the user
    media_id = get_media_id(username)
    response = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (response)
    r = requests.post(response, payload).json()
    if r['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

#========================================================================================================================

def Comment_on_post(username):       #This function is used to get the info about the comments of a post of the user
    media_id = get_media_id(username)
    comment = raw_input("Enter your Comment")
    response = (BASE_URL + 'media/%s/comments') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN,'text':comment}
    print 'POST request url : %s' % (response)
    r = requests.post(response, payload).json()
    if r['meta']['code'] == 200:
        print 'Comment was successful!'
    else:
        print 'Your Comment was unsuccessful. Try again!'


#=======================================================================================================================

def Delete_comment(username):     #This function is used to delete the negative comments on a post of the user
    media_id = get_media_id(username)
    response = requests.get("%smedia/%s/comments?access_token=%s" % (BASE_URL,media_id,APP_ACCESS_TOKEN)).json()
    if response['meta']['code']==200:
        if len(response['data']):
            for index in range(0,len(response['data'])):
                comt_id = response['data'][index]['id']
                comt_txt = response['data'][index]['text']
                blob = TextBlob(comt_txt, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    response= requests.delete("%smedia/%s/comments/%s?access_token=%s" %(BASE_URL,media_id,comt_id,APP_ACCESS_TOKEN)).json()
                    if response['meta']['code']==200:
                        print "comment deleted"
                    else:
                        print "unable to delete"
                else:
                    print "comment positive"
        else:
            print "thier are no comments on the post"
    else:
        print "The code recive other than 200"






#=======================================================================================================================
repeat =True
while repeat:
    question = input("""what do you want to do ?       
     1. get owner info 
      2. Get recent post of owner 
       3.Get other user info 
        4.Get other user post 
        5.Like on a post
        6.Comments on a post
        7. Delete a post
        0. for Exit""")      #this is used to get the input from the user
    if question == 1:
        owner_info()         #function call
    elif question == 2:
        owner_recent_post()     #function call
    elif question == 3:
        user_name= raw_input("what is the username of the user")
        Otheruser_info(user_name)     #function call
    elif question == 4:
        user_name = raw_input("what is the username of the user")
        Otheruser_recentpost(user_name)     #function call
    elif question == 5:
        user_name = raw_input("what is the username of the user")
        like_on_post(user_name)      #function call
    elif question == 6:
        user_name = raw_input("what is the username of the user")
        Comment_on_post(user_name)     #function call
    elif question == 7:
        user_name = raw_input("what is the username of the user")
        Delete_comment(user_name)     #function call

    elif question == 0:
        exit()          #Exit function is to exit
    else:
        print "wrong input"