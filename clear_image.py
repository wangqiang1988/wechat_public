import requests
import json
import os

def get_token():

    headers = {
    'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
}
    params = (
    ('grant_type', 'client_credential'),
    ('appid', os.environ.get('wechat_app_id')),
    ('secret', os.environ.get('wechat_app_secret')),
)
    response = requests.get('https://api.weixin.qq.com/cgi-bin/token', headers=headers, params=params)
    return response.json()['access_token']

def delete_image():
    token = get_token()
    headers = {
    'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
    'Content-Type': 'application/json',
}

    params = (
    ('access_token', token),
)
    data = { "type":'image', "offset":'0', "count":'20' }
    response = requests.post('https://api.weixin.qq.com/cgi-bin/material/batchget_material', headers=headers, params=params, json=data)
    response_all_image = requests.get('https://api.weixin.qq.com/cgi-bin/material/get_materialcount', headers=headers, params=params)
    print('总素材数:',response_all_image.json())
    for media_id in response.json()['item']:
        print(media_id['name'])
        data = { 'media_id':media_id['media_id']}
        response = requests.post('https://api.weixin.qq.com/cgi-bin/material/del_material', headers=headers, params=params,json=data)

        
#每次最多列20张，需要多次循环删除20*n张
i = 0
while True:
    if i < 20:
        delete_image()
        i +=1
    else:
        print("finshed")
        break