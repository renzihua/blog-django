# coding:utf-8
import requests,json,urllib

# url = 'http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_pic?page=2'
# url = 'http://apis.baidu.com/txapi/health/health?num=10&page=1'
# url = 'http://apis.baidu.com/showapi_open_bus/channel_news/search_news?channelId=5572a109b3cdc86cf39001db&channelName=%E5%9B%BD%E5%86%85%E6%9C%80%E6%96%B0&title=%E4%B8%8A%E5%B8%82&page=1&needContent=0&needHtml=0'
# 最新的新闻
url = 'http://apis.baidu.com/showapi_open_bus/channel_news/search_news'

# 新闻api的参数
params={
    "channelId":"5572a10bb3cdc86cf39001f8",
    "name":"国内焦点",
    "title":"",
    "page":1,
    "needContent":1,
    "needHtml":1
}

headers = {"apikey":"c6b55e48827139ab2f037594e42a822e"}

result = requests.get(url,headers=headers,params=params)

# 解析为json格式
result_json = json.loads(result.content)

# print result_json.get('showapi_res_body')
# for body in result_json.get('showapi_res_body').get('contentlist'):
#     print body.get('title')
#     file_path = "../uploads/api_img/" + body.get('title')
#     urllib.urlretrieve(url=body.get('img'),filename=file_path)

# 新闻
for body in result_json.get('showapi_res_body').get("pagebean").get('contentlist'):
    print "[段子]", body.get('title'),"_____"
    print body['pubDate']
    print body['imageurls']
    print body['link']
    print body['content']
    # print body['desc']
    # file_path = "../uploads/api_img/" + body.get('title')
    # urllib.urlretrieve(url=body.get('img'),filename=file_path)

# {
#     "channelId": "5572a108b3cdc86cf39001cd",
#     "name": "国内焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001ce",
#     "name": "国际焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001cf",
#     "name": "军事焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d0",
#     "name": "财经焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d1",
#     "name": "互联网焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d2",
#     "name": "房产焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d3",
#     "name": "汽车焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d4",
#     "name": "体育焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d5",
#     "name": "娱乐焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d6",
#     "name": "游戏焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d7",
#     "name": "教育焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d8",
#     "name": "女人焦点"
# },
# {
#     "channelId": "5572a108b3cdc86cf39001d9",
#     "name": "科技焦点"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001da",
#     "name": "社会焦点"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001db",
#     "name": "国内最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001dc",
#     "name": "台湾最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001dd",
#     "name": "港澳最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001de",
#     "name": "国际最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001df",
#     "name": "军事最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001e0",
#     "name": "财经最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001e1",
#     "name": "理财最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001e2",
#     "name": "宏观经济最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001e3",
#     "name": "互联网最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001e4",
#     "name": "房产最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001e5",
#     "name": "汽车最新"
# },
# {
#     "channelId": "5572a109b3cdc86cf39001e6",
#     "name": "体育最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001e7",
#     "name": "国际足球最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001e8",
#     "name": "国内足球最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001e9",
#     "name": "CBA最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001ea",
#     "name": "综合体育最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001eb",
#     "name": "娱乐最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001ec",
#     "name": "电影最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001ed",
#     "name": "电视最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001ee",
#     "name": "游戏最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001ef",
#     "name": "教育最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001f0",
#     "name": "女人最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001f1",
#     "name": "美容护肤最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001f2",
#     "name": "情感两性最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001f3",
#     "name": "健康养生最新"
# },
# {
#     "channelId": "5572a10ab3cdc86cf39001f4",
#     "name": "科技最新"
# },
# {
#     "channelId": "5572a10bb3cdc86cf39001f5",
#     "name": "数码最新"
# },
# {
#     "channelId": "5572a10bb3cdc86cf39001f6",
#     "name": "电脑最新"
# },
# {
#     "channelId": "5572a10bb3cdc86cf39001f7",
#     "name": "科普最新"
# },
# {
#     "channelId": "5572a10bb3cdc86cf39001f8",
#     "name": "社会最新"
# }
