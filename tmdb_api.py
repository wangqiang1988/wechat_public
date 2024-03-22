from tmdbv3api import TMDb
from tmdbv3api import Movie,TV
import os
import json
from werobot import WeRoBot
import requests
import argparse

tmdb = TMDb()
tmdb.language = 'zh-CN'
tmdb.api_key = os.environ.get('tmdb_api_key')
movie = Movie()
tv = TV()
def Client():
    robot = WeRoBot()
    robot.config["APP_ID"] = os.environ.get('wechat_app_id')
    robot.config["APP_SECRET"] = os.environ.get('wechat_app_secret')
    client = robot.client
    token = client.grant_token()
    return client, token

def search_tmdb(type,name):
    poster_path_list = []
    content_list=[]
    print('search_tmdb',type,name)
    i = 0
    if type == '电影':
        search = movie.search(name)
        if search['total_results'] == 0:
            imgurl = 'http://saqnq6fvz.hb-bkt.clouddn.com/014109558a3f8b000000b18f00adbf.jpg%401280w_1l_2o_100sh.jpg'
            return imgurl
        for res in search:
            if i == 1:
                break
            print('tmdbid:',res.id)
            print('语言:',res.original_language)
            print('tmdb评分:',res.vote_average)
            print('上映日期:',res.release_date)
            print('内容介绍:',res.overview)
            imgurl = 'https://image.tmdb.org/t/p/original'+ res.poster_path
            poster_path_list.append(imgurl)
            content= 'tmdbid:'+str(res.id) + '<br>' + '语言:'+str(res.original_language) + '<br>' + 'tmdb评分:'+ str(res.vote_average) + '<br>' + '上映日期:'+ str(res.release_date) + '<br>' + '内容介绍:'+'<br>'+ res.overview + '<br><br>'
            content_list.append(content)
            if name == res.title:
                i = 1
            else:
                i = 0
                imgurl = poster_path_list[0]
                content = content_list[0]
    
    
    elif type == '电视剧':
        show = tv.search(name)
        if show['total_results'] == 0:
            imgurl = 'http://saqnq6fvz.hb-bkt.clouddn.com/014109558a3f8b000000b18f00adbf.jpg%401280w_1l_2o_100sh.jpg'
            return imgurl
        for result in show:
            if i == 1:
                break
#            print(result.name)
            print('tmdbid:',result.id)
            print('语言:',result.origin_country[0])
            print('tmdb评分:',result.vote_average)
            print('上映日期:',result.first_air_date)
            print('内容介绍:',result.overview)
            imgurl = 'https://image.tmdb.org/t/p/original'+ result.poster_path
            poster_path_list.append(imgurl)
            content = content= 'tmdbid:'+str(result.id) + '<br>' + '语言:'+str(result.origin_country[0]) + '<br>' + 'tmdb评分:'+str(result.vote_average) + '<br>' + '上映日期:'+str(result.first_air_date) + '<br>' + '内容介绍:'+'<br>'+result.overview + '<br><br>'
            content_list.append(content)
            if name == result.name:
                i = 1
            else:
                i = 0 
                imgurl = poster_path_list[0]
                content = content_list[0]
    else:
        '没有搜索到'
    return imgurl,content


def down_img(img_url):
    response_img = requests.get(img_url)
    with open('tmdb_img.jpg', 'wb') as f:
        f.write(response_img.content)

def upload_image():
    #上传图片到公众号素材库
    media_json = client.upload_permanent_media("image",open('tmdb_img.jpg', "rb")) ##永久素材
    media_id = media_json['media_id']
    media_url = media_json['url']
    print('upload_success')
    return media_id ,media_url

def upload_wechat_news(token,content,thumb,title):
    #上传到草稿未发表
    AUTHOR = '电影小助手'
    articles = {
        'articles':
        [   
            {   
                "title": 'up推荐-'+title,
                "thumb_media_id": thumb,
                "author": AUTHOR,
                "digest": '电影推荐',
                "show_cover_pic": 0,
                "content": content,
                "need_open_comment":1,
            }
            # 若新增的是多图文素材，则此处应有几段articles结构，最多8段
        ]
    }


    headers={'Content-type': 'text/plain; charset=utf-8'}
    datas = json.dumps(articles, ensure_ascii=False).encode('utf-8')
    postUrl = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=%s" % token['access_token']
    r = requests.post(postUrl, data=datas, headers=headers)
    resp = json.loads(r.text)
    return resp

def publish(token,media_id):
    headers={'Content-type': 'text/plain; charset=utf-8'}
    postUrl = "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=%s" % token['access_token']
    articles = {
        'media_id':media_id,
    }
    datas = json.dumps(articles, ensure_ascii=False).encode('utf-8')
    r = requests.post(postUrl, data=datas, headers=headers)
    resp = json.loads(r.text)
    return resp


if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("title", help="名称")
    parser.add_argument("type", help="影视类型")
    parser.add_argument("publish",help="发布yes/no")
    options = parser.parse_args()
    title = options.title
    type = options.type
    client, token = Client()
    imgurl,content = search_tmdb(type,title)
    down_img(imgurl)
    filename = imgurl.split('/')[-1]
    media_id ,media_url = upload_image()
    wechat_content ='名称:'+ title + '<br>'+"<img src='%s'"%str(media_url)+ "/>" +'<br>' + content + '<br>'
    news_id = upload_wechat_news(token,wechat_content,media_id,title)
    if options.publish == 'yes':
        publish(token,news_id['media_id'])
    else:
        pass