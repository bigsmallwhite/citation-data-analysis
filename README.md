## 构建引文网络

读取节点对，通过python的networkx包生成有向网络图

## 获取引文路径

选取目标节点，即可遍历其在网络中的所有前向网络路径（list形式）

采用多线程，可以同时查询多个目标节点的前向网络

## 计算网络拓扑参数

通过pandas读取并计算每个目标专利引文网络的拓扑参数

