import random

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, hamming_loss, f1_score
from sklearn.metrics import precision_score, recall_score
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
import json
import ast
import csv
import glob, os
from .eval_pipeline import write_to_json
import re


class Metric:
    def __init__(self):
        self.score = None

    def measure(self, test_case, batch_size):
        raise NotImplementedError


class HitAtOneMetric(Metric):
    def __init__(self):
        super().__init__()

    def measure(self, test_case, batch_size=1):
        # Sample data: Each tuple is (predicted_answer, actual_answer, input_question_to_LLMs)
        hits = 0
        assert len(test_case) == batch_size

        for predicted, actual, _ in test_case:
            if predicted == actual:
                hits += 1

        self.score = hits / batch_size
        return self.score

    def by_case_measure(self, test_case, batch_size=1, all_negatives=False, csv_column=False):
        # Sample data: Each tuple is (predicted_answer, actual_answer, input_question_to_LLMs)
        yes_keywords = ["yes", "certainly", "definitely", "of course", "sure", "是的", "当然是", "正确"]
        no_keywords = ["no", "no way", "not at all", "certainly not", "never", "不", "不是", "错误"]

        hits = 0
        assert len(test_case) == batch_size
        if not csv_column:
            if all_negatives:
                for predicted, actual,_ in test_case:
                    if any(re.search(r'\b' + keyword + r'\b', str(predicted).lower()) for keyword in no_keywords):
                        hits += 1
                    # if 'no' in predicted.lower() or predicted == actual or '否' in predicted or '不' in predicted:
                    #     hits += 1
            else:
                for predicted, actual, _ in test_case:
                    if any(re.search(r'\b' + keyword + r'\b', str(predicted).lower()) for keyword in yes_keywords):
                        hits += 1
                    # if 'yes' in predicted.lower() or predicted == actual or '是' in predicted:
                    #     hits += 1
        else:
            if all_negatives:
                for predicted in test_case:
                    if any(re.search(r'\b' + keyword + r'\b', str(predicted).lower()) for keyword in no_keywords):
                        hits += 1
                    # if 'no' in predicted.lower() or '否' in predicted or '不' in predicted:
                    #     hits += 1
            else:
                for predicted in test_case:
                    if any(re.search(r'\b' + keyword + r'\b', str(predicted).lower()) for keyword in yes_keywords):
                        hits += 1
                    # if 'yes' in predicted.lower() or '是' in predicted:
                    #     hits += 1

        self.score = hits / batch_size
        return self.score


    def mixed_case_measure(self, test_case, gt, batch_size=1, csv_column=False):
        # Sample data: Each tuple is (predicted_answer, actual_answer, input_question_to_LLMs)
        yes_keywords = ["yes", "certainly", "definitely", "of course", "sure", "是的", "当然是", "正确"]
        no_keywords = ["no", "no way", "not at all", "certainly not", "never", "不", "不是", "错误"]

        hits = 0
        assert len(test_case) == batch_size
        if not csv_column:
            for (predicted, actual, _), gt_row in zip(test_case, gt):
                if gt_row == 0:
                    if any(re.search(r'\b' + keyword + r'\b', str(predicted).lower()) for keyword in no_keywords):
                        hits += 1
                    # if 'no' in predicted.lower() or predicted == actual or '否' in predicted or '不' in predicted:
                    #     hits += 1
                else:
                    if any(re.search(r'\b' + keyword + r'\b', str(predicted).lower()) for keyword in yes_keywords):
                        hits += 1
                    # if 'yes' in predicted.lower() or predicted == actual or '是' in predicted:
                    #     hits += 1
        else:
            for predicted, gt_row in zip(test_case, gt):
                if gt_row == 0:
                    if any(re.search(r'\b' + keyword + r'\b', str(predicted).lower()) for keyword in no_keywords):
                        hits += 1
                else:
                    if any(re.search(r'\b' + keyword + r'\b', str(predicted).lower()) for keyword in yes_keywords):
                        hits += 1
                # if 'yes' in predicted.lower() or '是' in predicted:
                #     hits += 1

        self.score = hits / batch_size
        return self.score


