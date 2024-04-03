import requests 
import json  
from werobot import WeRoBot
import os
import argparse
import datetime
import plog
import env
def Client():
    #初始化
    robot = WeRoBot()
    robot.config["APP_ID"] = os.environ.get('plog_wechat_app_id')
    robot.config["APP_SECRET"] = os.environ.get('plog_wechat_app_secret')
    client = robot.client
    token = client.grant_token()
    return client, token

def Client_m():
    #初始化
    robot = WeRoBot()
    robot.config["APP_ID"] = os.environ.get('wechat_app_id')
    robot.config["APP_SECRET"] = os.environ.get('wechat_app_secret')
    client = robot.client
    token = client.grant_token()
    return client, token

def file_is_larger_than_10k(file_path):
    file_size = os.path.getsize(file_path)
    return file_size > 10240
def freechat(prompt):
    headers = {
    'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
    'Authorization': 'Bearer %s'%os.environ.get('gpt_free_api'),
    'Content-Type': 'application/json',
    }

    data = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"revise `{prompt}` to a DALL-E prompt"}]
    })
    response = requests.post('https://api.chatanywhere.com.cn/v1/chat/completions', headers=headers, data=data) 
    dalle_prompt = json.loads(response.text)['choices'][0]['message']['content']
    return dalle_prompt

def getBingImg():
    try:
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            # 不是必须
        }
 
        response = requests.get("https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7&mkt=zh-CN",
                                headers=headers,  # 请求头
                                timeout=3,  # 设置请求超时时间
                                )
        response = json.loads(response.text)  # 转化为json
        imgList = []
        for item in response['images']:
            imgList.append({
                'copyright': item['copyright'],  # 版权
                'date': item['enddate'][0:4] + '-' + item['enddate'][4:6] + '-' + item['enddate'][6:],  # 时间
                'urlbase': 'https://cn.bing.com' + item['urlbase'],  # 原始图片链接
                'url': 'https://cn.bing.com' + item['url'],  # 图片链接
            })
        return imgList  # 返回一个数据数组
    except:
        return False
 
def upload_img(image):
    #response_img = requests.get(img_url)
   # with open('./output/0.jpeg', 'wb') as f:
    #    f.write(response_img.content)
    media_json = client.upload_permanent_media("image",open('/home/ubuntu/github/wechat_public/output/%s'%image, "rb")) ##永久素材
    media_id = media_json['media_id']
    media_url = media_json['url']
    print('upload_success')
    return media_id ,media_url

def upload_imagelist():
    """
    上传到微信公众号素材
    """
    media_url_p = []
    media_id_p = []
    for filename in sorted(os.listdir('/home/ubuntu/github/wechat_public/output')):
        if file_is_larger_than_10k('/home/ubuntu/github/wechat_public/output/%s'%filename):
            media_json_p = client.upload_permanent_media("image",open('/home/ubuntu/github/wechat_public/output' + '/'+  str(filename), "rb")) ##永久素材
            media_id_p.append(media_json_p['media_id'])
            media_url_p.append(media_json_p['url'])
            print('upload ',filename)
        else:
            pass
            
    THUMB_MEDIA_ID_p = media_id_p[0]
    RESULT_p = ''
    for img in media_url_p:
        RESULT_p += "<img src='%s'"%str(img)+ "/>" +'<br><br>' 
    return THUMB_MEDIA_ID_p,RESULT_p


def upload_wechat_news(title,media_id,disgest,media_url,token):
    #上传到草稿未发表
    AUTHOR = '王同学'
    articles = {
        'articles':
        [   
            {   
                "title": title,
                "thumb_media_id": media_id,
                "author": AUTHOR,
                "digest": disgest,
                "show_cover_pic": 0,
            #    "content": "<img src='%s'"%media_url+"/>" +'<br>' + '<p>'+ media_content +'</p>'+ '<br>',
                "content": media_url ,
                "need_open_comment":0,
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

def get_time():
    current_time = datetime.datetime.now().strftime('%Y%m%d')
    return current_time

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("wechat_title", help="公众号标题")
    parser.add_argument("wechat_disgest", help="文章简介")
    parser.add_argument("publish", help="是否发布,yes/no")
    options = parser.parse_args()
    bing_cookie = env.bing_cookie()
    dalle_prompt = freechat(options.wechat_title)
    res = plog.make_pic_and_save(bing_cookie,dalle_prompt)
    try:
        thum_id, media_url = upload_imagelist()
    except:
        thum_id, media_url = upload_imagelist()
    news_id = upload_wechat_news( current_time + '-'+ options.wechat_title,thum_id,options.wechat_disgest,media_url,token)
    if options.publish == 'yes':
        publish(token,news_id['media_id']) #发布
    else:
        pass

if __name__ == '__main__':
    current_time = get_time()
    client, token = Client()
    main()
    client, token = Client_m()
    main()
    os.system('mv /home/ubuntu/github/wechat_public/output /home/ubuntu/github/wechat_public/%s'%current_time)