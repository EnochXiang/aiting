#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： json2csv.py
#   @Author：    Enoch.Xiang
#   @contact：   xiangwenzhuo@yeah.net 
#   @date：      2019/4/2 下午4:04
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------

from pandas import DataFrame as df
import numpy as np
import os
import simplejson
import re
import pandas as pd
import json


path = '/users/cnuvv/desktop/singers/'
name = os.listdir(path)
name.remove('.DS_Store')
# print(len(name))
# print(name[146])

# for i in name:
def showdata(i):
    a = re.split('_|.json', i)
    num1 = int(a[1])
    num2 = int(a[2])
    num3 = int(a[3])
    # f = open(path+i, encoding='utf-8')
    with open(path+i, 'r') as f:
        file = simplejson.load(f, strict=False)
    data = df(file['hotlist'])
    one = np.ones((len(data), 1))
    area = one * num1
    genre = one * num2
    sex = one * num3
    data.insert(0, 'area', area)
    data.insert(1, 'genre', genre)
    data.insert(2, 'sex', sex)
    return data


# df1 = []
# # print(df1)
# for i in name:
#     # print(i)
#     df1.append(showdata(i))
# df2 = pd.concat(df1)
# df.to_csv(df2, path_or_buf='/users/cnuvv/desktop/singes.csv')



# data = df(data=file['hotlist'][0], index=['a', 'b', 'c', 'd'], columns=['one', 'two', 'three', 'four'])


# print(data)

# with open(path+'artists_4_8_3.json', 'r') as f:
#     file = json.load(f,strict=False)