class RelationPredictionMetric(Metric):
    def __init__(self):
        super().__init__()

    def measure(self, test_case, batch_size=1, threshold=0.5):
        # Sample data: Each tuple is (predicted_relation, actual_relation, input_question_to_LLMs)
        # the predicted and actual relations are the same dimension: (n_nodes, n_nodes)

        assert len(test_case) == batch_size, f"Batch size is {batch_size}, but now they are {len(test_case)}."
        auroc_list = []
        auprc_list = []
        accuracy_list = []
        hamming_list = []
        f1_list = []
        for predicted, actual, _ in test_case:
            ground_truth = np.array(actual).flatten()
            predicted = np.array(predicted).flatten()
            predicted_binarized = np.where(predicted >= threshold, 1, 0)

            auroc_list.append(roc_auc_score(ground_truth, predicted))
            auprc_list.append(average_precision_score(ground_truth, predicted))
            accuracy_list.append(accuracy_score(ground_truth, predicted_binarized))
            hamming_list.append(hamming_loss(ground_truth, predicted_binarized))
            f1_list.append(f1_score(ground_truth, predicted_binarized))

        self.score = {
            "AUROC": np.mean(auroc_list),
            "AUPRC": np.mean(auprc_list),
            "Accuracy": np.mean(accuracy_list),
            "Hamming Loss": np.mean(hamming_list),
            "F1": np.mean(f1_list)
        }

        return self.score

    def measure_binary(self, test_case, batch_size=1):
        # Sample data: Each tuple is (predicted_relation, actual_relation, input_question_to_LLMs)
        # different from the above method, this method is used for binary classification.
        # So each edge has a label of 0 or 1 in the predicted and actual relations.
        assert len(test_case) == batch_size, f"Batch size is {batch_size}, but now they are {len(test_case)}."
        auroc_list = []
        auprc_list = []
        accuracy_list = []
        hamming_list = []
        f1_list = []
        for predicted, actual, _ in test_case:
            ground_truth = np.array(actual).flatten()
            predicted = np.array(predicted).flatten()

            auroc_list.append(roc_auc_score(ground_truth, predicted))
            auprc_list.append(average_precision_score(ground_truth, predicted))
            accuracy_list.append(accuracy_score(ground_truth, predicted))
            hamming_list.append(hamming_loss(ground_truth, predicted))
            f1_list.append(f1_score(ground_truth, predicted))

        self.score = {
            "AUROC": np.mean(auroc_list),
            "AUPRC": np.mean(auprc_list),
            "Accuracy": np.mean(accuracy_list),
            "Hamming Loss": np.mean(hamming_list),
            "F1": np.mean(f1_list)
        }

        return self.score


class LLMKGAnswerRelevancyMetric(Metric):
    def __init__(self):
        super().__init__()

    def measure(self, test_case, batch_size=1, threshold=0.7):
        # Sample data: Each tuple is (predicted_answer, actual_answer, input_question_to_LLMs)

        assert len(test_case) == batch_size, f"Batch size is {batch_size}, but now they are {len(test_case)}."
        relevancy_metric = AnswerRelevancyMetric(
            threshold=threshold,
            include_reason=True
        )
        relevancy_scores = []
        test_cases = []
        for predicted, actual, input_question in test_case:
            test_cases.append(LLMTestCase(
                input=input_question,
                actual_output=actual
            ))
        dataset = EvaluationDataset(
            alias="LLMs on KGs Relevancy Evaluation",
            test_cases=test_cases
        )

        self.score = dataset.evaluate([relevancy_metric])
        return self.score


class LLMKGHallucinationMetric(Metric):
    def __init__(self):
        super().__init__()

    def measure(self, test_case, batch_size, threshold=0.5, task="one-hop reasoning", language="en"):
        # Sample data: Each tuple is (predicted_answer, actual_answer, input_question_to_LLMs)
        assert len(test_case) == batch_size, f"Batch size is {batch_size}, but now they are {len(test_case)}."
        hallucination_metric = HallucinationMetric(
            threshold=threshold,
            include_reason=True
        )
        context = self.get_context(task, language)
        test_cases = []
        for predicted, actual, input_question in test_case:
            test_cases.append(LLMTestCase(
                input=input_question,
                actual_output=actual,
                context=context
            ))
        dataset = EvaluationDataset(
            alias="LLMs on KGs Hallucination Evaluation",
            test_cases=test_cases
        )
        self.score = dataset.evaluate([hallucination_metric])
        return self.score

    def get_context(self, task, language="en"):
        if language == "en":
            if task == "one-hop reasoning":
                return ["One-hop reasoning on an Educational Knowledge Graph."]
            elif task == "two-hop reasoning":
                return ["Two-hop reasoning on an Educational Knowledge Graph."]
            elif task == "three-hop reasoning":
                return ["Three-hop reasoning on an Educational Knowledge Graph."]
            elif task == "relation extraction":
                return ["Relation extraction for an Educational Knowledge Graph."]
            elif task == "conjunction with two predecessors":
                return ["One-hop reasoning on an Educational Knowledge Graph for nodes with two predecessors."]
            elif task == "conjunction with three predecessors":
                return ["One-hop reasoning on an Educational Knowledge Graph for nodes with three predecessors."]
            else:
                return ["Tasks on an Educational Knowledge Graph."]
        elif language == "zh":
            if task == "one-hop reasoning":
                return ["教育知识图上的一跳推理。"]
            elif task == "two-hop reasoning":
                return ["教育知识图上的二跳推理。"]
            elif task == "three-hop reasoning":
                return ["教育知识图上的三跳推理。"]
            elif task == "relation extraction":
                return ["教育知识图上的关联提取。"]
            elif task == "conjunction with two predecessors":
                return ["具有两个前置节点的教育知识图上的一跳推理。"]
            elif task == "conjunction with three predecessors":
                return ["具有三个前置节点的教育知识图上的一跳推理。"]
            else:
                return ["大语言模型在教育知识图上的任务。"]
        else:
            return "Not implemented yet."


