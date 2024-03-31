import argparse
import os
from BingImageCreator import ImageGen



bing_cookie = os.environ.get('bing_cookie')
def make_pic_and_save(sentence):
    try:
        # for bing image when dall-e3 open drop this function
        i = ImageGen(bing_cookie,bing_cookie)
        images = i.get_images(sentence)
        new_path = os.path.join("./", 'output')
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        i.save_images(images, new_path)
        return True
    except:
        return 'error'
if __name__ =='__main__':
    make_pic_and_save('跑步的人越来越多')