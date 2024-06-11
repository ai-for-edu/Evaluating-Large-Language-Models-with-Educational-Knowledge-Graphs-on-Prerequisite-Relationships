import random
import networkx as nx
from lingua import Language, LanguageDetectorBuilder
from itertools import combinations


def is_chinese(text):
    languages = [Language.CHINESE, Language.ENGLISH]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()
    language = detector.detect_language_of(text)
    return language == Language.CHINESE


class DataPreprocessor:
    def __init__(self, graph_path):
        self.graph_path = graph_path
        self.graph = nx.read_graphml(graph_path)
        self.kg = self.graphml_to_kg()
        self.kg_edges = self.kg.number_of_edges()
        self.zh_flag = False

    def graphml_to_kg(self):
        """
        Convert a networkx DiGraph to a knowledge graph
        :return: a knowledge graph
        """
        nx_digraph = self.graph

        for edge in nx_digraph.edges(data=True):
            if 'relationship' in edge[2]:
                print(f"Edge {edge[0]} -> {edge[1]} has relationship: {edge[2]['relationship']}")
                return nx_digraph
        zh_flag = False
        for u, v, data in nx_digraph.edges(data=True):
            subj = nx_digraph.nodes[u]['name']
            obj = nx_digraph.nodes[v]['name']
            # print(subj)
            zh_flag += is_chinese(subj)
            zh_flag += is_chinese(obj)
        self.zh_flag = zh_flag
        # print("zh-flag: ", zh_flag)
        if zh_flag:
            for edge in nx_digraph.edges:
                nx_digraph[edge[0]][edge[1]]['relationship'] = '前置知识'
        else:
            for edge in nx_digraph.edges:
                nx_digraph[edge[0]][edge[1]]['relationship'] = 'the prerequisite knowledge of'
        return nx_digraph

    def construct_graph(self):
        # knowledge graph
        # kb[e][rel] = set([e, e, e])
        kg = self.kg

        triplets = []
        for u, v, data in kg.edges(data=True):
            subj = kg.nodes[u]['name']
            obj = kg.nodes[v]['name']
            pred = data.get('relationship', 'related')  # Default to 'related' if no relationship specified
            triplets.append((subj, pred, obj))
        return triplets

    def check_betweenness_centrality(self):
        edge_betweenness = nx.edge_betweenness_centrality(self.kg, normalized=True)
        sorted_edges = sorted(edge_betweenness.items(), key=lambda item: item[1], reverse=True)
        return sorted_edges

    def top_k_betweenness_centrality(self, k=10):
        """
        Find the top k edges with the highest betweenness centrality in a knowledge graph.
        Returns formatted strings for one-hop, two-hops, and three-hops neighbors.
        :param k:
        :return: The top k edges <sending_node, relation, receiving_node>
                with the highest betweenness centrality, descending order
                As the form of dictionary:
        """
        edge_betweenness = nx.edge_betweenness_centrality(self.kg, normalized=True)
        sorted_edges = sorted(edge_betweenness.items(), key=lambda item: item[1], reverse=True)
        top_k_edges = sorted_edges[:k]

        # Data structure to store results
        result = []

        for edge, centrality in top_k_edges:
            node_u, node_v = edge
            relationship = self.kg[node_u][node_v].get('relationship', 'related')
            one_hops = [(self.kg.nodes[node_u]['name'], relationship, self.kg.nodes[node_v]['name'])]
            two_hops = []
            three_hops = []

            # Collect two-hops (pick one successor of node_v if available)
            neighbors_v = list(self.kg.neighbors(node_v))
            if neighbors_v:
                selected_neighbor = random.choice(neighbors_v)
                rel2 = self.kg[node_v][selected_neighbor].get('relationship', 'related')
                two_hops.append((self.kg.nodes[node_u]['name'], relationship, self.kg.nodes[node_v]['name'],
                                 rel2, self.kg.nodes[selected_neighbor]['name']))

                # Collect three-hops (pick one successor of the selected_neighbor if available)
                neighbors_n = list(self.kg.neighbors(selected_neighbor))
                if neighbors_n:
                    selected_second_neighbor = random.choice(neighbors_n)
                    rel3 = self.kg[selected_neighbor][selected_second_neighbor].get('relationship', 'related')
                    three_hops.append(
                        (self.kg.nodes[node_u]['name'], relationship, self.kg.nodes[node_v]['name'],
                         rel2, self.kg.nodes[selected_neighbor]['name'],
                         rel3, self.kg.nodes[selected_second_neighbor]['name']
                         ))

            result.append({
                'edge': (self.kg.nodes[node_u]['name'], self.kg.nodes[node_v]['name']),
                'one_hops': one_hops,
                'two_hops': two_hops,
                'three_hops': three_hops
            })

        return result

    def construct_graph_negative(self):
        """
        Find node pairs in a directed graph that are not connected at all. And make them as negative samples.
        """
        # knowledge graph
        # kb[e][rel] = set([e, e, e])
        kg = self.kg

        node_list = list(kg.nodes())
        triplets = []
        rel = ''
        for u, v, data in kg.edges(data=True):
            rel = data.get('relationship', 'related')  # Default to 'related' if no relationship specified

        for i in range(len(node_list)):
            for j in range(len(node_list)):
                if i == j:
                    continue
                node1 = node_list[i]
                node2 = node_list[j]
                # Check if there is no path in either direction
                if not nx.has_path(kg, node1, node2) and not nx.has_path(kg, node2, node1):
                    # Extract names if available or use node id
                    name1 = kg.nodes[node1].get('name', node1)
                    name2 = kg.nodes[node2].get('name', node2)
                    triplets.append((name1, rel, name2))
        if len(triplets) > self.kg_edges:
            triplets = random.sample(triplets, self.kg_edges)
        return triplets

    def construct_two_hop_paths(self):
        graph = self.kg
        two_hop_paths = []
        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        for node in graph.nodes():
            # Get successors of the node (i.e., nodes one hop away)
            successors = list(graph.successors(node))
            for successor in successors:
                # Get the successors of the successors (two hops away)
                second_hop_successors = list(graph.successors(successor))
                for second_hop in second_hop_successors:
                    if second_hop != node:  # Exclude self-loops or returning edges
                        two_hop_paths.append((graph.nodes[node]['name'], relation, graph.nodes[successor]['name'],
                                              relation, graph.nodes[second_hop]['name']))
        return two_hop_paths

    def construct_two_hop_paths_negative_replace_terminal(self):
        """
        Generating negative samples by replacing the terminal node in two-hop path sampling pipeline,
        :return:
        """
        graph = self.kg
        negative_two_hop_paths = []
        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        all_nodes = set(graph.nodes())  # Collect all nodes for random sampling

        for node in graph.nodes():
            # Get successors of the node (i.e., nodes one hop away)
            successors = list(graph.successors(node))
            for successor in successors:
                # Get the successors of the successors (two hops away)
                second_hop_successors = list(graph.successors(successor))
                for second_hop in second_hop_successors:
                    if second_hop != node:  # Exclude self-loops or returning edges
                        # Generate negative sample
                        potential_negatives = list(all_nodes - set(second_hop_successors) - {node, successor})
                        if potential_negatives:
                            negative_end = random.choice(potential_negatives)
                            negative_two_hop_paths.append((graph.nodes[node]['name'], relation,
                                                           graph.nodes[successor]['name'], relation,
                                                           graph.nodes[negative_end]['name']))

        return negative_two_hop_paths

    def construct_two_hop_paths_negative_replace_intermediate(self):
        """
        Adjust the path such that the connection between the start node and
        the new intermediate node does not logically lead to the end node via a valid two-hop path.
        :return:
        """
        graph = self.kg
        negative_two_hop_paths = []
        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        all_nodes = set(graph.nodes())  # Collect all nodes for random sampling

        for node in graph.nodes():
            # Get successors of the node (i.e., nodes one hop away)
            successors = list(graph.successors(node))
            for successor in successors:
                # Get the successors of the successors (two hops away)
                second_hop_successors = list(graph.successors(successor))
                for second_hop in second_hop_successors:
                    if second_hop != node:  # Exclude self-loops or returning edges
                        # Generate negative sample by replacing the intermediate node
                        # Exclude the current successor and any node that would make a valid two-hop path to the second_hop
                        potential_intermediates = all_nodes - set(successors) - {node, second_hop}
                        potential_intermediates -= set(
                            nx.descendants(graph, second_hop))  # Ensure no valid path through replacement
                        if potential_intermediates:
                            negative_intermediate = random.choice(list(potential_intermediates))
                            negative_two_hop_paths.append((graph.nodes[node]['name'], relation,
                                                           graph.nodes[negative_intermediate]['name'], relation,
                                                           graph.nodes[second_hop]['name']))

        return negative_two_hop_paths

    def construct_two_hop_paths_negative_invert_relations(self):
        """
        Inverting relationships to create negative samples in a two-hop reasoning task within a knowledge graph involves
        changing the direction of one or both edges, resulting in a path that is not typically valid.
        In the case here, only consider the change of the direction of both edges.
        :return:
        """
        graph = self.kg
        negative_two_hop_paths = []
        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        # all_nodes = set(graph.nodes())  # Collect all nodes for random sampling
        for node in graph.nodes():
            # Get successors of the node (i.e., nodes one hop away)
            successors = list(graph.successors(node))
            for successor in successors:
                # Get the successors of the successors (two hops away)
                second_hop_successors = list(graph.successors(successor))
                for second_hop in second_hop_successors:
                    if second_hop != node:  # Exclude self-loops or returning edges
                        negative_two_hop_paths.append(
                            (graph.nodes[second_hop]['name'],
                             relation,
                             graph.nodes[successor]['name'],
                             relation,
                             graph.nodes[node]['name']))

                    # # The following cases are not considered as they are not valid paths
                    # # in the case of educational KGs
                    # elif graph.has_edge(second_hop, successor):
                    #     # Only invert the second relationship
                    #     negative_two_hop_paths.append((graph.nodes[node]['name'], relation,
                    #                                    graph.nodes[second_hop]['name'], relation,
                    #                                    graph.nodes[successor]['name']))
                    # elif graph.has_edge(successor, node):
                    #     # Only invert the first relationship
                    #     negative_two_hop_paths.append((graph.nodes[successor]['name'], relation,
                    #                                    graph.nodes[node]['name'], relation,
                    #                                    graph.nodes[second_hop]['name']))

        return negative_two_hop_paths

    def construct_two_hop_paths_negative_path_disruption(self):
        """
        If A→B→C represents a flow of concepts or processes,
        inserting an unrelated or obstructive node to form A→X→C where
        X does not logically connect A and C could be a viable negative example.
        :return:
        """
        graph = self.kg
        negative_two_hop_paths = []
        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        all_nodes = set(graph.nodes())  # Collect all nodes for random sampling

        for node in graph.nodes():
            # Get successors of the node (i.e., nodes one hop away)
            successors = list(graph.successors(node))
            for successor in successors:
                # Get the successors of the successors (two hops away)
                second_hop_successors = list(graph.successors(successor))
                for second_hop in second_hop_successors:
                    if second_hop != node:  # Exclude self-loops or returning edges
                        # Generate negative sample by introducing a disruptor
                        # Select a disruptor that is not a successor of the first node or predecessor of the last node
                        potential_disruptors = [
                            n for n in all_nodes if
                            n not in second_hop_successors
                            and not nx.has_path(graph, node, n)
                            and not nx.has_path(graph, n, second_hop)
                        ]
                        if potential_disruptors:
                            disruptor = random.choice(potential_disruptors)
                            negative_two_hop_paths.append((graph.nodes[node]['name'], relation,
                                                           graph.nodes[disruptor]['name'], relation,
                                                           graph.nodes[second_hop]['name']))

        return negative_two_hop_paths

    def construct_three_hop_paths(self):
        graph = self.kg
        three_hop_paths = []
        relation = ''
        for u, v, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        for node in graph.nodes():
            # Get successors of the node (i.e., nodes one hop away)
            successors = list(graph.successors(node))
            for successor in successors:
                # Get the successors of the successors (two hops away)
                second_hop_successors = list(graph.successors(successor))
                for second_hop in second_hop_successors:
                    third_hop_successors = list(graph.successors(second_hop))
                    for third_hop in third_hop_successors:
                        if third_hop != node:  # Exclude self-loops or returning edges
                            three_hop_paths.append((graph.nodes[node]['name'], relation,
                                                    graph.nodes[successor]['name'], relation,
                                                    graph.nodes[second_hop]['name'], relation,
                                                    graph.nodes[third_hop]['name']))
        return three_hop_paths

    def construct_three_hop_paths_negative(self):
        """
        Generate negative samples for three-hop reasoning tasks by replacing the terminal node with a random node
        :return:
        """
        graph = self.kg
        negative_three_hop_paths = []
        relation = ''

        # Assume a default relationship if not specified
        for u, v, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        all_nodes = list(graph.nodes())  # List of all nodes for random selection

        for node in graph.nodes():
            # Get successors of the node (i.e., nodes one hop away)
            successors = list(graph.successors(node))
            for successor in successors:
                # Get the successors of the successors (two hops away)
                second_hop_successors = list(graph.successors(successor))
                for second_hop in second_hop_successors:
                    # Third hop: successors of the second-hop node
                    third_hop_successors = list(graph.successors(second_hop))
                    for third_hop in third_hop_successors:
                        if third_hop != node:  # Ensure it's not creating a loop back to the start
                            # Now, choose a random node that is not a valid third_hop
                            possible_negatives = [n for n in all_nodes if n not in third_hop_successors and n != node]
                            if possible_negatives:
                                random_negative_node = random.choice(possible_negatives)
                                negative_three_hop_paths.append((graph.nodes[node]['name'], relation,
                                                                 graph.nodes[successor]['name'], relation,
                                                                 graph.nodes[second_hop]['name'], relation,
                                                                 graph.nodes[random_negative_node]['name']))
                            possible_first_replacements = [n for n in all_nodes if n not in successors and n != node]
                            if possible_first_replacements:
                                random_first_replacement = random.choice(possible_first_replacements)
                                negative_three_hop_paths.append((graph.nodes[node]['name'], relation,
                                                                 graph.nodes[random_first_replacement]['name'],
                                                                 relation,
                                                                 graph.nodes[second_hop]['name'], relation,
                                                                 graph.nodes[third_hop]['name']))

                            # Replace the second intermediate node (second_hop) with a random node
                            possible_second_replacements = [n for n in all_nodes if
                                                            n not in second_hop_successors and n != successor]
                            if possible_second_replacements:
                                random_second_replacement = random.choice(possible_second_replacements)
                                negative_three_hop_paths.append((graph.nodes[node]['name'], relation,
                                                                 graph.nodes[successor]['name'], relation,
                                                                 graph.nodes[random_second_replacement]['name'],
                                                                 relation,
                                                                 graph.nodes[third_hop]['name']))
                            # Check if all inverted relationships exist
                            if graph.has_edge(third_hop, second_hop) and graph.has_edge(second_hop,
                                                                                        successor) and graph.has_edge(
                                successor, node):
                                # Store the inverted negative path
                                negative_three_hop_paths.append((graph.nodes[third_hop]['name'], relation,
                                                                 graph.nodes[second_hop]['name'], relation,
                                                                 graph.nodes[successor]['name'], relation,
                                                                 graph.nodes[node]['name']))
                            possible_disruptors = [n for n in all_nodes if
                                                   n not in successors and n not in second_hop_successors and n not in third_hop_successors]
                            # Choose a random disruptor node that is not connected directly to the current path
                            if possible_disruptors:
                                disruptor = random.choice(possible_disruptors)
                                # Insert disruptor in one of the intermediate positions
                                positions = [1,
                                             2]  # Position 1 between first and second, Position 2 between second and third
                                position = random.choice(positions)
                                if position == 1:
                                    # Disrupt between first and second hop
                                    negative_three_hop_paths.append((graph.nodes[node]['name'], relation,
                                                                     graph.nodes[disruptor]['name'], relation,
                                                                     graph.nodes[second_hop]['name'], relation,
                                                                     graph.nodes[third_hop]['name']))
                                elif position == 2:
                                    # Disrupt between second and third hop
                                    negative_three_hop_paths.append((graph.nodes[node]['name'], relation,
                                                                     graph.nodes[successor]['name'], relation,
                                                                     graph.nodes[disruptor]['name'], relation,
                                                                     graph.nodes[third_hop]['name']))

        return negative_three_hop_paths

    def construct_paths_nodes_with_two_predecessors(self):
        graph = self.kg

        p2_query = []

        for node in graph.nodes():
            predecessors = list(graph.predecessors(node))
            if len(predecessors) == 2:
                # Store each predecessor and the relationship to the target node
                p2_query.append((graph.nodes[predecessors[0]]['name'], graph.nodes[predecessors[1]]['name'],
                                 graph.edges[predecessors[0], node]['relationship'], graph.nodes[node]['name']))

        return p2_query

    def construct_paths_nodes_with_two_predecessors_negative_one(self, choice=0):
        """
        Generate negative samples for two-hop reasoning tasks by replacing one of the predecessors with a random node
        :param choice: to choose which predecessor to replace, 0 for first, 1 for second
        :return:
        """
        graph = self.kg

        p2_negative_query = []

        for node in graph.nodes():
            predecessors = list(graph.predecessors(node))
            if len(predecessors) == 2:
                # Choose a node to replace
                replacement_target = choice
                other_predecessor = predecessors[1 - replacement_target]
                # Collect possible replacements that are not current predecessors of the node
                possible_replacements = [
                    n for n in graph.nodes() if n not in predecessors
                                                and not nx.has_path(graph, n, node) and not nx.has_path(graph, node, n)
                ]

                if possible_replacements:
                    replacement = random.choice(possible_replacements)

                    # Create the negative sample
                    if replacement_target == 0:
                        negative_sample = (graph.nodes[replacement]['name'], graph.nodes[other_predecessor]['name'],
                                           graph.edges[other_predecessor, node]['relationship'],
                                           graph.nodes[node]['name'])
                    else:
                        negative_sample = (graph.nodes[other_predecessor]['name'], graph.nodes[replacement]['name'],
                                           graph.edges[other_predecessor, node]['relationship'],
                                           graph.nodes[node]['name'])

                    p2_negative_query.append(negative_sample)

        return p2_negative_query

    def construct_paths_nodes_with_two_predecessors_negative_two(self):
        graph = self.kg

        p2_double_negative_query = []

        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        for node in graph.nodes():
            predecessors = list(graph.predecessors(node))
            if len(predecessors) == 2:
                # Collect possible replacements that are not current predecessors of the node
                possible_replacements = [n for n in graph.nodes() if n not in predecessors
                                         and not nx.has_path(graph, n, node) and not nx.has_path(graph, node, n)]

                if len(possible_replacements) >= 2:
                    # Ensure we get two distinct replacements
                    replacement1, replacement2 = random.sample(possible_replacements, 2)

                    # Create the negative sample
                    negative_sample = (graph.nodes[replacement1]['name'], graph.nodes[replacement2]['name'],
                                       relation,
                                       graph.nodes[node]['name'])  # Using 'related' or adjust based on your data

                    p2_double_negative_query.append(negative_sample)

        return p2_double_negative_query

    def construct_paths_nodes_with_three_predecessors(self):
        graph = self.kg

        p3_query = []

        for node in graph.nodes():
            predecessors = list(graph.predecessors(node))
            if len(predecessors) == 3:
                # Store each predecessor and the relationship to the target node
                p3_query.append((graph.nodes[predecessors[0]]['name'], graph.nodes[predecessors[1]]['name'],
                                 graph.nodes[predecessors[2]]['name'],
                                 graph.edges[predecessors[0], node]['relationship'], graph.nodes[node]['name']))

        return p3_query

    def construct_paths_nodes_with_three_predecessors_negative_one(self, choice=0):
        """
        Generate negative samples for three-hop reasoning tasks by replacing one of the predecessors with a random node
        :param choice: Which predecessor to replace, 0, 1, or 2
        :return:
        """
        graph = self.kg

        # 'the prerequisite knowledge of'
        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        p3_negative_query = []

        for node in graph.nodes():
            predecessors = list(graph.predecessors(node))
            if len(predecessors) == 3:
                # Collect possible replacements that either do not lead to the node or from
                # which the node is not reachable
                possible_replacements = [n for n in graph.nodes() if
                                         not nx.has_path(graph, n, node) and not nx.has_path(graph, node, n)]

                if possible_replacements:
                    # Choose a random predecessor to replace
                    replacement_target = predecessors[choice]
                    replacement = random.choice(possible_replacements)

                    # Construct the new list of predecessors with one replaced
                    new_predecessors = [replacement if pred == replacement_target else pred for pred in predecessors]

                    # Store the new set up with one predecessor replaced
                    p3_negative_query.append((
                        graph.nodes[new_predecessors[0]]['name'],
                        graph.nodes[new_predecessors[1]]['name'],
                        graph.nodes[new_predecessors[2]]['name'],
                        relation,  # Assuming a default 'related' relationship or adjust based on your data
                        graph.nodes[node]['name']
                    ))

        return p3_negative_query

    def construct_paths_nodes_with_three_predecessors_negative_two(self, replace_indices=(0, 1)):
        graph = self.kg

        p3_double_negative_query = []
        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        for node in graph.nodes():
            predecessors = list(graph.predecessors(node))
            if len(predecessors) == 3:
                # Validate replace_indices are valid and unique
                if len(set(replace_indices)) == 2 and all(idx in [0, 1, 2] for idx in replace_indices):
                    # Collect possible replacements that either do not lead to the node or
                    # from which the node is not reachable
                    possible_replacements = [n for n in graph.nodes() if
                                             not nx.has_path(graph, n, node) and not nx.has_path(graph, node, n)]

                    if len(possible_replacements) >= 2:
                        # Randomly select two distinct nodes to use as replacements
                        replacement1, replacement2 = random.sample(possible_replacements, 2)

                        # Replace the specified predecessors
                        new_predecessors = predecessors[:]
                        new_predecessors[replace_indices[0]] = replacement1
                        new_predecessors[replace_indices[1]] = replacement2

                        # Store the new setup with two predecessors replaced
                        p3_double_negative_query.append((
                            graph.nodes[new_predecessors[0]]['name'],
                            graph.nodes[new_predecessors[1]]['name'],
                            graph.nodes[new_predecessors[2]]['name'],
                            relation,  # Default relationship
                            graph.nodes[node]['name']
                        ))
                else:
                    raise ValueError("Invalid indices for replacement.")

        return p3_double_negative_query

    def construct_paths_nodes_with_three_predecessors_negative_three(self):
        graph = self.kg

        p3_full_negative_query = []
        relation = ''
        for _, _, data in graph.edges(data=True):
            relation = data.get('relationship', 'related')
            break

        for node in graph.nodes():
            predecessors = list(graph.predecessors(node))
            if len(predecessors) == 3:
                # Collect possible replacements that neither lead to the node nor from which the node is reachable
                possible_replacements = [n for n in graph.nodes() if
                                         not nx.has_path(graph, n, node) and not nx.has_path(graph, node, n)]

                if len(possible_replacements) >= 3:
                    # Randomly select three distinct nodes to use as replacements
                    replacement1, replacement2, replacement3 = random.sample(possible_replacements, 3)

                    # Store the new setup with all predecessors replaced
                    p3_full_negative_query.append((
                        graph.nodes[replacement1]['name'],
                        graph.nodes[replacement2]['name'],
                        graph.nodes[replacement3]['name'],
                        relation,  # Assuming a default 'related' relationship or adjust based on your data
                        graph.nodes[node]['name']
                    ))

        return p3_full_negative_query

    # def get_node_pairs(self, graph):  # Deprecated
    #     node_pairs = []
    #     nodes = list(graph.nodes())
    #     # print("number of nodes: ", len(nodes))
    #     # edges = list(graph.edges())
    #     # print("number of edges: ", len(edges))
    #     for i, node1 in enumerate(nodes):
    #         for node2 in nodes:  # Avoid duplicate pairs and self-pairs
    #             if node2 == node1:
    #                 continue
    #             has_edge = graph.has_edge(node1, node2)
    #             # print("has_edge: ", has_edge)
    #             relationship = graph[node1][node2]['relationship'] if has_edge else None
    #             node_pairs.append((
    #                 graph.nodes[node1]['name'],
    #                 graph.nodes[node2]['name'],
    #                 has_edge,
    #                 relationship))
    #     return node_pairs

    def get_node_pairs(self, graph):
        node_pairs = []
        non_edge_pairs = []
        nodes = list(graph.nodes())

        # Collecting edge pairs
        for node1, node2 in graph.edges():
            relationship = graph[node1][node2]['relationship']
            node_pairs.append((
                graph.nodes[node1]['name'],
                graph.nodes[node2]['name'],
                True,
                relationship
            ))

        # Number of edges to match with non-edges
        num_edges = len(node_pairs)

        # Collecting non-edge pairs
        while len(non_edge_pairs) < num_edges:
            node1, node2 = random.sample(nodes, 2)
            if not graph.has_edge(node1, node2) and not graph.has_edge(node2, node1) and (
            node1, node2) not in non_edge_pairs:
                non_edge_pairs.append((
                    graph.nodes[node1]['name'],
                    graph.nodes[node2]['name'],
                    False,
                    None
                ))

        # Combining edge and non-edge pairs
        node_pairs.extend(non_edge_pairs)
        return node_pairs

    def find_n_weakly_connected(self, graph, nodes, k, n=50):
        # Check all combinations of N nodes in the component to find a valid subgraph
        subgraph_ls = []
        count = 0
        for combo in combinations(nodes, k):
            subgraph = graph.subgraph(combo)
            if nx.is_weakly_connected(subgraph):
                subgraph_ls.append(subgraph)
                count += 1
            if count >= n:
                break
        return subgraph_ls

    def get_k_nodes(self, graph, k, n=0):
        weakly_connected = list(nx.weakly_connected_components(graph))
        selected_component = []
        for component in weakly_connected:
            if len(component) >= k:
                selected_component.append(component)
        k_nodes = []
        for component in selected_component:
            subgraph_ls = self.find_n_weakly_connected(graph, component, k)
            if len(subgraph_ls) > 0:
                k_nodes.extend(subgraph_ls)
            if len(k_nodes) >= n and n > 0:
                break
            if len(subgraph_ls) >= n and n > 0:
                break
        if len(k_nodes) == 0:
            print("No weakly connected subgraph with N nodes was found.")
            return k_nodes
        print("Matched cases: ", len(k_nodes))
        return [self.get_node_pairs(subgraph) for subgraph in k_nodes]

    def get_query_for_relation_extraction(self, one_one_one=True, k=10, n=0):
        """

        :param one_one_one:
        :param k: the number of nodes in the subgraph
        :param n: the number of node pairs / subgraphs to return
        :return:
        """
        graph = self.kg
        if one_one_one:
            ls = self.get_node_pairs(graph)
        else:
            ls = self.get_k_nodes(graph, k, n)
        if n == 0:
            return ls
        else:
            return random.sample(ls, n)

    def get_negative_node_pairs_for_relation_extraction(self):
        """
        Generate negative samples for relation extraction tasks by selecting node pairs that are not connected.
        Optimized for large graphs.
        :return:
        """
        num_samples = self.kg_edges
        nodes = list(self.kg.nodes())
        non_edges = []

        while len(non_edges) < num_samples:
            node1, node2 = random.sample(nodes, 2)
            if not self.kg.has_edge(node1, node2):
                non_edges.append((
                    self.kg.nodes[node1]['name'],
                    self.kg.nodes[node2]['name'],
                    False,
                    None
                ))

        return non_edges