class LLMKGTopKMetric(Metric):
    def __init__(self):
        super().__init__()

    def measure(self, test_case, batch_size, threshold=0.5, k=5):
        # Sample data: Each tuple is (predicted_answer, actual_answer, input_question_to_LLMs)
        assert len(test_case) == batch_size, f"Batch size is {batch_size}, but now they are {len(test_case)}."
        topk_precision_list = []
        topk_recall_list = []
        topk_accuracy_list = []
        for predicted, actual, _ in test_case:
            ground_truth = np.array(actual).flatten()
            predicted = np.array(predicted).flatten()
            topk_indices = np.argsort(predicted)[: k]
            topk_true = ground_truth[topk_indices]
            topk_pred = np.ones(k)

            # Calculate precision and recall
            precision_k = precision_score(topk_true, topk_pred, zero_division=0)
            recall_k = recall_score(topk_true, topk_pred, zero_division=0)
            accuracy_k = np.mean(topk_true == topk_pred)

            topk_precision_list.append(precision_k)
            topk_recall_list.append(recall_k)
            topk_accuracy_list.append(accuracy_k)

        self.score = {
            "Top-K Precision": np.mean(topk_precision_list),
            "Top-K Recall": np.mean(topk_recall_list),
            "Top-K Accuracy": np.mean(topk_accuracy_list)
        }

        return self.score


