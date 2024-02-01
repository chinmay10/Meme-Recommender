import instaloader
import os
from instaloader import *
import json
import time
import pickle
import sys

def change_user(L):
    global cur, users, pswds, user_pswd
    try:
        cur = (cur+1)%len(users)
        user_pswd['cur'] = cur
        L.login(users[cur], pswds[cur])
        print(f"User {users[cur]} logged in")
        
    except Exception as e:
        print(e)
        print(f"Failed logging {users[cur]}")
        L = instaloader.Instaloader()
    return L

def login_first_user(L):
    global cur, users, pswds, user_pswd
    with open('resume_info.json','r') as file:
        info = json.load(file)
    user = info['node']['context_username']
    uid = users.index(user)
    try:
        L.login(users[uid], pswds[uid])
    except Exception as e:
        print(e)
        print(f"Failed logging {users[cur]}")
        L = instaloader.Instaloader()
    return L

    

    

def download_posts():
    L = instaloader.Instaloader()
    profile = Profile.from_username(L.context, '9gag')
    post_iterator = profile.get_posts()
    L = login_first_user(L)
    if os.path.exists('resume_info.json'):
        post_iterator.thaw(load_structure_from_file(L.context,'resume_info.json'))
    count = 0
    for post in post_iterator:
        if count > 0 and count % 20 == 0:
            save_structure_to_file(post_iterator.freeze(),'resume_info.json')
            L = change_user(L)
        if count > 0 and count % 100==0:
            time.sleep(120)
        try:
            result = L.download_post(post, target=profile.username)
            if result:
                print(f"downloaded {count}")
                count +=1
                time.sleep(1)
        except Exception as e:
            print("Unable to download for post: "+post.shortcode.lower())
            print(e)
            save_structure_to_file(post_iterator.freeze(),'resume_info.json')
            sys.exit(1)
                
    
if __name__ == '__main__':
    with open("ig_credentials.pkl", "rb") as file:
    # Load the dictionary from the file
        user_pswd = pickle.load(file)
    cur = user_pswd['cur']
    users = user_pswd['users']
    pswds = user_pswd['pswd']
    download_posts()


    
