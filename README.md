# wechat_public
发布一个公众号文章到草稿箱或者发布

# main是发布公众号程序
他会将你所发布的标题作为bingimage生成一张图片，并选择一张作为封面和内容图片,生成公众号文章草稿

用法:python main.py 标题 简介 yes/no
环境变量设置公众号app_id、app_secret
robot.config["APP_ID"] = os.environ.get('plog_wechat_app_id')
robot.config["APP_SECRET"] = os.environ.get('plog_wechat_app_secret')

## plog是bingimage生成的图片
bing_cookie,bing_user请参考acheong08/BingImageCreator

# clear_image是删除素材库图片程序
用法:python clear_image.py

# tmdb
用法:python tmdb.py 幸运汉克 电视剧 no 
发布公众号格式为：

名称
宣传图
影视信息
简介
剧照