class ReadQuestionsFromLocal:
    def __init__(self, path, save_root=None):
        """
        :param path: default_path to the graphml file
        """
        self.path = path
        self.dataset_default = path.split('/')[-1].split('.')[0]
        self.zh_flag = "WDKG" in self.dataset_default
        self.questions_directory = 'logs/questions/' + self.dataset_default + '/'
        self.processed_data_directory = 'logs/processed_data/' + self.dataset_default + '/'
        self.questions = self.list_files_glob(self.questions_directory)
        self.processed_data = self.list_files_glob(self.processed_data_directory)
        self.save_root = save_root

    def read(self):
        df = pd.read_csv(self.path)
        return df

    def list_files_glob(self, directory):
        """ Returns a list of all files in the given directory using glob """
        # Path pattern to match all files in the directory
        # Use '*.ext' to match files with a specific extension
        path_pattern = directory + '/*'  # Matches all files and directories
        files = [file for file in glob.glob(path_pattern) if os.path.isfile(file)]
        return files

    def read_from_json(self, path):
        if not self.zh_flag:
            with open(path, 'r') as file:
                data = json.load(file)
        else:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        return data

    def convert_strings_to_bools(self, data):
        """
        Recursively convert 'True' and 'False' strings in a nested list to boolean values.

        Parameters:
        - data (list): A nested list possibly containing 'True' and 'False' strings.

        Returns:
        - list: A nested list with 'True' and 'False' strings converted to boolean values.
        """
        if isinstance(data, list):
            return [self.convert_strings_to_bools(item) for item in data]
        elif data == 'True':
            return True
        elif data == 'False':
            return False
        else:
            return data

    def convert_nested_strings_to_tuples(self, data):
        """
        Recursively convert string representations of tuples in a nested list to actual tuples.

        Parameters:
            data (list): The nested list potentially containing string representations of tuples.

        Returns:
            list: A nested list with string tuples converted to actual tuples.
        """
        if isinstance(data, list):
            # Recursively process each item in the list
            return [self.convert_nested_strings_to_tuples(item) for item in data]
        elif isinstance(data, str):
            # Try to convert strings that represent tuples
            try:
                # Use ast.literal_eval to safely evaluate the string
                evaluated = ast.literal_eval(data)
                # Check if the evaluated result is indeed a tuple
                if isinstance(evaluated, tuple):
                    return evaluated  # Keep as tuple
                return evaluated
            except (SyntaxError, ValueError):
                # Return the data unchanged if it's not a string tuple
                return data
        else:
            # Return the data unchanged if it's not a list or string
            return data

    def read_from_csv(self, path):
        full_list = []
        # Open the CSV file
        with open(path, newline='') as csvfile:
            # Create a reader object which will read from the opened file
            reader = csv.reader(csvfile)

            # Iterate over each row in the CSV file
            for row in reader:
                # Append each row to the list
                full_list.append(row)

        # Convert the nested list to tuples is necessary
        full_list = self.convert_nested_strings_to_tuples(full_list)

        # Convert the 'True' and 'False' strings to boolean values
        full_list = self.convert_strings_to_bools(full_list)

        return full_list

    def get_basic_length(self, negative=False):
        """
        Get the basic length of the dataset
        """
        one_hop_questions = []
        for question in self.questions:
            if 'one-hop' in question:
                one_hop_questions.append(question)
        one_hop_questions = [s for s in one_hop_questions if 'shot' not in s]

        if not negative:
            one_hop_questions = [s for s in one_hop_questions if 'negative' not in s]
        else:
            one_hop_questions = [s for s in one_hop_questions if 'negative' in s]

        data_dict = {}
        for path in one_hop_questions:
            try:
                data = self.read_from_json(path)
            except FileNotFoundError:
                print(f"File not found: {path}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {path}")
            if len(data) != 0:
                break
        return len(data)

    def sample_n_from_x(self, elements, n, x):
        """
        Randomly sample n elements from every x elements in the list.

        Parameters:
            elements (list): The list from which to sample.
            n (int): The number of elements to sample from each segment.
            x (int): The segment size to consider for each sampling.

        Returns:
            list: A list containing the sampled elements.
            list: A list of indices of the sampled elements.
        """
        sampled_elements = []
        sampled_indices = []
        # Iterate over the list in steps of x
        for i in range(0, len(elements), x):
            # Get the current segment
            segment = elements[i:i + x]
            segment_length = len(segment)

            # Calculate current segment's indices
            current_indices = range(i, i + segment_length)

            # Determine the number of elements to sample based on segment size
            num_samples = min(n, segment_length)

            # Sample indices from the current segment
            sampled_segment_indices = random.sample(current_indices, num_samples)

            # Map sampled indices to their respective elements
            sampled_elements.extend(elements[idx] for idx in sampled_segment_indices)
            sampled_indices.extend(sampled_segment_indices)

        return sampled_elements, sampled_indices

    def read_one_hop(self, one_shot=False, negative=False, sampling=False, samples=50, use_sampled=False):
        """
        Read the one-hop questions from the local directory
        """

        if one_shot:
            samples = int(samples / 10)
        # print(self.questions)
        one_hop_questions = []
        basic_length = self.get_basic_length(negative)
        for question in self.questions:
            if 'one-hop' in question:
                one_hop_questions.append(question)
        if not one_shot:
            one_hop_questions = [s for s in one_hop_questions if 'shot' not in s]
        else:
            one_hop_questions = [s for s in one_hop_questions if 'shot' in s]
        if not negative:
            one_hop_questions = [s for s in one_hop_questions if 'negative' not in s]
        else:
            one_hop_questions = [s for s in one_hop_questions if 'negative' in s]

        if not use_sampled:
            data_dict = {}
            len_cache = 0
            indices = []
            for path in one_hop_questions:
                try:
                    data_cache = self.read_from_json(path)
                    len_file = len(data_cache)
                    if len(indices) == 0:
                        if not one_shot:
                            if sampling and len_file > samples:
                                indices = random.sample(range(len_file), samples)
                                data_cache = [data_cache[i] for i in indices]
                        else:
                            if sampling and len_file > samples:
                                data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                        data_dict[path] = data_cache
                        len_cache = len(data_cache)
                    else:
                        if len_file != len_cache:
                            if not one_shot:
                                if sampling and len_file > samples:
                                    indices = random.sample(range(len_file), samples)
                                    data_cache = [data_cache[i] for i in indices]
                            else:
                                if sampling and len_file > samples:
                                    data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                            data_dict[path] = data_cache
                            len_cache = len(data_cache)
                        else:
                            data_dict[path] = [data_cache[i] for i in indices]
                    # ['logs/questions/DBE-KT22/one-hop-questions.json',
                    # 'logs/questions/DBE-KT22/one-hop-questions_w_triplets.json']
                    parts = path.split('/')
                    parts.insert(-1, 'sampled')
                    path_sampled = '/'.join(parts)
                    write_to_json(data_dict[path], path_sampled)

                except FileNotFoundError:
                    print(f"File not found: {path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path}")
        else:
            data_dict = {}
            for path in one_hop_questions:
                parts = path.split('/')
                parts.insert(-1, 'sampled')
                path_sampled = '/'.join(parts)
                try:
                    data_cache = self.read_from_json(path_sampled)
                    data_dict[path] = data_cache
                except FileNotFoundError:
                    print(f"File not found: {path_sampled}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path_sampled}")
        print("---One-hop questions read.---")
        return data_dict

    def read_two_hop(
            self,
            one_shot=False,
            negative=False,
            path_distruption=False,
            invert_relations=False,
            replace_intermediate=False,
            replace_terminal=False,
            sampling=False,
            samples=48,
            use_sampled=False
    ):
        """
        Read the two-hop questions from the local directory
        """

        if one_shot:
            samples = int(samples / 10)
        if negative:
            samples = int(samples / 4)
        # print(self.questions)
        two_hop_questions = []
        basic_length = self.get_basic_length(negative)
        for question in self.questions:
            if 'two-hop' in question:
                two_hop_questions.append(question)
        if not one_shot:
            two_hop_questions = [s for s in two_hop_questions if 'shot' not in s]
        else:
            two_hop_questions = [s for s in two_hop_questions if 'shot' in s]
        if not negative:
            two_hop_questions = [s for s in two_hop_questions if 'negative' not in s]
        else:
            two_hop_questions = [s for s in two_hop_questions if 'negative' in s]
        # print("After negative filter")
        # print(two_hop_questions)
        if path_distruption:
            two_hop_questions = [s for s in two_hop_questions if 'path-disruption' in s]
        if invert_relations:
            two_hop_questions = [s for s in two_hop_questions if 'invert-relations' in s]
        if replace_intermediate:
            two_hop_questions = [s for s in two_hop_questions if 'replace-intermediate' in s]
        if replace_terminal:
            two_hop_questions = [s for s in two_hop_questions if 'replace-terminal' in s]
        # print("After second filter")
        # print(two_hop_questions)

        if not use_sampled:
            data_dict = {}
            len_cache = 0
            indices = []
            for path in two_hop_questions:
                try:
                    data_cache = self.read_from_json(path)
                    len_file = len(data_cache)
                    if len(indices) == 0:
                        if not one_shot:
                            if sampling and len_file > samples:
                                indices = random.sample(range(len_file), samples)
                                data_cache = [data_cache[i] for i in indices]
                        else:
                            if sampling and len_file > samples:
                                data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                        data_dict[path] = data_cache
                        len_cache = len(data_cache)
                    else:
                        if len_file != len_cache:
                            if not one_shot:
                                if sampling and len_file > samples:
                                    indices = random.sample(range(len_file), samples)
                                    data_cache = [data_cache[i] for i in indices]
                            else:
                                if sampling and len_file > samples:
                                    data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                            data_dict[path] = data_cache
                            len_cache = len(data_cache)
                        else:
                            data_dict[path] = [data_cache[i] for i in indices]
                    # ['logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal_w_triplets.json',
                    # 'logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal.json']
                    parts = path.split('/')
                    parts.insert(-1, 'sampled')
                    path_sampled = '/'.join(parts)
                    write_to_json(data_dict[path], path_sampled)

                except FileNotFoundError:
                    print(f"File not found: {path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path}")
        else:
            data_dict = {}
            for path in two_hop_questions:
                parts = path.split('/')
                parts.insert(-1, 'sampled')
                path_sampled = '/'.join(parts)
                try:
                    data_cache = self.read_from_json(path_sampled)
                    data_dict[path] = data_cache
                except FileNotFoundError:
                    print(f"File not found: {path_sampled}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path_sampled}")
        print("---Two-hop questions read.---")
        return data_dict

    def read_three_hop(
            self,
            one_shot=False,
            negative=False,
            sampling=False,
            samples=25,
            use_sampled=False
    ):
        """
        Read the two-hop questions from the local directory
        """

        if one_shot:
            samples = int(samples / 10)
        # if negative:
            # samples = int(samples / 4)
        # print(self.questions)
        three_hop_questions = []
        basic_length = self.get_basic_length(negative)
        for question in self.questions:
            if 'three-hop' in question:
                three_hop_questions.append(question)
        if not one_shot:
            three_hop_questions = [s for s in three_hop_questions if 'shot' not in s]
        else:
            three_hop_questions = [s for s in three_hop_questions if 'shot' in s]
        if not negative:
            three_hop_questions = [s for s in three_hop_questions if 'negative' not in s]
        else:
            three_hop_questions = [s for s in three_hop_questions if 'negative' in s]
        # print("After negative filter")
        # print(three_hop_questions)
        # print("After second filter")
        # print(three_hop_questions)

        if not use_sampled:
            data_dict = {}
            len_cache = 0
            indices = []
            for path in three_hop_questions:
                try:
                    data_cache = self.read_from_json(path)
                    len_file = len(data_cache)
                    if len(indices) == 0:
                        if not one_shot:
                            if sampling and len_file > samples:
                                indices = random.sample(range(len_file), samples)
                                data_cache = [data_cache[i] for i in indices]
                        else:
                            if sampling and len_file > samples:
                                data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                        data_dict[path] = data_cache
                        len_cache = len(data_cache)
                    else:
                        if len_file != len_cache:
                            if not one_shot:
                                if sampling and len_file > samples:
                                    indices = random.sample(range(len_file), samples)
                                    data_cache = [data_cache[i] for i in indices]
                            else:
                                if sampling and len_file > samples:
                                    data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                            data_dict[path] = data_cache
                            len_cache = len(data_cache)
                        else:
                            data_dict[path] = [data_cache[i] for i in indices]
                    # ['logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal_w_triplets.json',
                    # 'logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal.json']
                    parts = path.split('/')
                    parts.insert(-1, 'sampled')
                    path_sampled = '/'.join(parts)
                    write_to_json(data_dict[path], path_sampled)

                except FileNotFoundError:
                    print(f"File not found: {path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path}")
        else:
            data_dict = {}
            for path in three_hop_questions:
                parts = path.split('/')
                parts.insert(-1, 'sampled')
                path_sampled = '/'.join(parts)
                try:
                    data_cache = self.read_from_json(path_sampled)
                    data_dict[path] = data_cache
                except FileNotFoundError:
                    print(f"File not found: {path_sampled}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path_sampled}")
        print("---Three-hop questions read.---")
        return data_dict

    def read_two_predecessor(
            self,
            one_shot=False,
            negative=False,
            p0=False,
            p1=False,
            two=False,
            sampling=False,
            samples=30,
            use_sampled=False
    ):
        """
        Read the two-hop questions from the local directory
        """

        if one_shot:
            samples = int(samples / 10)
        # if negative:
            # samples = int(samples / 4)
        # print(self.questions)
        two_predecessor_questions = []
        basic_length = self.get_basic_length(negative)
        for question in self.questions:
            if 'two-predecessors' in question:
                two_predecessor_questions.append(question)
        if not one_shot:
            two_predecessor_questions = [s for s in two_predecessor_questions if 'shot' not in s]
        else:
            two_predecessor_questions = [s for s in two_predecessor_questions if 'shot' in s]
        if not negative:
            two_predecessor_questions = [s for s in two_predecessor_questions if 'negative' not in s]
        else:
            two_predecessor_questions = [s for s in two_predecessor_questions if 'negative' in s]

        if p0:
            two_predecessor_questions = [s for s in two_predecessor_questions if 'p0' in s]
        if p1:
            two_predecessor_questions = [s for s in two_predecessor_questions if 'p1' in s]
        if two:
            two_predecessor_questions = [s for s in two_predecessor_questions if 'negative-two' in s]
        # print("After negative filter")
        # print(two_predecessor_questions)
        # print("After second filter")
        # print(two_predecessor_questions)

        if not use_sampled:
            data_dict = {}
            len_cache = 0
            indices = []
            for path in two_predecessor_questions:
                try:
                    data_cache = self.read_from_json(path)
                    len_file = len(data_cache)
                    if len(indices) == 0:
                        if not one_shot:
                            if sampling and len_file > samples:
                                indices = random.sample(range(len_file), samples)
                                data_cache = [data_cache[i] for i in indices]
                            else:
                                indices = random.sample(range(len_file), len_file)
                                data_cache = [data_cache[i] for i in indices]
                        else:
                            if sampling and len_file > samples:
                                data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                            else:
                                data_cache, indices = self.sample_n_from_x(data_cache, len_file, basic_length)
                        data_dict[path] = data_cache
                        len_cache = len(data_cache)
                    else:
                        if len_file != len_cache:
                            if not one_shot:
                                if sampling and len_file > samples:
                                    indices = random.sample(range(len_file), samples)
                                    data_cache = [data_cache[i] for i in indices]
                                else:
                                    indices = random.sample(range(len_file), len_file)
                                    data_cache = [data_cache[i] for i in indices]
                            else:
                                if sampling and len_file > samples:
                                    data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                                else:
                                    data_cache, indices = self.sample_n_from_x(data_cache, len_file, basic_length)
                            data_dict[path] = data_cache
                            len_cache = len(data_cache)
                        else:
                            data_dict[path] = [data_cache[i] for i in indices]
                    # ['logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal_w_triplets.json',
                    # 'logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal.json']
                    parts = path.split('/')
                    parts.insert(-1, 'sampled')
                    path_sampled = '/'.join(parts)
                    write_to_json(data_dict[path], path_sampled)

                except FileNotFoundError:
                    print(f"File not found: {path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path}")
        else:
            data_dict = {}
            for path in two_predecessor_questions:
                parts = path.split('/')
                parts.insert(-1, 'sampled')
                path_sampled = '/'.join(parts)
                try:
                    data_cache = self.read_from_json(path_sampled)
                    data_dict[path] = data_cache
                except FileNotFoundError:
                    print(f"File not found: {path_sampled}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path_sampled}")
        print("---Two-predecessors questions read.---")
        return data_dict

    def read_three_predecessor(
            self,
            one_shot=False,
            negative=False,
            one_p0=False,
            one_p1=False,
            one_p2=False,
            two_p01=False,
            two_p02=False,
            two_p12=False,
            three=False,
            sampling=False,
            samples=30,
            use_sampled=False
    ):
        """
        Read the two-hop questions from the local directory
        """

        if one_shot:
            samples = int(samples / 10)
        # if negative:
            # samples = int(samples / 4)
        # print(self.questions)
        three_predecessor_questions = []
        basic_length = self.get_basic_length(negative)
        for question in self.questions:
            if 'three-predecessors' in question:
                three_predecessor_questions.append(question)
        if not one_shot:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'shot' not in s]
        else:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'shot' in s]
        if not negative:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'negative' not in s]
        else:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'negative' in s]

        if one_p0:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'one-p0' in s]
        if one_p1:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'one-p1' in s]
        if one_p2:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'one-p2' in s]
        if two_p01:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'two-p01' in s]
        if two_p02:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'two-p02' in s]
        if two_p12:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'two-p12' in s]
        if three:
            three_predecessor_questions = [s for s in three_predecessor_questions if 'negative-three' in s]
        # print("After negative filter")
        # print(three_predecessor_questions)
        # print("After second filter")
        # print(three_predecessor_questions)

        if not use_sampled:
            data_dict = {}
            len_cache = 0
            indices = []
            for path in three_predecessor_questions:
                try:
                    data_cache = self.read_from_json(path)
                    len_file = len(data_cache)
                    if len(indices) == 0:
                        if not one_shot:
                            if sampling and len_file > samples:
                                indices = random.sample(range(len_file), samples)
                                data_cache = [data_cache[i] for i in indices]
                        else:
                            if sampling and len_file > samples:
                                data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                        data_dict[path] = data_cache
                        len_cache = len(data_cache)
                    else:
                        if len_file != len_cache:
                            if not one_shot:
                                if sampling and len_file > samples:
                                    indices = random.sample(range(len_file), samples)
                                    data_cache = [data_cache[i] for i in indices]
                            else:
                                if sampling and len_file > samples:
                                    data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                            data_dict[path] = data_cache
                            len_cache = len(data_cache)
                        else:
                            data_dict[path] = [data_cache[i] for i in indices]
                    # ['logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal_w_triplets.json',
                    # 'logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal.json']
                    parts = path.split('/')
                    parts.insert(-1, 'sampled')
                    path_sampled = '/'.join(parts)
                    write_to_json(data_dict[path], path_sampled)

                except FileNotFoundError:
                    print(f"File not found: {path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path}")
        else:
            data_dict = {}
            for path in three_predecessor_questions:
                parts = path.split('/')
                parts.insert(-1, 'sampled')
                path_sampled = '/'.join(parts)
                try:
                    data_cache = self.read_from_json(path_sampled)
                    data_dict[path] = data_cache
                except FileNotFoundError:
                    print(f"File not found: {path_sampled}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path_sampled}")
        print("---Three-predecessors questions read.---")
        return data_dict

    def read_node_pairs(
            self,
            one_shot=False,
            sampling=False,
            samples=30,
            use_sampled=False
    ):
        """
        Read the two-hop questions from the local directory
        """
        # if negative:
            # samples = int(samples / 4)
        # print(self.questions)
        node_pair_questions = []
        basic_length = self.get_basic_length()
        for question in self.questions:
            if 'node-pairs' in question:
                node_pair_questions.append(question)
        if not one_shot:
            node_pair_questions = [s for s in node_pair_questions if 'shot' not in s]
        else:
            node_pair_questions = [s for s in node_pair_questions if 'shot' in s]

        # print("After negative filter")
        # print(node_pair_questions)
        # print("After second filter")
        # print(node_pair_questions)

        if not use_sampled:
            data_dict = {}
            len_cache = 0
            indices = []
            for path in node_pair_questions:
                try:
                    data_cache = self.read_from_json(path)
                    # print("Data cache")
                    # print(data_cache)
                    # print(len(data_cache))
                    len_file = len(data_cache)
                    if len(indices) == 0:
                        # print("one_shot: ", one_shot)
                        # print("sampling: ", sampling)
                        # print("len_file: ", len_file)
                        if not one_shot:
                            if sampling and len_file > samples:
                                indices = random.sample(range(len_file), samples)
                                data_cache = [data_cache[i] for i in indices]
                                # print(indices)
                        else:
                            if sampling and len_file > samples:
                                data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                        data_dict[path] = data_cache
                        len_cache = len(data_cache)
                        # print("After sampling: ", len(data_cache))
                    else:
                        if len_file != len_cache:
                            if not one_shot:
                                if sampling and len_file > samples:
                                    indices = random.sample(range(len_file), samples)
                                    data_cache = [data_cache[i] for i in indices]
                            else:
                                if sampling and len_file > samples:
                                    data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                            data_dict[path] = data_cache
                            len_cache = len(data_cache)
                        else:
                            data_dict[path] = [data_cache[i] for i in indices]
                    # ['logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal_w_triplets.json',
                    # 'logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal.json']
                    parts = path.split('/')
                    parts.insert(-1, 'sampled')
                    path_sampled = '/'.join(parts)
                    write_to_json(data_dict[path], path_sampled)

                except FileNotFoundError:
                    print(f"File not found: {path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path}")
        else:
            data_dict = {}
            for path in node_pair_questions:
                parts = path.split('/')
                parts.insert(-1, 'sampled')
                path_sampled = '/'.join(parts)
                try:
                    data_cache = self.read_from_json(path_sampled)
                    data_dict[path] = data_cache
                except FileNotFoundError:
                    print(f"File not found: {path_sampled}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path_sampled}")
        print("---Node-pair questions read.---")
        return data_dict

    def read_sub_graph(
            self,
            one_shot=False,
            size_5=False,
            size_10=False,
            size_15=False,
            sampling=False,
            samples=5,
            use_sampled=False
    ):
        """
        Read the two-hop questions from the local directory
        """

        if one_shot:
            samples = int(samples / 10)
        # if negative:
            # samples = int(samples / 4)
        # print(self.questions)
        sub_graph_questions = []
        basic_length = self.get_basic_length()
        for question in self.questions:
            if 'sub-graph' in question:
                sub_graph_questions.append(question)
        if not one_shot:
            sub_graph_questions = [s for s in sub_graph_questions if 'shot' not in s]
        else:
            sub_graph_questions = [s for s in sub_graph_questions if 'shot' in s]

        if size_5:
            sub_graph_questions = [s for s in sub_graph_questions if 'size-5' in s]
        if size_10:
            sub_graph_questions = [s for s in sub_graph_questions if 'size-10' in s]
        if size_15:
            sub_graph_questions = [s for s in sub_graph_questions if 'size-15' in s]
        # print("After negative filter")
        # print(sub_graph_questions)
        # print("After second filter")
        # print(sub_graph_questions)

        if not use_sampled:
            data_dict = {}
            len_cache = 0
            indices = []
            for path in sub_graph_questions:
                try:
                    data_cache = self.read_from_json(path)
                    len_file = len(data_cache)
                    if len(indices) == 0:
                        if not one_shot:
                            if sampling and len_file > samples:
                                indices = random.sample(range(len_file), samples)
                                data_cache = [data_cache[i] for i in indices]
                        else:
                            if sampling and len_file > samples:
                                data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                        data_dict[path] = data_cache
                        len_cache = len(data_cache)
                    else:
                        if len_file != len_cache:
                            if not one_shot:
                                if sampling and len_file > samples:
                                    indices = random.sample(range(len_file), samples)
                                    data_cache = [data_cache[i] for i in indices]
                            else:
                                if sampling and len_file > samples:
                                    data_cache, indices = self.sample_n_from_x(data_cache, samples, basic_length)
                            data_dict[path] = data_cache
                            len_cache = len(data_cache)
                        else:
                            data_dict[path] = [data_cache[i] for i in indices]
                    # ['logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal_w_triplets.json',
                    # 'logs/questions/DBE-KT22/two-hop-negative-questions-replace-terminal.json']
                    parts = path.split('/')
                    parts.insert(-1, 'sampled')
                    path_sampled = '/'.join(parts)
                    write_to_json(data_dict[path], path_sampled)

                except FileNotFoundError:
                    print(f"File not found: {path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path}")
        else:
            data_dict = {}
            for path in sub_graph_questions:
                parts = path.split('/')
                parts.insert(-1, 'sampled')
                path_sampled = '/'.join(parts)
                try:
                    data_cache = self.read_from_json(path_sampled)
                    data_dict[path] = data_cache
                except FileNotFoundError:
                    print(f"File not found: {path_sampled}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {path_sampled}")
        print("---Node-pair questions read.---")
        return data_dict


