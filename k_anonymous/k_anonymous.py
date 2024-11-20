import json
import os
from collections import defaultdict

import networkx as nx

from util.file_util import FileUtil


def write_json_to_file(kv_pairs, output_file, chunk_size=1024 * 1024 * 10):  # 10 MB
    """将键值对以 JSON 格式写入文件，支持大文件写入"""
    try:
        # 将键值对转换为 JSON 字符串
        json_str = json.dumps(kv_pairs, ensure_ascii=False, indent=4)

        # 分块写入文件
        with open(output_file, 'w', encoding='utf-8') as file:
            for i in range(0, len(json_str), chunk_size):
                chunk = json_str[i:i + chunk_size]
                file.write(chunk)

                # 检查文件大小
                current_size = os.path.getsize(output_file)
                if current_size > 10 * 1024 * 1024 * 1024:  # 10 GB
                    print("File size exceeds the maximum allowed size.")
                    break
    except IOError as e:
        print(f"Error writing to file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
if __name__ == '__main__':
    domain_map = FileUtil.read_json_from_file('../domain_map_to_number_map.json')
    G = nx.Graph()
    edges = []
    for key, value in domain_map.items():
        for item in value:
            edges.append((key, item))
    G.add_edges_from(edges)
    nodes = sorted(G.nodes(), key= int)
    # neighbor_vectors = {}
    # for node in nodes:
    #     # 获取节点的邻居
    #     neighbors = set(G.neighbors(node))
    #     # 初始化邻域向量
    #     vector = [1 if n in neighbors or n == node else 0 for n in nodes]
    #     # 将向量存储到字典中
    #     neighbor_vectors[node] = vector
    # print("Neighbor Vectors:")
    # for node in nodes:  # 按照排序后的节点顺序打印
    #     print(f"Node {node}: {neighbor_vectors[node]}")
    # print("\nOriginal Graph - Nodes:", nodes, "Edges:", list(G.edges()))
    # FileUtil.write_json_to_file(neighbor_vectors, '../test.json')

    degrees = dict(G.degree())

    # 使用 defaultdict 来分类节点
    degree_to_nodes = defaultdict(list)

    # 将节点按度分类
    for node, degree in degrees.items():
        degree_to_nodes[degree].append(node)

    # 打印分类结果
    print("Nodes classified by degree:")
    for degree, nodes in degree_to_nodes.items():
        print(f"Degree {degree}: {nodes}")

    # 打印原始图的信息
    print("\nOriginal Graph - Nodes:", G.nodes(), "Edges:", G.edges())