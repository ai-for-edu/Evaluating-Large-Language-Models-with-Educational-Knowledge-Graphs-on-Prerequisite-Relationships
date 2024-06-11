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
    graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/DBE-KT22/DBE-KT22.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-Course.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-KnowledgePoints.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/Junyi/Junyi-Prerequisites.graphml'

    G = nx.read_graphml(graphml_path)

    def decompose_subquestions(s):
        # decompose the question into subquestions according to '. ' and '? '
        subquestions = s.split('. ')[1:]
        return subquestions[0].split('? ')

    def decompose_subquestions_ZH(s):
        # decompose the question into subquestions according to '. ' and '? '
        subquestions = s.split('。')[1:]
        return subquestions[0].split('？')

    def extract_strings(s):
        # Find the positions of 'Is ', 'the', and 'of '
        subquestions = decompose_subquestions(s)
        str1_list = []
        str2_list = []
        for subquestion in subquestions[:-1]:
            start1 = subquestion.find('Is ') + 3
            end1 = subquestion.find(' the')
            start2 = subquestion.find('of ') + 3
            end2 = -1

            # Extract the substrings
            str1_list.append(subquestion[start1:end1].strip())
            str2_list.append(subquestion[start2:].strip())
        return str1_list, str2_list

    def extract_strings_ZH(s):
        # Find the positions of 'Is ', 'the', and 'of '
        subquestions = decompose_subquestions_ZH(s)
        str1_list = []
        str2_list = []
        for subquestion in subquestions[:-1]:
            # Find the positions of 'Is ', 'the', and 'of '
            start1 = subquestion.find('请问') + 2
            end1 = subquestion.find('是')
            start2 = subquestion.find('是') + 1
            end2 = subquestion.find('的直接前置知识点吗')

            # Extract the substrings
            str1_list.append(subquestion[start1:end1].strip())
            str2_list.append(subquestion[start2:].strip())

        return str1_list, str2_list

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
    df = pd.read_csv('logs/answers/DBE-KT22-sub-graph-questions-size-10-json_qwen-turbo_answer.csv')

    if 'WDKG' in graphml_path:
        string1, string2 = zip(*df.iloc[:, 0].apply(extract_strings_ZH))
    else:
        # Apply the function to the first column
        string1, string2 = zip(*df.iloc[:, 0].apply(extract_strings))

    merged_string1 = []
    merged_string2 = []
    for i in range(len(string1)):
        merged_string1.extend(string1[i])
        merged_string2.extend(string2[i])
    string1 = merged_string1
    string2 = merged_string2

    df_new = pd.DataFrame({'String1': string1, 'String2': string2})
    # Define a function to check the existence of a directed edge

    # Apply the function to the DataFrame
    df_new['EdgeExists'] = df_new.apply(check_edge_exists, axis=1)
    # Save the DataFrame to an Excel file
    df_new.to_excel('output_w_groundtruth_subgraph.xlsx', index=False)
    # Assuming G is your graph
    # list_of_edges = G.edges()
    # for i in list_of_edges:
    #     print(i)
    # for node, attributes in G.nodes(data=True):
    #     print(f"Node: {node} Attributes: {attributes}")


