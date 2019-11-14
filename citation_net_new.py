# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 22:35:34 2019 @author: D-pc
"""
import networkx as nx
from multiprocessing.pool import Pool
from functools import partial
import csv

class Citation_index(object):
    
    def __init__(self, filepath):
        self.path = filepath
        self.G = nx.DiGraph()
        
    def read_file(self):
        '''读取文件'''
        with open(self.path, 'r', encoding='utf-8-sig') as f:
            content = f.readlines()
        return content
    
    def creat_pair(self, content):
        '''处理节点对'''
        for i in content:
            item = i.strip().replace('\n', '')
            item = item.split('\t')
            if len(item) != 2:
                return
            else:
                yield tuple(item)
                
    def add_edge(self, pair):
        '''添加边关系'''
        self.G.add_edge(*pair)
        
    def get_final_nodes(self):
        '''获取所有的终结点'''
        final_nodes = []
        for i in self.G.out_degree:
            if i[1] == 0:
                final_nodes.append(i[0])
        return final_nodes 
       
    def iter_path(self, start, end, path):
        '''递归查找路径'''
        path = path + [start]
        if start == end:
            return [path]
        else:
            paths = []
            for node in self.G.successors(start):
                if node not in path:
                    newpaths = self.iter_path(node, end, path)
                    for newpath in newpaths:
                        paths.append(newpath)
        return paths
    
    def save(self, name, result):
        with open('{}.csv'.format(name),'a', newline='') as w:
            for line in result:
                writer = csv.writer(w)
                writer.writerow(line)
#                w.write(str(line)+'\n')
            
def main(patent,cit, nodes):
    matrix = [] # 创建所有路径保存列表
    for each_node in nodes: # 遍历终结点
        allpath = cit.iter_path(patent, each_node, path=[])
        matrix =matrix + allpath
    max_len = max((len(l) for l in matrix))
    new_matrix = list(map(lambda l: l + ['null'] * (max_len - len(l)), matrix))
    new_matrix.insert(0, ['Gen'+str(j) for j in range(max_len)])
    cit.save(patent, new_matrix)
    return '节点-{} is done'.format(patent)
            
if __name__ == '__main__':
    filepath = r'test1.txt' # 节点关系路径
    cit = Citation_index(filepath) # 类实例化
    contents = cit.read_file() # 读取全部节点文件
    print('读取节点完毕')
    for each in cit.creat_pair(contents): # 读取节点关系对
        cit.add_edge(each)
    print('添加边关系完毕')
    nodes = cit.get_final_nodes() # 获取所有的终结点
    targets = []
    with open(r'target1.txt', 'r') as f: # 获取目标节点
        for element in f:
            targets.append(element.replace('\n', ''))
    print('读取目标节点完毕')
    new_main = partial(main, cit=cit, nodes=nodes) # 扩展main的功能，增加固定参数
    pool = Pool()
    results = pool.map(new_main, targets)
    for result in results:
        print(result)
    pool.close()
    pool.join()
            
            