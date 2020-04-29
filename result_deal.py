# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:18:19 2019 @author: D-pc
"""
import pandas as pd
import numpy as np
import csv
import os
from collections import OrderedDict

class Count(object):
    # 格式化参数
    def __init__(self, data):
        self.df = data
    
    # 判断是否有被引
    def flage(self):
        return len(self.df.columns)
    
    # 获取目标专利号
    def get_target(self):
        return self.df.loc[0, 'Gen0']
    
    # 获取引证路径长度
    def get_length(self):
        return len(self.df.loc[0])-1
    
    # 获取直接被引频次
    def direct_cit(self):
        return len(set(self.df['Gen1']))
    
    # 获取目标专利每代的引证频次
    def get_relation(self, length):
        detail = OrderedDict()
        for i in range(length):
            col_data = self.df.iloc[:, [i, i+1]]
            lst = []
            for index,row in col_data.iterrows():
                if np.nan in list(row):
                    continue
                else:
                    if list(row) not in lst:
                        lst.append(list(row))
            detail[i+1] = len(lst)
        return detail

    # 获取专利总数、每代的专利数
    def get_amount(self):
        all_p = []
        per_p = OrderedDict()
        for index, row in self.df.iteritems():
            for each in set(row):
                if each is np.nan:
                    continue
                elif each not in all_p:
                    all_p.append(each)
            if np.nan in set(row):
                per_p[index] = len(set(row))-1
            else:
                per_p[index] = len(set(row))
        return len(all_p), per_p

    # 计算累积引证指数
    def cumulative_index(self, detail, length):
        weight_ind = 0
        no_weight_ind = 0
        for key, value in detail.items():
            weight_ind += (length+1-key)/length * value
            no_weight_ind += value
        return weight_ind, no_weight_ind
        
    # 获取子代中每个专利的直接被引频次
    def per_direct_cit(self, length):
        per_detail = {}
        for j in range(1, length):
            col_data1 = self.df.iloc[:, [j, j+1]]
            for index,row in col_data1.iterrows():
                if np.nan in list(row):
                    continue
                else:
                    per_detail.setdefault(list(row)[0], 
                                          []).append(list(row)[1])
        for k, v in per_detail.items():
            per_detail[k] = len(set(v))
        con = sorted(per_detail.items(), key=lambda x:int(x[1]),reverse=True)
        # con = zip(order_per_detail.keys(), order_per_detail.values())
        return con

    # 保存基本信息
    def save(self, order, num, patent, length, 
             direct, amount, weight_ind, no_weight):
        datas = []
        datas.append(patent) #保存专利号
        datas.append(length) #保存引证长度
        datas.append(direct) #保存直接被引频次
        datas.append(amount) #保存专利总数
        datas.append(weight_ind) #保存累积被引指数
        datas.append(no_weight) #保存总被引数
        with open(r'C:\files\专利引用数据处理 -新处理\详细结果_1.csv', 
                  'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(datas)
            print('{} of {} -{} 保存成功'.format(order, num, patent))
    
    #保存每代被引频次
    def save_detail(self, order, num, patent, per_gen_value):
        per_gen_value.insert(0, patent)
        with open(r'C:\files\专利引用数据处理 -新处理\每代被引频次.csv', 
                  'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(per_gen_value)
            print('{} of {} -{} 保存成功'.format(order, num, patent))
    
    #保存每代专利数
    def save_patent_amount(self, order, num, patent, per_gen_amount):
        per_gen_amount.insert(0, patent)
        with open(r'C:\files\专利引用数据处理 -新处理\每代专利数.csv', 
                  'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(per_gen_amount)
            print('{} of {} -{} 保存成功'.format(order, num, patent))
    
    #保存子代专利的被引频次
    def save_child_patent_cit(self, order, num, patent, con_data):
        with open(r'C:\files\专利引用数据处理 -新处理\子专利被引频次_1.csv', 
                  'a', newline='') as f:
            writer = csv.writer(f)
            for i in con_data:
                writer.writerow(list(i))
            print('{} of {} -{} 保存成功'.format(order, num, patent))
    
def main(order, num, file):
    data = pd.read_csv(file, dtype=str)  #读取dataframe
    count = Count(data)   #实例化
    patent = count.get_target()      #获取目标专利号
    if count.flage() > 1: #判断专利是否被引
        # length = count.get_length()      #获取引证路径长度
        # direct = count.direct_cit()      #获取直接被引频次
        # frequency_detail = count.get_relation(length)    #获取每代的被引频次
        # weight, no_weight = count.cumulative_index(frequency_detail, length) #计算累积被引指标
        all_amount, per_amount = count.get_amount()      #获取专利总数和每代的专利数
        # count.save_detail(order, num, patent, list(frequency_detail.values()))
        # con_data = count.per_direct_cit(length) #计算子代专利的直接被引频次
        # count.save(order, num, patent, length, direct, amount, weight, no_weight) #保存处理结果
        count.save_patent_amount(order, num, patent, list(per_amount.values()))
        # count.save_child_patent_cit(order, num, patent, con_data)
    else:
        # count.save(order, num, patent, 0, 0, 0, 0, 0) #保存处理结果
        print(patent, '没有被引')
        
        
if __name__ == '__main__':
    path = r'C:\files\专利引用数据处理 -新处理\超算结果'
    num = len(os.listdir(path))
    print('开始计算……')
    for order, each_csv in enumerate(os.listdir(path)):
        main(order+1, num, os.path.join(path, each_csv))
    print('计算结束!')




