import argparse
import os
from BingImageCreator import ImageGen



bing_cookie = os.environ.get('bing_cookie')
bing_user = os.environ.get('bing_user')
def make_pic_and_save(sentence):
    try:
        print(bing_cookie)
        # for bing image when dall-e3 open drop this function
        i = ImageGen(bing_cookie,bing_user)
        images = i.get_images(sentence)
        new_path = os.path.join("./", 'output')
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        i.save_images(images, new_path)
        return True
    except Exception as e:
        return e
if __name__ =='__main__':
    make_pic_and_save('跑步的人越来越多')