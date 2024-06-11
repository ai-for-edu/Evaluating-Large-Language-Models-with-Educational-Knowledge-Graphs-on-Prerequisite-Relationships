from Edu_KG_Eval.eval_utils import *
import pandas as pd
import glob
from eval_results import *
import numpy as np
from sklearn.metrics import accuracy_score
import re
from itertools import combinations
from collections import defaultdict


def list_files_glob(directory):
    """ Returns a list of all files in the given directory using glob """
    # Path pattern to match all files in the directory
    # Use '*.ext' to match files with a specific extension
    path_pattern = directory + '/*'  # Matches all files and directories
    files = [file for file in glob.glob(path_pattern) if os.path.isfile(file)]
    return files


def access_variable_by_name(var_name):
    return globals()[var_name]


def sort_key(file, order):
    for i, model in enumerate(order):
        if model in file:
            return i
    return len(order)  # I


def are_similar(name1, name2):
    # Normalize by removing 'negative-' if present
    normalized1 = re.sub(r'negative-', '', name1)
    normalized2 = re.sub(r'negative-', '', name2)
    return normalized1 == normalized2


def group_nega_two_hop(vector_names):
    # Regex pattern to extract identifiers like DBE_KT22
    pattern = re.compile(r"^(DBE_KT22|WDKG_Course|Junyi_Prerequisites)")

    # Initialize a dictionary to hold grouped vectors
    grouped_vectors = defaultdict(list)

    # Simulating vectors with random data
    vector_data = {
        name: [1, 2, 3]  # Replace this with your actual vector data
        for name in vector_names
    }

    # Grouping the vectors based on extracted identifiers
    for name, vector in vector_data.items():
        match = pattern.match(name)
        if match:
            identifier = match.group(1)
            grouped_vectors[identifier].append(vector)

    # Concatenating vectors in each group
    from itertools import chain

    concatenated_vectors = {}
    for identifier, vectors in grouped_vectors.items():
        concatenated_vectors[identifier] = list(chain(*vectors))

    # Display concatenated vectors for each group
    for identifier, concatenated_vector in concatenated_vectors.items():
        print(f"{identifier}: {concatenated_vector}")


def test_run():

    negative = False
    all = False
    selected_string = 'two-predecessor'

    directory_answers = 'logs/answers'
    files = list_files_glob(directory_answers)

    if negative and not all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' in file
                 and selected_string in file]

    if not all and not negative:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' not in file
                 and selected_string in file]
    if all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and selected_string in file]


    # print(files)

    order = ['gpt-4', 'qwen-turbo', 'moonshot-v1-128k', 'claude-3-haiku-20240307', 'yi-34b-chat-0205', 'gemini-1.5-pro']

    files.sort()

    def sort_key(file):
        for i, model in enumerate(order):
            if model in file:
                return i
        return len(order)  #

    files = sorted(files, key=sort_key)
    if negative:
        gt = np.zeros(50)
    elif not all:
        gt = np.ones(50)
    else:
        gt = np.concatenate(np.ones(50), np.zeros(50))

    for file in files:
        print('-' * 25)
        # print(file)
        predicted_name = file.split('/')[-1].replace('-json', '').replace('_answer.csv', '').replace('-', '_').replace('.', '_')
        print(predicted_name)
        manual_summary = access_variable_by_name(predicted_name)
        gt = gt[:len(manual_summary)]
        # print(manual_summary)
        print("Manual Accuracy: ", accuracy_score(gt, manual_summary))
        df = pd.read_csv(file)
        answers = df['answer'].values.tolist()
        metric = HitAtOneMetric()
        # for all positive or negative cases
        auto_hit_at_one = metric.by_case_measure(answers, len(answers), csv_column=True, all_negatives=negative)
        # for mixed cases
        # auto_hit_at_one = metric.mixed_case_measure(answers, gt, len(answers), csv_column=True)
        print("Auto Accuracy: ", auto_hit_at_one)
        if negative:
            gt = np.zeros(50)
        else:
            gt = np.ones(50)


