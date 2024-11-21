import json
from collections import defaultdict

import networkx as nx

from util.file_util import FileUtil

import json
from collections import defaultdict


def write_neighbor_vector_groups_to_file(neighbor_vector_groups, file_path):
    """
    将邻域向量组写入 JSON 文件。

    :param neighbor_vector_groups: 邻域向量组的字典
    :param file_path: 输出文件的路径
    """
    # 将 defaultdict 转换为普通字典，以便 json 序列化
    neighbor_vector_groups_dict = {str(degree): {str(vector): nodes for vector, nodes in groups.items()} for
                                   degree, groups in neighbor_vector_groups.items()}

    with open(file_path, 'w') as f:
        json.dump(neighbor_vector_groups_dict, f, indent=4)

    print(f"Results written to '{file_path}'")


### 读取文件的方法
def read_neighbor_vector_groups_from_file(file_path):
    """
    从 JSON 文件读取邻域向量组。

    :param file_path: 输入文件的路径
    :return: 邻域向量组的字典
    """
    with open(file_path, 'r') as f:
        neighbor_vector_groups_dict = json.load(f)

    # 将字符串键转换回整数和元组
    neighbor_vector_groups = {}
    for degree_str, groups in neighbor_vector_groups_dict.items():
        degree = int(degree_str)
        neighbor_vector_groups[degree] = {}
        for vector_str, nodes in groups.items():
            vector = tuple(map(int, vector_str.strip('()').split(', ')))
            neighbor_vector_groups[degree][vector] = nodes

    return neighbor_vector_groups

if __name__ == '__main__':

    domain_map = FileUtil.read_json_from_file('domain_map_to_number_map.json')
    # print("domain_map:", len(domain_map))
    G = nx.Graph()
    edges = []
    for key, value in domain_map.items():
        for item in value:
            edges.append((key, item))
    G.add_edges_from(edges)

    nodes = G.nodes()
    neighbor_vectors = {}
    for node in domain_map.keys():
        # 获取节点的邻居
        neighbors = set(G.neighbors(node))
        # 初始化邻域向量
        vector = [1 if n in neighbors or n == node else 0 for n in nodes]
        # 将向量存储到字典中
        neighbor_vectors[node] = vector

    # for key in sorted(neighbor_vectors.keys(), key = int):
    #     print(f"Node {key}: {neighbor_vectors[key]}")
    # FileUtil.write_json_to_file(neighbor_vectors, 'test.json')
    # print("neighbor_vectors:", len(neighbor_vectors))

    # 按照节点度进行分组
    degree_groups = defaultdict(list)
    for node in domain_map.keys():
        degree = G.degree(node)
        degree_groups[degree].append(node)
    # for degree, values in degree_groups.items():
    #     print(f"Degree {degree}:")
    #     print(values)
    neighbor_vector_groups = {}
    for degree, nodes_in_group in degree_groups.items():
        neighbor_vector_groups[degree] = defaultdict(list)
        for node in nodes_in_group:
            vector = tuple(neighbor_vectors[node])  # 将向量转换为元组以便作为字典的键
            neighbor_vector_groups[degree][vector].append(node)
    print("neighbor_vector_groups:", len(neighbor_vector_groups))
    print("Degree Groups and Neighbor Vector Groups:")
    for degree, groups in neighbor_vector_groups.items():
        print(f"Degree {degree}:")
        for vector, nodes in groups.items():
            print(f"  Vector {vector}: {nodes}")
    print("\nOriginal Graph - Nodes:", nodes, "Edges:", list(G.edges()))
    write_neighbor_vector_groups_to_file(neighbor_vector_groups, 'neighbor_vector_groups.json')

    new_neighbor_vector_groups = read_neighbor_vector_groups_from_file('neighbor_vector_groups.json')
    for degree, groups in new_neighbor_vector_groups.items():
        print(f"Degree {degree}:")
        for vector, nodes in groups.items():
            print(f"  Vector {vector}: {nodes}")


    # # 创建一个简单的非 k-匿名图
    # G = nx.Graph()
    # # 添加边以形成一个非 k-匿名的度序列
    # edges = [('0', '1'), ('1', '2'), ('2', '3'), ('3', '4'), ('4', '5'),
    #          ('5', '0'), ('0', '2'), ('1', '5')]
    # G.add_edges_from(edges)
    #
    # nodes = G.nodes()
    # neighbor_vectors = {}
    # for node in nodes:
    #     # 获取节点的邻居
    #     neighbors = set(G.neighbors(node))
    #     # 初始化邻域向量
    #     vector = [1 if n in neighbors or n == node else 0 for n in nodes]
    #     # 将向量存储到字典中
    #     neighbor_vectors[node] = vector
    #
    # # for key in sorted(neighbor_vectors.keys(), key = int):
    # #     print(f"Node {key}: {neighbor_vectors[key]}")
    # # FileUtil.write_json_to_file(neighbor_vectors, 'test.json')
    # # print("neighbor_vectors:", len(neighbor_vectors))
    #
    # # 按照节点度进行分组
    # degree_groups = defaultdict(list)
    # for node in nodes:
    #     degree = G.degree(node)
    #     degree_groups[degree].append(node)
    # # for degree, values in degree_groups.items():
    # #     print(f"Degree {degree}:")
    # #     print(values)
    # neighbor_vector_groups = {}
    # for degree, nodes_in_group in degree_groups.items():
    #     neighbor_vector_groups[degree] = defaultdict(list)
    #     for node in nodes_in_group:
    #         vector = tuple(neighbor_vectors[node])  # 将向量转换为元组以便作为字典的键
    #         neighbor_vector_groups[degree][vector].append(node)
    # print("neighbor_vector_groups:", len(neighbor_vector_groups))
    # print("Degree Groups and Neighbor Vector Groups:")
    # for degree, groups in neighbor_vector_groups.items():
    #     print(f"Degree {degree}:")
    #     for vector, nodes in groups.items():
    #         print(f"  Vector {vector}: {nodes}")
    # print("\nOriginal Graph - Nodes:", nodes, "Edges:", list(G.edges()))
    # with open('neighbor_vector_groups.json', 'w') as f:
    #     # 将 defaultdict 转换为普通字典，以便 json 序列化
    #     neighbor_vector_groups_dict = {str(degree): {str(vector): nodes for vector, nodes in groups.items()} for
    #                                    degree, groups in neighbor_vector_groups.items()}
    #     json.dump(neighbor_vector_groups_dict, f, indent=4)