def unmatching_query_w_gt(queries, path_or_triplet=True):
    """
    Generate a query that does not match the ground truth, just shuffle the order of the nodes in the query.
    :param path_or_triplet: Flag, is the query a path / triplet or p2 p3 query?
    :param queries: a query in the form of (node1, node2, has_edge, relationship)
    :return: a query that does not match the ground truth
    """
    new_queries = []
    if path_or_triplet:
        for i, query in enumerate(queries):
            # Create a new list that excludes the current query
            other_queries = queries[:i] + queries[i + 1:]
            while True:
                # Randomly select a query from the new list
                new_query = random.choice(other_queries)
                # Check if the first element of the new query doesn't match the first element of the current query
                if new_query[0] != query[0]:
                    new_queries.append(new_query)
                    break
        return new_queries
    else:
        for i, query in enumerate(queries):
            # Create a new list that excludes the current query
            other_queries = queries[:i] + queries[i + 1:]
            while True:
                # Randomly select a query from the new list
                new_query = random.choice(other_queries)
                # Check if the first element of the new query doesn't match the first element of the current query
                if new_query[-1] != query[-1]:
                    new_queries.append(new_query)
                    break
        return new_queries


def matching_betweeness_edges_as_gt(query, selected_edges):
    """
    Matching each query with the selected top k edges
    :param query: a query in the form of (node1, node2, has_edge, relationship)
    :param selected_edges: the selected edges (or one-hop, two-hops, three-hops) based on betweenness centrality
    :return: a list of query that matches the ground truth, with each corresponding to the repetitions
    of the edges in the selected_edges
    """
    to_return = []
    for edge in selected_edges:
        if len(edge) == 0:
            continue
        if len(edge) == 1:
            new_query = edge
        else:
            new_query = random.choice(edge)

        # Calculate the length difference
        length_diff = len(query) - 1
        # Extend the list by repeating the single element
        new_query.extend(new_query * length_diff)
        to_return.append(new_query)

    return to_return
