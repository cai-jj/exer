import json
from collections import defaultdict

import networkx as nx

from util.file_util import FileUtil


### 计算代价
def calculate_merge_cost(neighbor_vectors, group1, group2):
    """
    计算将节点 node 加入 group 的合并代价，并返回新的领域向量。

    :param neighbor_vectors: 存储每个节点的领域向量
    :param node: 待加入的节点
    :param group: 目标组
    :return: 合并代价, 新的领域向量
    """
    node_vector = neighbor_vectors[group1[0]]
    target_vector = neighbor_vectors[group2[0]]  # 组内的任意一个节点的领域向量

    cost = 0
    new_vector = node_vector[:]
    for i in range(len(node_vector)):
        if node_vector[i] == 0 and target_vector[i] == 1:
            new_vector[i] = 1
            cost += 1  # 将 0 变为 1 的代价
        elif node_vector[i] == 1 and target_vector[i] == 0:
            new_vector[i] = 1
            cost += 1
    return cost * (len(group1) + len(group2)), new_vector


def k_anonymize_directed(G, k, domain_map):
    """
    对有向图进行 k-匿名化处理。

    :param G: 有向图
    :param k: k-匿名性参数
    :return: k-匿名化的图, 新的分组
    """
    # 计算邻域向量
    print("domain_map:", len(domain_map))
    nodes = G.nodes()
    in_degree_vectors = {}
    for node in domain_map.keys():
        in_neighbors = set(G.predecessors(node))  # 获取入度邻居
        vector = [1 if n in in_neighbors or n == node else 0 for n in nodes]
        in_degree_vectors[node] = vector
    # 按照领域向量进行分组
    vector_groups = defaultdict(list)
    for node in domain_map.keys():
        vector = tuple(in_degree_vectors[node])  # 将向量转换为元组以便作为字典的键
        vector_groups[vector].append(node)
    print("vector_groups:", len(vector_groups))
    # 筛选出所有节点数量小于 k 的分组
    # small_groups = [(vector, nodes) for vector, nodes in vector_groups.items() if len(nodes) < k]
    small_groups = []
    new_groups = defaultdict(list)
    for vector, nodes in vector_groups.items():
        if len(nodes) < k:
            small_groups.append((vector, nodes))
        else:
            new_groups[vector] = nodes
    while small_groups:
        vector, nodes = small_groups.pop(0)
        while len(nodes) < k:
            # 尝试合并其他小于 k 的分组
            min_cost = float('inf')
            best_other_group = None
            best_new_vector = None

            for other_vector, other_nodes in small_groups:
                merge_cost, new_vector = calculate_merge_cost(in_degree_vectors, nodes, other_nodes)
                if merge_cost < min_cost:
                    min_cost = merge_cost
                    best_other_group = (other_vector, other_nodes)
                    best_new_vector = new_vector

            if best_other_group:
                small_groups.remove(best_other_group)
                other_vector, other_nodes = best_other_group
                nodes.extend(other_nodes)
                # 更新领域向量
                for node in nodes:
                    in_degree_vectors[node] = best_new_vector
                # 重新检查合并后的组是否仍需处理
                if len(nodes) < k:
                    continue
                else:
                    new_groups[tuple(best_new_vector)] = nodes
                    break
            else:
                new_groups[tuple(vector)] = nodes
                break

    return G, new_groups, vector_groups

if __name__ == '__main__':

    domain_map = FileUtil.read_json_from_file('domain_map_to_number_map.json')

    # 创建有向图
    G = nx.DiGraph()
    edges = []
    for key, value in domain_map.items():
        for item in value:
            edges.append((item, key))  # item 指向 key
    G.add_edges_from(edges)

    # 进行 k-匿名化处理
    k = 3
    G_anonymized, anonymized_vector_groups, vector_groups = k_anonymize_directed(G, k, domain_map)
    # 打印 k-匿名化后的结果
    print("\norigin Graph - Nodes:", list(G.nodes()), "Edges:", list(G.edges()))
    print("Origin Vector Groups:")
    for vector, nodes in vector_groups.items():
        print(f"  Vector {vector}: {nodes}")
    # 打印 k-匿名化后的结果
    print("\nAnonymized Graph - Nodes:", list(G_anonymized.nodes()), "Edges:", list(G_anonymized.edges()))
    print("Anonymized Vector Groups:")
    for vector, nodes in anonymized_vector_groups.items():
        print(f"  Vector {vector}: {nodes}")
