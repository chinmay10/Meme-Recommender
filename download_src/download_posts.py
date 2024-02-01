import instaloader
import os
from instaloader import *
import json
import time
# L = instaloader.Instaloader()
# profile = Profile.from_username(L.context, '9gag')
# post_iterator = profile.get_posts()
# with resumable_iteration(
#         context=L.context,
#         iterator=post_iterator,
#         load=lambda _, path: FrozenNodeIterator(**json.load(open(path))),
#         save=lambda fni, path: json.dump(fni._asdict(), open(path, 'w')),
#         format_path=lambda magic: "resume_info_{}.json".format(magic)
# ) as (is_resuming, start_index):
#     for post in post_iterator:
#         L.download_post(post, target=profile.username)
def download_posts():
    L = instaloader.Instaloader()
    profile = Profile.from_username(L.context, '9gag')
    post_iterator = profile.get_posts()
    try:
        post_iterator = profile.get_posts()
        if os.path.exists('resume_info.json'):
            post_iterator.thaw(load_structure_from_file(L.context,'resume_info.json'))
        count = 0
        for post in post_iterator:
            L.download_post(post, target=profile.username)
            count += 1
            if count == 20:
                print('seleeping ....')
                count = 0
                save_structure_to_file(post_iterator.freeze(),'resume_info.json')
                time.sleep(60)
    except Exception as e:
        save_structure_to_file(post_iterator.freeze(),'resume_info.json')
        print(e)


download_posts()


    
    
