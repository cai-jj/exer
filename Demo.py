from collections import defaultdict

import networkx as nx

from util.file_util import FileUtil

if __name__ == '__main__':

    domain_map = FileUtil.read_json_from_file('domain_map_to_number_map.json')
    G = nx.Graph()
    edges = []
    for key, value in domain_map.items():
        for item in value:
            edges.append((key, item))
    G.add_edges_from(edges)
    nodes = sorted(G.nodes(), key=int)
    neighbor_vectors = {}
    for node in nodes:
        # 获取节点的邻居
        neighbors = set(G.neighbors(node))
        # 初始化邻域向量
        vector = [1 if n in neighbors or n == node else 0 for n in nodes]
        # 将向量存储到字典中
        neighbor_vectors[node] = vector
    print("Neighbor Vectors:")
    for node in nodes:  # 按照排序后的节点顺序打印
        print(f"Node {node}: {neighbor_vectors[node]}")
    degree_groups = defaultdict(list)
    for node in nodes:
        degree = G.degree(node)
        degree_groups[degree].append(node)
    neighbor_vector_groups = {}
    for degree, nodes_in_group in degree_groups.items():
        neighbor_vector_groups[degree] = defaultdict(list)
        for node in nodes_in_group:
            vector = tuple(neighbor_vectors[node])  # 将向量转换为元组以便作为字典的键
            neighbor_vector_groups[degree][vector].append(node)

    print("Degree Groups and Neighbor Vector Groups:")
    for degree, groups in neighbor_vector_groups.items():
        print(f"Degree {degree}:")
        for vector, nodes in groups.items():
            print(f"  Vector {vector}: {nodes}")
    print("\nOriginal Graph - Nodes:", nodes, "Edges:", list(G.edges()))