def check_groundtruth_edges_w_floats():
    # Load the graph
    # Load the graph
    graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/DBE-KT22/DBE-KT22.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-Course.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-KnowledgePoints.graphml'
    # graphml_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/Junyi/Junyi-Prerequisites.graphml'

    G = nx.read_graphml(graphml_path)

    def decompose_subquestions(s):
        # decompose the question into subquestions according to '? '
        subquestions = s.split('? ')
        return subquestions

    def decompose_subquestions_ZH(s):
        # decompose the question into subquestions according to '. ' and '? '
        subquestions = s.split('？')
        return subquestions

    def extract_strings(s):
        subquestions = decompose_subquestions(s)
        str1_list = []
        str2_list = []
        for subquestion in subquestions[:-1]:
            # Find the positions of 'Is ', 'the', and 'of '
            start1 = subquestion.find('How essential is ') + 17
            end1 = subquestion.find(' as a direct prerequisite')
            start2 = subquestion.find('for understanding ') + 18
            end2 = -1

            # Extract the substrings
            str1_list.append(subquestion[start1:end1].strip())
            str2_list.append(subquestion[start2:].strip())

        return str1_list, str2_list

    def extract_strings_ZH(s):
        # Find the positions of 'Is ', 'the', and 'of '
        subquestions = decompose_subquestions_ZH(s)
        str1_list = []
        str2_list = []
        for subquestion in subquestions[:-1]:
            start1 = subquestion.find('请问') + 2
            end1 = subquestion.find('是')
            start2 = subquestion.find('是') + 1
            end2 = subquestion.find('的直接前置知识点')

            # Extract the substrings
            str1_list.append(subquestion[start1:end1].strip())
            str2_list.append(subquestion[start2:].strip())

        return str1_list, str2_list

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
    df = pd.read_csv('logs/answers/DBE-KT22-sub-graph-questions_w_floats-size-10-json_qwen-turbo_answer.csv')

    if 'WDKG' in graphml_path:
        string1, string2 = zip(*df.iloc[:, 0].apply(extract_strings_ZH))
    else:
        # Apply the function to the first column
        string1, string2 = zip(*df.iloc[:, 0].apply(extract_strings))

    merged_string1 = []
    merged_string2 = []
    for i in range(len(string1)):
        merged_string1.extend(string1[i])
        merged_string2.extend(string2[i])
    string1 = merged_string1
    string2 = merged_string2

    df_new = pd.DataFrame({'String1': string1, 'String2': string2})
    # Define a function to check the existence of a directed edge

    # Apply the function to the DataFrame
    df_new['EdgeExists'] = df_new.apply(check_edge_exists, axis=1)
    # Save the DataFrame to an Excel file
    df_new.to_excel('output_w_groundtruth_subgraph_f.xlsx', index=False)
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
                    'Junyi-Prerequisites-node-pairs', 'Junyi-Prerequisites-node-pairsf',
                   'DBE-KT22-subgraph5_b', 'DBE-KT22-subgraph5_f', 'DBE-KT22-subgraph10_b', 'testtest10', 'DBE-KT22-subgraph10_f']  # , 'DBE-KT22-subgraph10'  'testtest10'

    # print sheet names
    for count, sheet in enumerate(sheet_names[-1:]):
        print(sheet)
        df = pd.read_excel(results, sheet_name=sheet)
        # Iterate over the columns from the third to the eighth
        seg_list = [18, 40, 64, 86, 106]
        for j, seg in enumerate(seg_list):
            print("----- ++++++ R", j+1, " ++++++ -----")
            if j == 0:
                p1 = 0
            else:
                p1 = seg_list[j - 1]
            p2 = seg_list[j]
            for i in range(3, 8):  # Python uses 0-based indexing  # 8
                print("-----", df.columns[i], "-----")
                pred = df.iloc[p1:p2, i]
                # predictions  # DBE-KT22-sub 5: 8   18   26   36   44  # 22  40  62  84  104  # DBE-KT22-sub 10_b: 22  44  68  90  114
                # testtest10: 20  44  66  88  110  DBE-KT22-sub 10_f: 18  40  64  86  106
                true = df.iloc[p1:p2, 8]  # ground truth
                # print("true: ", true)
                # print("pred: ", pred)
                # Calculate metrics

                auroc = metrics.roc_auc_score(true, pred)
                auprc = metrics.average_precision_score(true, pred)
                # Print metrics
                print(f"Metrics for column {i + 1}:")
                # Check if the result is binary
                # print(len(np.unique(pred)))
                # print(len(np.unique(true)))

                # if count % 2 == 0 and '_f' not in sheet:
                #     accuracy = metrics.accuracy_score(true, pred)
                #     recall = metrics.recall_score(true, pred)
                #     precision = metrics.precision_score(true, pred)
                #     print(f"Accuracy: {accuracy}")
                #     print(f"Recall: {recall}")
                #     print(f"Precision: {precision}")

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