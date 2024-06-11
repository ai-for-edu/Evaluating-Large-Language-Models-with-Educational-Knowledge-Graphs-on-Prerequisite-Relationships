import pandas as pd
import networkx as nx
from sklearn import metrics
import numpy as np


# Define a function to extract the two strings
def get_kgs_from_questions():

    def extract_strings(s):
        # Find the positions of 'Is ', 'the', and 'of '
        start1 = s.find('Is ') + 3
        end1 = s.find(' the')
        start2 = s.find('of ') + 3
        end2 = s.find('?')

        # Extract the substrings
        str1 = s[start1:end1].strip()
        str2 = s[start2:end2].strip()

        return str1, str2

    # Load the CSV file
    df = pd.read_csv('logs/answers/DBE-KT22-node-pairs-questions-json_qwen-turbo_answer.csv')

    # Apply the function to the first column
    df['String1'], df['String2'] = zip(*df.iloc[:, 0].apply(extract_strings))

    # Save the DataFrame to an Excel file
    df.to_excel('output.xlsx', index=False)


# Get the groundtruth from the gml based on the questions
def check_groundtruth_edges():
    # Load the graph
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/DBE-KT22/DBE-KT22.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-Course.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-KnowledgePoints.graphml'
    graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/Junyi/Junyi-Prerequisites.graphml'

    G = nx.read_graphml(graphml_path)

    def extract_strings(s):
        # Find the positions of 'Is ', 'the', and 'of '
        start1 = s.find('Is ') + 3
        end1 = s.find(' the')
        start2 = s.find('of ') + 3
        end2 = s.find('?')

        # Extract the substrings
        str1 = s[start1:end1].strip()
        str2 = s[start2:end2].strip()

        return str1, str2

    def extract_strings_ZH(s):
        # Find the positions of 'Is ', 'the', and 'of '
        start1 = s.find('请问') + 2
        end1 = s.find('是')
        start2 = s.find('是') + 1
        end2 = s.find('的直接前置知识点吗？')

        # Extract the substrings
        str1 = s[start1:end1].strip()
        str2 = s[start2:end2].strip()

        return str1, str2

    def check_edge_exists(row):
        # Get nodes with 'name' attribute equal to 'String1' and 'String2'
        if 'Junyi' in graphml_path:
            nodes_string1 = [n for n, d in G.nodes(data=True) if d['name'] == row['String1'].replace(' ', '_')]
            nodes_string2 = [n for n, d in G.nodes(data=True) if d['name'] == row['String2'].replace(' ', '_')]
        else:
            nodes_string1 = [n for n, d in G.nodes(data=True) if d['name'] == row['String1']]
            nodes_string2 = [n for n, d in G.nodes(data=True) if d['name'] == row['String2']]

        # Check if there is a directed edge from any node in 'nodes_string1' to any node in 'nodes_string2'
        for node1 in nodes_string1:
            for node2 in nodes_string2:
                if G.has_edge(node1, node2):
                    return 1

        return 0

    # Load the CSV file
    df = pd.read_csv('logs/answers/Junyi-Prerequisites-node-pairs-questions-json_gpt-4_answer.csv')

    if 'WDKG' in graphml_path:
        df['String1'], df['String2'] = zip(*df.iloc[:, 0].apply(extract_strings_ZH))
    else:
        # Apply the function to the first column
        df['String1'], df['String2'] = zip(*df.iloc[:, 0].apply(extract_strings))

    # Define a function to check the existence of a directed edge

    # Apply the function to the DataFrame
    df['EdgeExists'] = df.apply(check_edge_exists, axis=1)
    # Save the DataFrame to an Excel file
    df.to_excel('output_w_groundtruth.xlsx', index=False)
    # Assuming G is your graph
    # list_of_edges = G.edges()
    # for i in list_of_edges:
    #     print(i)
    # for node, attributes in G.nodes(data=True):
    #     print(f"Node: {node} Attributes: {attributes}")


