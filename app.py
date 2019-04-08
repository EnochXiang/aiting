from flask import Flask, request
import json
import hashlib
import requests
import time
import zipfile


# API token config
def get_Token():
    """
    get aiting oauth token
    :return:
    """
    oauth_consumer_key = 'SHMusicClient'
    oauth_consumer_secret = 'f3a210f900f44e19be03555609cfcd76'
    clientid = 'LinuxClient'
    clientsecret = 'ZC001'
    oauth_consumer_sig = hashlib.md5((oauth_consumer_key+clientid+clientsecret+oauth_consumer_secret).encode("utf-8")).hexdigest()

    url = 'https://csmeta.tingmall.com/ContentServiceWS/OAuth/getAccessTokenSig'+'?oauth_consumer_key='+oauth_consumer_key+'&oauth_consumer_sig='+oauth_consumer_sig+'&clientid='+clientid+'&clientsecret='+clientsecret
    res = requests.get(url=url).json()
    token_secret = res['response']['docs']['token_secret']
    refresh_token = res['response']['docs']['refresh_token']
    access_token = res['response']['docs']['access_token']
    return token_secret,refresh_token,access_token


headers = {'token_secret':get_Token()[0], 'oauth_token':get_Token()[2]}


def timestamp_datetime(value):
    """
    translate timestamp to datetime
    :param value:timestamp
    :return:datetime
    """
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt


def datetime_timestamp(dt):
    """
    translate datetime to timestamp
    :param dt: datetime
    :return: timestamp
    """
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return str(int(s))


def get_NewData(type,time):
    """
    返回time时间段之后更新的数据
    :param type:['artist', 'song', 'album', 'songlistV2', 'verifyArtist', 'verifySong', 'verifyAlbum', 'verifySonglist',
            'songHot']
    :param time:timestamp
    :return:new data
    """
    a = datetime_timestamp(time)
    data = {'time': a}
    url2 = 'https://csmeta.tingmall.com/ContentServiceWS/MetaInfo/'+type
    res2 = requests.post(url=url2, headers = headers, data=data).json()
    return res2


app = Flask(__name__)


@app.route('/combine', methods=['POST','GET'])
def combine():
    """
    get time value from url, get new data from timestamp to now, combine all type data.
    :return: new data include all types.
    """
    # timeStamp = request.args.get('time')
    # timeStamp = params['time']
    timeStamp = request.form['time']
    type = ['artist', 'song', 'album', 'songlistV2', 'verifyArtist', 'verifySong', 'verifyAlbum', 'verifySonglist',
            'songHot']
    res = []
    for i in type:
        data = get_NewData(type=i, time=timeStamp)
        res.append({i:data})
    res = json.dumps(res)
    return res


@app.route('/ArtistInfo/getArtistInfoFiltered', methods=['POST','GET'])
def getArtistInfoFiltered():
    """
    根据过滤条件包含姓氏拼音字母，性别，地区等来取得歌手的相关讯息。歌手列表顺序根据热度值排序。
    :return:
    """
    url = 'https://csapi.tingmall.com/ContentServiceWS/ArtistInfo/getArtistInfoFiltered'
    res = requests.post(url=url, headers=headers)
    if res.content:
        res = json.dumps(res.json())
    return res


@app.route('/ArtistInfo/getArtistInfo', methods=['POST','GET'])
def getArtistInfo():
    """
    根据歌手id获取上架歌手信息
    :return:
    """
    artistid = request.form['artistid']
    data = {'artistid': artistid}
    url = 'https://csapi.tingmall.com/ContentServiceWS/ArtistInfo/getArtistInfo'
    res = requests.post(url=url, headers=headers, data=data)
    if res.content:
        res = json.dumps(res.json())
    return res


@app.route('/AggregateSearch/aggregateSearch', methods=['POST','GET'])
def aggregateSearch():
    """
    根据用户输入的搜索词(歌曲名，歌手名，专辑名)来获取歌曲，歌手及专辑的讯息。并且可以支持拼音首字母搜索。
    查询歌曲时，关键字会只查歌曲字段。
    查询专辑时，关键字会只查专辑字段。
    查询歌手时，关键字会只查歌手字段。
    备注:对于不用到的参数请勿解析读取，后期会
    对一些无用多余的字段做清除!
    :return:
    """
    data = {'searchvalue': request.form['searchvalue']}
    url = 'https://csapi.tingmall.com/ContentServiceWS/AggregateSearch/aggregateSearch'
    res = requests.post(url=url, data=data, headers=headers)
    if res.content:
        res = json.dumps(res.json())
    return res


@app.route('/ContentFileInfo/getLyricURL', methods=['POST', 'GET'])
def getLyricURL():
    """
    获取歌词url
    :return:
    """
    data = {'itemid': request.form['itemid'], 'subitemtype': request.form['subitemtype']}
    url = 'https://csapi.tingmall.com/ContentServiceWS/ContentFileInfo/getLyricURL'
    res = requests.post(url=url, data=data, headers=headers)
    if res.content:
        res = json.dumps(res.json())
    return res


@app.route('/CategoryExInfo/getCategoryGroup', methods=['POST', 'GET'])
def getCategoryGroup():
    """
    获取一级分类信息
    :return:
    """
    url = 'https://csapi.tingmall.com/ContentServiceWS/CategoryExInfo/getCategoryGroup'
    res = requests.post(url=url, headers=headers)
    if res.content:
        res = json.dumps(res.json())
    return res


@app.route('/CategoryExInfo/getCategoryMenu', methods=['POST', 'GET'])
def getCategoryMenu():
    """
    根据一级分类mccode获取二级分类列表
    :return:
    """
    data = {}
    if 'categoryid' in request.form.keys():
        data['categoryid'] = request.form['categoryid']
    if 'categorycode' in request.form.keys():
        data['categorycode'] = request.form['categorycode']
    url = 'https://csapi.tingmall.com/ContentServiceWS/CategoryExInfo/getCategoryMenu'
    res = requests.post(url=url, data=data, headers=headers)
    if res.content:
        res = json.dumps(res.json())
    return res


@app.route('/CategoryExInfo/getCategoryStation', methods=['POST', 'GET'])
def getCategoryStation():
    """
    根据二级分类代码(Genre.MCCode)来取得分类内容列表。
    :return:
    """
    data = {}
    if 'categoryid' in request.form.keys():
        data['categoryid'] = request.form['categoryid']
    if 'categorycode' in request.form.keys():
        data['categorycode'] = request.form['categorycode']
    url = 'https://csapi.tingmall.com/ContentServiceWS/CategoryExInfo/getCategoryStation'
    res = requests.post(url=url, data=data, headers=headers)
    if res.content:
        res = json.dumps(res.json())
    return res




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8222)