def test_run_two_predecessor():
    negative = False
    all = False
    p0 = False
    p1 = False
    two = False

    selected_string = 'two-predecessor'

    directory_answers = 'logs/answers'
    files = list_files_glob(directory_answers)

    if negative and not all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' in file
                 and selected_string in file]

    if not all and not negative:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' not in file
                 and selected_string in file]
    if all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and selected_string in file]

    if p0:
        files = [file for file in files if 'p0' in file]
    if p1:
        files = [file for file in files if 'p1' in file]
    if two:
        files = [file for file in files if 'negative-two' in file]
    # print(files)

    order = ['gpt-4', 'qwen-turbo', 'moonshot-v1-128k', 'claude-3-haiku-20240307', 'yi-34b-chat-0205', 'gemini-1.5-pro']

    files.sort()

    def sort_key(file):
        for i, model in enumerate(order):
            if model in file:
                return i
        return len(order)  #

    files = sorted(files, key=sort_key)
    if negative:
        gt = np.zeros(50)
    elif not all:
        gt = np.ones(50)
    else:
        gt = np.concatenate(np.ones(50), np.zeros(50))

    for file in files:
        print('-' * 25)
        # print(file)
        predicted_name = file.split('/')[-1].replace('-json', '').replace('_answer.csv', '').replace('-', '_').replace(
            '.', '_')
        print(predicted_name)
        manual_summary = access_variable_by_name(predicted_name)
        gt = gt[:len(manual_summary)]
        # print(manual_summary)
        print("Manual Accuracy: ", accuracy_score(gt, manual_summary))
        df = pd.read_csv(file)
        answers = df['answer'].values.tolist()
        metric = HitAtOneMetric()
        # for all positive or negative cases
        auto_hit_at_one = metric.by_case_measure(answers, len(answers), csv_column=True, all_negatives=negative)
        # for mixed cases
        # auto_hit_at_one = metric.mixed_case_measure(answers, gt, len(answers), csv_column=True)
        print("Auto Accuracy: ", auto_hit_at_one)
        if negative:
            gt = np.zeros(50)
        else:
            gt = np.ones(50)


def test_run_three_predecessor():
    negative = True
    all = False
    p0 = False
    p1 = True
    p2 = False
    p01 = False
    p02 = False
    p12 = False
    three = False

    selected_string = 'three-predecessor'

    directory_answers = 'logs/answers'
    files = list_files_glob(directory_answers)

    if negative and not all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' in file
                 and selected_string in file]

    if not all and not negative:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' not in file
                 and selected_string in file]
    if all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and selected_string in file]

    if p0:
        files = [file for file in files if 'one-p0' in file]
    if p1:
        files = [file for file in files if 'one-p1' in file]
    if p2:
        files = [file for file in files if 'one-p2' in file]
    if p01:
        files = [file for file in files if 'p01' in file]
    if p02:
        files = [file for file in files if 'p02' in file]
    if p12:
        files = [file for file in files if 'p12' in file]
    if three:
        files = [file for file in files if 'negative-three' in file]
    # print(files)

    order = ['gpt-4', 'qwen-turbo', 'moonshot-v1-128k', 'claude-3-haiku-20240307', 'yi-34b-chat-0205', 'gemini-1.5-pro']

    files.sort()

    def sort_key(file):
        for i, model in enumerate(order):
            if model in file:
                return i
        return len(order)  #

    files = sorted(files, key=sort_key)
    if negative:
        gt = np.zeros(50)
    elif not all:
        gt = np.ones(50)
    else:
        gt = np.concatenate(np.ones(50), np.zeros(50))

    for file in files:
        print('-' * 25)
        # print(file)
        predicted_name = file.split('/')[-1].replace('-json', '').replace('_answer.csv', '').replace('-', '_').replace(
            '.', '_')
        print(predicted_name)
        manual_summary = access_variable_by_name(predicted_name)
        gt = gt[:len(manual_summary)]
        # print(manual_summary)
        print("Manual Accuracy: ", accuracy_score(gt, manual_summary))
        df = pd.read_csv(file)
        answers = df['answer'].values.tolist()
        metric = HitAtOneMetric()
        # for all positive or negative cases
        auto_hit_at_one = metric.by_case_measure(answers, len(answers), csv_column=True, all_negatives=negative)
        # for mixed cases
        # auto_hit_at_one = metric.mixed_case_measure(answers, gt, len(answers), csv_column=True)
        print("Auto Accuracy: ", auto_hit_at_one)
        if negative:
            gt = np.zeros(50)
        else:
            gt = np.ones(50)