def check_groundtruth_edges_w_floats():
    # Load the graph
    # Load the graph
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/DBE-KT22/DBE-KT22.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-Course.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-KnowledgePoints.graphml'
    graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/Junyi/Junyi-Prerequisites.graphml'

    G = nx.read_graphml(graphml_path)

    def extract_strings(s):
        # Find the positions of 'Is ', 'the', and 'of '
        start1 = s.find('How essential is ') + 17
        end1 = s.find(' as a direct prerequisite')
        start2 = s.find('for understanding ') + 18
        end2 = s.find('?')

        # Extract the substrings
        str1 = s[start1:end1].strip()
        str2 = s[start2:end2].strip()

        return str1, str2

    def extract_strings_ZH(s):
        # Find the positions of 'Is ', 'the', and 'of '
        start1 = s.find('请问') + 2
        end1 = s.find('是')
        start2 = s.find('是') + 1
        end2 = s.find('的直接前置知识点')

        # Extract the substrings
        str1 = s[start1:end1].strip()
        str2 = s[start2:end2].strip()

        return str1, str2

    def check_edge_exists(row):
        # Get nodes with 'name' attribute equal to 'String1' and 'String2'
        if 'Junyi' in graphml_path:
            nodes_string1 = [n for n, d in G.nodes(data=True) if d['name'] == row['String1'].replace(' ', '_')]
            nodes_string2 = [n for n, d in G.nodes(data=True) if d['name'] == row['String2'].replace(' ', '_')]
        else:
            nodes_string1 = [n for n, d in G.nodes(data=True) if d['name'] == row['String1']]
            nodes_string2 = [n for n, d in G.nodes(data=True) if d['name'] == row['String2']]

        # Check if there is a directed edge from any node in 'nodes_string1' to any node in 'nodes_string2'
        for node1 in nodes_string1:
            for node2 in nodes_string2:
                if G.has_edge(node1, node2):
                    return 1

        return 0

    # Load the CSV file
    df = pd.read_csv('logs/answers/Junyi-Prerequisites-node-pairs-questions_w_floats-json_gpt-4_answer.csv')

    if 'WDKG' in graphml_path:
        df['String1'], df['String2'] = zip(*df.iloc[:, 0].apply(extract_strings_ZH))
    else:
        # Apply the function to the first column
        df['String1'], df['String2'] = zip(*df.iloc[:, 0].apply(extract_strings))

    # Define a function to check the existence of a directed edge

    # Apply the function to the DataFrame
    df['EdgeExists'] = df.apply(check_edge_exists, axis=1)
    # Save the DataFrame to an Excel file
    df.to_excel('output_w_groundtruth.xlsx', index=False)
    # Assuming G is your graph
    # list_of_edges = G.edges()
    # for i in list_of_edges:
    #     print(i)
    # for node, attributes in G.nodes(data=True):
    #     print(f"Node: {node} Attributes: {attributes}")


def evaluate_node_pairs():

    results = pd.ExcelFile('results_summary.xlsx')
    sheet_names = ['one-hop', 'two-hop', 'three-hop', 'two-predecessors', 'three-predecessors', 'node-pairs-summary',
                    'DBE-KT22-node-pairs', 'DBE-KT22-node-pairs-float', 'WDKG-Course-node-pairs',
                    'WDKG-Course-node-pairs-float',
                    'WDKG-Knowledgepoints-node-pairs', 'WDKG-KnowledgePoints-node-pai_f',
                    'Junyi-Prerequisites-node-pairs', 'Junyi-Prerequisites-node-pairsf']

    # print sheet names
    for count, sheet in enumerate(sheet_names[6:]):
        print(sheet)
        df = pd.read_excel(results, sheet_name=sheet)
        # Iterate over the columns from the third to the eighth
        for i in range(2, 8):  # Python uses 0-based indexing
            print("-----", df.columns[i], "-----")
            pred = df.iloc[:, i]  # predictions
            true = df.iloc[:, 8]  # ground truth

            # Calculate metrics

            auroc = metrics.roc_auc_score(true, pred)
            auprc = metrics.average_precision_score(true, pred)
            # Print metrics
            print(f"Metrics for column {i + 1}:")
            # Check if the result is binary
            # print(len(np.unique(pred)))
            # print(len(np.unique(true)))
            if count % 2 == 0:
                accuracy = metrics.accuracy_score(true, pred)
                recall = metrics.recall_score(true, pred)
                precision = metrics.precision_score(true, pred)
                print(f"Accuracy: {accuracy}")
                print(f"Recall: {recall}")
                print(f"Precision: {precision}")
            print(f"AUROC: {auroc}")
            print(f"AUPRC: {auprc}")

            print()
        print("=" * 25)
        print()
        # break


    # print(results.sheet_names)


if __name__ == '__main__':
    # get_kgs_from_questions()
    # check_groundtruth_edges()
    # check_groundtruth_edges_w_floats()

    evaluate_node_pairs()