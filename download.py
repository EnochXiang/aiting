#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： download.py
#   @Author：    Enoch.Xiang
#   @contact：   xiangwenzhuo@yeah.net 
#   @date：      2019/4/2 下午2:23
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------

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


def singer():
    """
    获取歌手各个分类的歌手信息 ，singer/artists_{area}_{genre}_{sex}.zip
    :param params:
    area:0(全部),1(华语),2(韩国 ),3(日本),4(欧美),5(其 它),6(港台),7(日韩)。 参数是放在接口名的第 一个0上
    genre:0(全部),1(流行),2(嘻哈 ),3(摇滚),4(电子),5(民 谣),6(R&B),7(民歌),8(轻 音乐),9(爵士),\
          10(古典 ),11(乡村),12(蓝调) 参数是放在接口名的第 二个0上
    sex:0(全部),1(男),2(女),3(组 合) 参数是放在接口名的第 三个0上
    :return:
    """
    headers = {
        'token_secret':get_Token()[0],
        'oauth_token':get_Token()[2]
    }
    # data = {
    #     'area': request.form['area'],
    #     'genre': request.form['genre'],
    #     'sex': request.form['sex']
    # }

    # url = 'https://csimage.tingmall.com/singer/artists_'+ data['area']+'_'+data['genre']+'_'+data['sex']+'.zip'
    # url = 'https://csimage.tingmall.com/singer/artists_0_0_0.zip'
    # data = json.dumps(data)
    for i in [0,1,2,3,4,5,6,7]:
        for j in [0,1,2,3,4,5,6,7,8,9,10,11,12]:
            for k in [0,1,2,3]:
                file_name = 'artists_'+str(i)+'_'+str(j)+'_'+str(k)+'.zip'
                url = 'https://csimage.tingmall.com/singer/'+file_name
                res = requests.get(url=url, headers=headers, stream=True)
                f = open(file_name, "wb")
                for chunk in res.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
                f.close()
    return json.dumps(headers)


# singer()


def unzip_file(zip_src):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file)
    else:
        print('This is not zip')