def test_run_two_hop_negatives_concat():

    negative = True
    all = False
    selected_string = 'two-hop'

    directory_answers = 'logs/answers'
    files = list_files_glob(directory_answers)

    if negative and not all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' in file
                 and selected_string in file]

    if not all and not negative:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' not in file
                 and selected_string in file]
    if all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and selected_string in file]

    # print(files)

    order = ['gpt-4', 'qwen-turbo', 'moonshot-v1-128k', 'claude-3-haiku-20240307', 'yi-34b-chat-0205', 'gemini-1.5-pro']

    files.sort()

    def sort_key(file):
        for i, model in enumerate(order):
            if model in file:
                return i
        return len(order)  #

    files = sorted(files, key=sort_key)
    if negative:
        gt = np.zeros(50)
    elif not all:
        gt = np.ones(50)
    else:
        gt = np.concatenate(np.ones(50), np.zeros(50))

    value_dict = {}

    # Keywords
    keywords = ['gpt_4', 'qwen_turbo', 'moonshot_v1_128k', 'claude_3_haiku_20240307', 'yi_34b_chat_0205',
                'gemini_1_5_pro']
    # Initialize dictionary for grouping
    grouped_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    # Grouping logic
    for s in files:
        s = s.split('/')[-1].replace('-json', '').replace('_answer.csv', '').replace('-', '_').replace('.', '_')
        # print(predicted_name)
        segments = s.split('_')
        # print(predicted_name)
        first_two = '_'.join(segments[:2])  # Extract first two segments
        keyword = next((k for k in keywords if s.endswith(k)), None)  # Find the keyword at the end
        triplet_flag = "w_triplets" if "w_triplets" in s else "no_triplets"

        if keyword:
            grouped_data[first_two][keyword][triplet_flag].append(s)

        # gt = gt[:len(manual_summary)]
        # # print(manual_summary)
        # print("Manual Accuracy: ", accuracy_score(gt, manual_summary))
        # df = pd.read_csv(file)
        # answers = df['answer'].values.tolist()
        # metric = HitAtOneMetric()
        # # for all positive or negative cases
        # auto_hit_at_one = metric.by_case_measure(answers, len(answers), csv_column=True, all_negatives=negative)
        # # for mixed cases
        # # auto_hit_at_one = metric.mixed_case_measure(answers, gt, len(answers), csv_column=True)
        # print("Auto Accuracy: ", auto_hit_at_one)
        # if negative:
        #     gt = np.zeros(50)
        # else:
        #     gt = np.ones(50)

    # Display grouped data
    for group, subgroups in grouped_data.items():
        print(f"Group: {group}")
        for keyword, triplet_groups in subgroups.items():
            print(f"  {keyword}:")

            for triplet, items in triplet_groups.items():
                print(f"    {triplet}")
                cache = []
                for i in items:
                    print(f"             : {i}")
                    cache.extend(access_variable_by_name(i))
                # cache.extend(access_variable_by_name(items))
                manual_summary = cache
                gt = gt[:len(manual_summary)]
                print("Manual Accuracy: ", accuracy_score(gt, manual_summary))


def test_run_both_po_ne():
    negative = True
    all = False
    selected_string = 'two-hop'

    directory_answers = 'logs/answers'
    files = list_files_glob(directory_answers)

    if negative and not all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' in file
                 and selected_string in file]

    if not all and not negative:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and 'negative' not in file
                 and selected_string in file]
    if all:
        files = [file for file in files if '.csv' in file and 'gpt-4-turbo' not in file and selected_string in file]



    matched_pairs = []

    def sort_key(file):
        for i, model in enumerate(order):
            if model in file:
                return i
        return len(order)  #

    # The order you want
    order = ['gpt-4', 'qwen-turbo', 'moonshot-v1-128k', 'claude-3-haiku-20240307', 'yi-34b-chat-0205', 'gemini-1.5-pro']

    files.sort()

    files = sorted(files, key=sort_key)

    # Check each combination of files
    for fname1, fname2 in combinations(files, 2):
        if are_similar(fname1, fname2):
            # Ensure the filename containing 'negative' is first
            if 'negative' in fname2:
                matched_pairs.append((fname1, fname2))
            else:
                matched_pairs.append((fname2, fname1))

    # print(matched_pairs)

    gt = np.concatenate((np.ones(50), np.zeros(50)))

    for file1, file2 in matched_pairs:
        # print('-' * 25)
        # print(file)
        predicted_name1 = file1.split('/')[-1].replace('-json', '').replace('_answer.csv', '').replace('-', '_').replace(
            '.', '_')
        # print(predicted_name1)

        predicted_name2 = file2.split('/')[-1].replace('-json', '').replace('_answer.csv', '').replace('-', '_').replace(
            '.', '_')
        # print(predicted_name2)

        manual_summary1 = access_variable_by_name(predicted_name1)
        manual_summary2 = access_variable_by_name(predicted_name2)

        manual_summary = np.concatenate((manual_summary1, manual_summary2))

        # print(manual_summary)
        print("Manual Accuracy: ", accuracy_score(gt, manual_summary))
        df1 = pd.read_csv(file1)
        answers1 = df1['answer'].values.tolist()
        df2 = pd.read_csv(file2)
        answers2 = df2['answer'].values.tolist()
        answers = answers1 + answers2
        metric = HitAtOneMetric()
        # for all positive or negative cases
        auto_hit_at_one = metric.mixed_case_measure(answers, gt, len(answers), csv_column=True)
        # for mixed cases
        # auto_hit_at_one = metric.mixed_case_measure(answers, gt, len(answers), csv_column=True)
        print("Auto Accuracy: ", auto_hit_at_one)


if __name__ == '__main__':
    # test_run_both_po_ne()
    # test_run()
    test_run_two_predecessor()

    # test_run_three_predecessor()

    # test_run_two_hop_negatives_concat()

    # xx = 'logs/answers/WDKG-Course-one-hop-questions-json_qwen-turbo_answer.csv'
    # print(xx.split('/')[-1].replace('-json', '').replace('_answer.csv', '').replace('-', '_'))