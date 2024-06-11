from Edu_KG_Eval.global_config import *
from Edu_KG_Eval import llm_engine
from Edu_KG_Eval.data_preprocessing import DataPreprocessor, matching_betweeness_edges_as_gt, unmatching_query_w_gt
from Edu_KG_Eval.generate_llm_questions import triplet_to_sentence_one_hop_reasoning_one_shot, triplet_to_sentence_w_triplets_one_hop_reasoning_one_shot
from Edu_KG_Eval.generate_llm_questions import triplet_to_sentence_one_hop_reasoning, triplet_to_sentence_w_triplets_one_hop_reasoning
from Edu_KG_Eval.generate_llm_questions import paths_to_sentence_two_hop_reasoning, paths_to_sentence_w_paths_two_hop_reasoning
from Edu_KG_Eval.generate_llm_questions import paths_to_sentence_two_hop_reasoning_one_shot, paths_to_sentence_w_paths_two_hop_reasoning_one_shot
from Edu_KG_Eval.generate_llm_questions import paths_to_sentence_three_hop_reasoning, paths_to_sentence_w_paths_three_hop_reasoning
from Edu_KG_Eval.generate_llm_questions import paths_to_sentence_three_hop_reasoning_one_shot, paths_to_sentence_w_paths_three_hop_reasoning_one_shot
from Edu_KG_Eval.generate_llm_questions import query_2p_to_sentence_one_hop_reasoning, query_2p_to_sentence_w_query_one_hop_reasoning
from Edu_KG_Eval.generate_llm_questions import query_2p_to_sentence_one_hop_reasoning_one_shot, query_2p_to_sentence_w_query_one_hop_reasoning_one_shot
from Edu_KG_Eval.generate_llm_questions import query_3p_to_sentence_one_hop_reasoning, query_3p_to_sentence_w_query_one_hop_reasoning
from Edu_KG_Eval.generate_llm_questions import query_3p_to_sentence_one_hop_reasoning_one_shot, query_3p_to_sentence_w_query_one_hop_reasoning_one_shot
from Edu_KG_Eval.generate_llm_questions import node_pairs_to_sentence_relation_extraction_one_shot, node_pairs_to_sentence_w_float_relation_extraction_one_shot
from Edu_KG_Eval.generate_llm_questions import node_pairs_to_sentence_relation_extraction, node_pairs_to_sentence_w_float_relation_extraction
from Edu_KG_Eval.generate_llm_questions import subgraph_node_pairs_to_sentence_relation_extraction, subgraph_node_pairs_to_sentence_w_float_relation_extraction
from Edu_KG_Eval.generate_llm_questions import subgraph_node_pairs_to_sentence_relation_extraction_one_shot, subgraph_node_pairs_to_sentence_w_float_relation_extraction_one_shot

from Edu_KG_Eval.arg_parser import parse_args
import json
import csv
import os


def write_to_csv(data, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def write_to_json(data, path, zh_flag=False):
    if not zh_flag:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def read_from_json(path, zh_flag=False):
    # Read JSON data from a file
    if not zh_flag:
        with open(path, 'r') as file:
            data = json.load(file)
    else:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    return data


def generate_one_hop_data(args, path):
    print(f"Processing {path} for one-hop data...")
    dataset_default = path.split('/')[-1].split('.')[0]
    zh_flag = False
    if "WDKG" in dataset_default:
        zh_flag = True
    processed_data_directory = 'logs/processed_data/' + dataset_default
    questions_directory = 'logs/questions/' + dataset_default
    data_processor = DataPreprocessor(path)

    # Build the queries both positive and negative
    query = data_processor.construct_graph()
    negative_query = data_processor.construct_graph_negative()

    # get the ones for one-shot reasoning
    selected_edges = data_processor.top_k_betweenness_centrality(k=10)

    x = [d['one_hops'] for d in selected_edges if 'one_hops' in d]
    gt_series = matching_betweeness_edges_as_gt(query, x)

    # save the queries
    query_path = os.path.join(processed_data_directory, 'one-hop-query.csv')
    negative_query_path = os.path.join(processed_data_directory, 'one-hop-negative-query.csv')
    gt_series_path = os.path.join(processed_data_directory, 'one-hop-one-shot-series.csv')

    write_to_csv(query, query_path)
    write_to_csv(negative_query, negative_query_path)
    write_to_csv(gt_series, gt_series_path)

    # generate the questions
    sentences = triplet_to_sentence_one_hop_reasoning(query)
    sentences_f = triplet_to_sentence_w_triplets_one_hop_reasoning(query)

    sentences_n = triplet_to_sentence_one_hop_reasoning(negative_query)
    sentences_f_n = triplet_to_sentence_w_triplets_one_hop_reasoning(negative_query)

    sentences_one_shot = triplet_to_sentence_one_hop_reasoning_one_shot(query, gt_series)
    sentences_f_one_shot = triplet_to_sentence_w_triplets_one_hop_reasoning_one_shot(query, gt_series)

    sentences_n_one_shot = triplet_to_sentence_one_hop_reasoning_one_shot(negative_query, gt_series)
    sentences_f_n_one_shot = triplet_to_sentence_w_triplets_one_hop_reasoning_one_shot(negative_query, gt_series)

    # save the questions
    questions_path = os.path.join(questions_directory, 'one-hop-questions.json')
    questions_f_path = os.path.join(questions_directory, 'one-hop-questions_w_triplets.json')

    questions_n_path = os.path.join(questions_directory, 'one-hop-negative-questions.json')
    questions_f_n_path = os.path.join(questions_directory, 'one-hop-negative-questions_w_triplets.json')

    questions_one_shot_path = os.path.join(questions_directory, 'one-hop-one-shot-questions.json')
    questions_f_one_shot_path = os.path.join(questions_directory, 'one-hop-one-shot-questions_w_triplets.json')

    questions_n_one_shot_path = os.path.join(questions_directory, 'one-hop-negative-one-shot-questions.json')
    questions_f_n_one_shot_path = os.path.join(questions_directory, 'one-hop-negative-one-shot-questions_w_triplets.json')

    write_to_json(sentences, questions_path, zh_flag)
    write_to_json(sentences_f, questions_f_path, zh_flag)

    write_to_json(sentences_n, questions_n_path, zh_flag)
    write_to_json(sentences_f_n, questions_f_n_path, zh_flag)

    write_to_json(sentences_one_shot, questions_one_shot_path, zh_flag)
    write_to_json(sentences_f_one_shot, questions_f_one_shot_path, zh_flag)

    write_to_json(sentences_n_one_shot, questions_n_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_one_shot, questions_f_n_one_shot_path, zh_flag)

    print(f"Done processing {path}!")


def generate_two_hop_data(args, path):
    print(f"Processing {path} for two-hop data...")
    dataset_default = path.split('/')[-1].split('.')[0]
    zh_flag = False
    if "WDKG" in dataset_default:
        zh_flag = True
    processed_data_directory = 'logs/processed_data/' + dataset_default
    questions_directory = 'logs/questions/' + dataset_default
    data_processor = DataPreprocessor(path)

    # Build the queries both positive and negative
    query = data_processor.construct_two_hop_paths()
    negative_query_replace_terminal = data_processor.construct_two_hop_paths_negative_replace_terminal()
    negative_query_replace_intermediate = data_processor.construct_two_hop_paths_negative_replace_intermediate()
    negative_query_invert_relations = data_processor.construct_two_hop_paths_negative_invert_relations()
    negative_query_path_disruption = data_processor.construct_two_hop_paths_negative_path_disruption()

    # get the ones for two-shot reasoning
    selected_edges = data_processor.top_k_betweenness_centrality(k=10)

    # break if no two-hops:
    if len(query) == 0:
        print("CURRENT DATASET HAS NO TWO-HOPS")
        return

    x = [d['two_hops'] for d in selected_edges if 'two_hops' in d]
    gt_series = matching_betweeness_edges_as_gt(query, x)

    # save the queries
    query_path = os.path.join(processed_data_directory, 'two-hop-query.csv')
    negative_query_replace_terminal_path = os.path.join(processed_data_directory,
                                                        'two-hop-negative-query-replace-terminal.csv')
    negative_query_replace_intermediate_path = os.path.join(processed_data_directory,
                                                            'two-hop-negative-query-replace-intermediate.csv')
    negative_query_invert_relations_path = os.path.join(processed_data_directory,
                                                        'two-hop-negative-query-invert-relations.csv')
    negative_query_path_disruption_path = os.path.join(processed_data_directory,
                                                       'two-hop-negative-query-path-disruption.csv')
    gt_series_path = os.path.join(processed_data_directory, 'two-hop-one-shot-series.csv')

    write_to_csv(query, query_path)
    write_to_csv(negative_query_replace_terminal, negative_query_replace_terminal_path)
    write_to_csv(negative_query_replace_intermediate, negative_query_replace_intermediate_path)
    write_to_csv(negative_query_invert_relations, negative_query_invert_relations_path)
    write_to_csv(negative_query_path_disruption, negative_query_path_disruption_path)
    write_to_csv(gt_series, gt_series_path)

    # generate the questions
    sentences = paths_to_sentence_two_hop_reasoning(query)
    sentences_f = paths_to_sentence_w_paths_two_hop_reasoning(query)

    sentences_n_rt = paths_to_sentence_two_hop_reasoning(negative_query_replace_terminal)
    sentences_f_n_rt = paths_to_sentence_w_paths_two_hop_reasoning(negative_query_replace_terminal)

    sentences_n_ri = paths_to_sentence_two_hop_reasoning(negative_query_replace_intermediate)
    sentences_f_n_ri = paths_to_sentence_w_paths_two_hop_reasoning(negative_query_replace_intermediate)

    sentences_n_ir = paths_to_sentence_two_hop_reasoning(negative_query_invert_relations)
    sentences_f_n_ir = paths_to_sentence_w_paths_two_hop_reasoning(negative_query_invert_relations)

    sentences_n_pd = paths_to_sentence_two_hop_reasoning(negative_query_path_disruption)
    sentences_f_n_pd = paths_to_sentence_w_paths_two_hop_reasoning(negative_query_path_disruption)

    sentences_one_shot = paths_to_sentence_two_hop_reasoning_one_shot(query, gt_series)
    sentences_f_one_shot = paths_to_sentence_w_paths_two_hop_reasoning_one_shot(query, gt_series)

    sentences_n_rt_one_shot = paths_to_sentence_two_hop_reasoning_one_shot(negative_query_replace_terminal, gt_series)
    sentences_f_n_rt_one_shot = paths_to_sentence_w_paths_two_hop_reasoning_one_shot(negative_query_replace_terminal, gt_series)

    sentences_n_ri_one_shot = paths_to_sentence_two_hop_reasoning_one_shot(negative_query_replace_intermediate, gt_series)
    sentences_f_n_ri_one_shot = paths_to_sentence_w_paths_two_hop_reasoning_one_shot(negative_query_replace_intermediate, gt_series)

    sentences_n_ir_one_shot = paths_to_sentence_two_hop_reasoning_one_shot(negative_query_invert_relations, gt_series)
    sentences_f_n_ir_one_shot = paths_to_sentence_w_paths_two_hop_reasoning_one_shot(negative_query_invert_relations, gt_series)

    sentences_n_pd_one_shot = paths_to_sentence_two_hop_reasoning_one_shot(negative_query_path_disruption, gt_series)
    sentences_f_n_pd_one_shot = paths_to_sentence_w_paths_two_hop_reasoning_one_shot(negative_query_path_disruption, gt_series)

    # save the questions
    questions_path = os.path.join(questions_directory, 'two-hop-questions.json')
    questions_f_path = os.path.join(questions_directory, 'two-hop-questions_w_triplets.json')

    questions_n_rt_path = os.path.join(questions_directory, 'two-hop-negative-questions-replace-terminal.json')
    questions_f_n_rt_path = os.path.join(questions_directory, 'two-hop-negative-questions-replace-terminal_w_triplets.json')

    questions_n_ri_path = os.path.join(questions_directory, 'two-hop-negative-questions-replace-intermediate.json')
    questions_f_n_ri_path = os.path.join(questions_directory, 'two-hop-negative-questions-replace-intermediate_w_triplets.json')

    questions_n_ir_path = os.path.join(questions_directory, 'two-hop-negative-questions-invert-relations.json')
    questions_f_n_ir_path = os.path.join(questions_directory, 'two-hop-negative-questions-invert-relations_w_triplets.json')

    questions_n_pd_path = os.path.join(questions_directory, 'two-hop-negative-questions-path-disruption.json')
    questions_f_n_pd_path = os.path.join(questions_directory, 'two-hop-negative-questions-path-disruption_w_triplets.json')

    questions_one_shot_path = os.path.join(questions_directory, 'two-hop-one-shot-questions.json')
    questions_f_one_shot_path = os.path.join(questions_directory, 'two-hop-one-shot-questions_w_triplets.json')

    questions_n_rt_one_shot_path = os.path.join(questions_directory, 'two-hop-negative-one-shot-questions-replace-terminal.json')
    questions_f_n_rt_one_shot_path = os.path.join(questions_directory,
                                                  'two-hop-negative-one-shot-questions-replace-terminal_w_triplets.json')

    questions_n_ri_one_shot_path = os.path.join(questions_directory, 'two-hop-negative-one-shot-questions-replace-intermediate.json')
    questions_f_n_ri_one_shot_path = os.path.join(questions_directory,
                                                  'two-hop-negative-one-shot-questions-replace-intermediate_w_triplets.json')

    questions_n_ir_one_shot_path = os.path.join(questions_directory, 'two-hop-negative-one-shot-questions-invert-relations.json')
    questions_f_n_ir_one_shot_path = os.path.join(questions_directory,
                                                  'two-hop-negative-one-shot-questions-invert-relations_w_triplets.json')

    questions_n_pd_one_shot_path = os.path.join(questions_directory, 'two-hop-negative-one-shot-questions-path-disruption.json')
    questions_f_n_pd_one_shot_path = os.path.join(questions_directory,
                                                  'two-hop-negative-one-shot-questions-path-disruption_w_triplets.json')

    write_to_json(sentences, questions_path, zh_flag)
    write_to_json(sentences_f, questions_f_path, zh_flag)

    write_to_json(sentences_n_rt, questions_n_rt_path, zh_flag)
    write_to_json(sentences_f_n_rt, questions_f_n_rt_path, zh_flag)

    write_to_json(sentences_n_ri, questions_n_ri_path, zh_flag)
    write_to_json(sentences_f_n_ri, questions_f_n_ri_path, zh_flag)

    write_to_json(sentences_n_ir, questions_n_ir_path, zh_flag)
    write_to_json(sentences_f_n_ir, questions_f_n_ir_path, zh_flag)

    write_to_json(sentences_n_pd, questions_n_pd_path, zh_flag)
    write_to_json(sentences_f_n_pd, questions_f_n_pd_path, zh_flag)

    write_to_json(sentences_one_shot, questions_one_shot_path, zh_flag)
    write_to_json(sentences_f_one_shot, questions_f_one_shot_path, zh_flag)

    write_to_json(sentences_n_rt_one_shot, questions_n_rt_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_rt_one_shot, questions_f_n_rt_one_shot_path, zh_flag)

    write_to_json(sentences_n_ri_one_shot, questions_n_ri_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_ri_one_shot, questions_f_n_ri_one_shot_path, zh_flag)

    write_to_json(sentences_n_ir_one_shot, questions_n_ir_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_ir_one_shot, questions_f_n_ir_one_shot_path, zh_flag)

    write_to_json(sentences_n_pd_one_shot, questions_n_pd_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_pd_one_shot, questions_f_n_pd_one_shot_path, zh_flag)

    print(f"Done processing {path}!")


def generate_three_hop_data(args, path):
    print(f"Processing {path} for three-hop data...")
    dataset_default = path.split('/')[-1].split('.')[0]
    zh_flag = False
    if "WDKG" in dataset_default:
        zh_flag = True
    processed_data_directory = 'logs/processed_data/' + dataset_default
    questions_directory = 'logs/questions/' + dataset_default
    data_processor = DataPreprocessor(path)

    # Build the queries both positive and negative
    query = data_processor.construct_three_hop_paths()
    negative_query = data_processor.construct_three_hop_paths_negative()

    # get the ones for two-shot reasoning
    selected_edges = data_processor.top_k_betweenness_centrality(k=10)

    # break if no two-hops:
    if len(query) == 0:
        print("CURRENT DATASET HAS NO THREE-HOPS")
        return

    x = [d['three_hops'] for d in selected_edges if 'three_hops' in d]
    gt_series = matching_betweeness_edges_as_gt(query, x)

    # save the queries
    query_path = os.path.join(processed_data_directory, 'three-hop-query.csv')
    negative_query_path = os.path.join(processed_data_directory, 'three-hop-negative-query.csv')
    gt_series_path = os.path.join(processed_data_directory, 'three-hop-one-shot-series.csv')

    write_to_csv(query, query_path)
    write_to_csv(negative_query, negative_query_path)
    write_to_csv(gt_series, gt_series_path)

    # generate the questions
    sentences = paths_to_sentence_three_hop_reasoning(query)
    sentences_f = paths_to_sentence_w_paths_three_hop_reasoning(query)

    sentences_n = paths_to_sentence_three_hop_reasoning(negative_query)
    sentences_f_n = paths_to_sentence_w_paths_three_hop_reasoning(negative_query)

    sentences_one_shot = paths_to_sentence_three_hop_reasoning_one_shot(query, gt_series)
    sentences_f_one_shot = paths_to_sentence_w_paths_three_hop_reasoning_one_shot(query, gt_series)

    sentences_n_one_shot = paths_to_sentence_three_hop_reasoning_one_shot(negative_query, gt_series)
    sentences_f_n_one_shot = paths_to_sentence_w_paths_three_hop_reasoning_one_shot(negative_query, gt_series)

    # save the questions
    questions_path = os.path.join(questions_directory, 'three-hop-questions.json')
    questions_f_path = os.path.join(questions_directory, 'three-hop-questions_w_triplets.json')

    questions_n_path = os.path.join(questions_directory, 'three-hop-negative-questions.json')
    questions_f_n_path = os.path.join(questions_directory, 'three-hop-negative-questions_w_triplets.json')

    questions_one_shot_path = os.path.join(questions_directory, 'three-hop-one-shot-questions.json')
    questions_f_one_shot_path = os.path.join(questions_directory, 'three-hop-one-shot-questions_w_triplets.json')

    questions_n_one_shot_path = os.path.join(questions_directory, 'three-hop-negative-one-shot-questions.json')
    questions_f_n_one_shot_path = os.path.join(questions_directory,
                                               'three-hop-negative-one-shot-questions_w_triplets.json')

    write_to_json(sentences, questions_path, zh_flag)
    write_to_json(sentences_f, questions_f_path, zh_flag)

    write_to_json(sentences_n, questions_n_path, zh_flag)
    write_to_json(sentences_f_n, questions_f_n_path, zh_flag)

    write_to_json(sentences_one_shot, questions_one_shot_path, zh_flag)
    write_to_json(sentences_f_one_shot, questions_f_one_shot_path, zh_flag)

    write_to_json(sentences_n_one_shot, questions_n_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_one_shot, questions_f_n_one_shot_path, zh_flag)

    print(f"Done processing {path}!")


def generate_two_predecessors_data(args, path):
    print(f"Processing {path} for two predecessors data...")
    dataset_default = path.split('/')[-1].split('.')[0]
    zh_flag = False
    if "WDKG" in dataset_default:
        zh_flag = True
    processed_data_directory = 'logs/processed_data/' + dataset_default
    questions_directory = 'logs/questions/' + dataset_default
    data_processor = DataPreprocessor(path)

    # Build the queries both positive and negative
    query = data_processor.construct_paths_nodes_with_two_predecessors()
    negative_query_negative_one_p0 = data_processor.construct_paths_nodes_with_two_predecessors_negative_one(choice=0)
    negative_query_negative_one_p1 = data_processor.construct_paths_nodes_with_two_predecessors_negative_one(choice=1)
    negative_query_negative_two = data_processor.construct_paths_nodes_with_two_predecessors_negative_two()

    # break if no two-hops:
    if len(query) == 0:
        print("CURRENT DATASET HAS NO TWO-PREDECESSORS")
        return

    # get the ones for two-shot reasoning
    gt_series = unmatching_query_w_gt(query)

    # save the queries
    query_path = os.path.join(processed_data_directory, 'two-predecessors-query.csv')
    negative_query_negative_one_p0_path = os.path.join(processed_data_directory,
                                                       'two-predecessors-query-negative-one-p0.csv')
    negative_query_negative_one_p1_path = os.path.join(processed_data_directory,
                                                       'two-predecessors-query-negative-one-p1.csv')
    negative_query_negative_two_path = os.path.join(processed_data_directory,
                                                    'two-predecessors-query-negative-two.csv')
    gt_series_path = os.path.join(processed_data_directory, 'two-predecessors-one-shot-series.csv')

    write_to_csv(query, query_path)
    write_to_csv(negative_query_negative_one_p0, negative_query_negative_one_p0_path)
    write_to_csv(negative_query_negative_one_p1, negative_query_negative_one_p1_path)
    write_to_csv(negative_query_negative_two, negative_query_negative_two_path)
    write_to_csv(gt_series, gt_series_path)

    # generate the questions
    sentences = query_2p_to_sentence_one_hop_reasoning(query)
    sentences_f = query_2p_to_sentence_w_query_one_hop_reasoning(query)

    sentences_n_one_p0 = query_2p_to_sentence_one_hop_reasoning(negative_query_negative_one_p0)
    sentences_f_n_one_p0 = query_2p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_one_p0)

    sentences_n_one_p1 = query_2p_to_sentence_one_hop_reasoning(negative_query_negative_one_p1)
    sentences_f_n_one_p1 = query_2p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_one_p1)

    sentences_n_two = query_2p_to_sentence_one_hop_reasoning(negative_query_negative_two)
    sentences_f_n_two = query_2p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_two)

    sentences_one_shot = query_2p_to_sentence_one_hop_reasoning_one_shot(query, gt_series)
    sentences_f_one_shot = query_2p_to_sentence_w_query_one_hop_reasoning_one_shot(query, gt_series)

    sentences_n_one_p0_one_shot = query_2p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_one_p0, gt_series)
    sentences_f_n_one_p0_one_shot = query_2p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_one_p0, gt_series)

    sentences_n_one_p1_one_shot = query_2p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_one_p1, gt_series)
    sentences_f_n_one_p1_one_shot = query_2p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_one_p1, gt_series)

    sentences_n_two_one_shot = query_2p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_two, gt_series)
    sentences_f_n_two_one_shot = query_2p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_two, gt_series)

    # save the questions
    questions_path = os.path.join(questions_directory, 'two-predecessors-questions.json')
    questions_f_path = os.path.join(questions_directory, 'two-predecessors-questions_w_triplets.json')

    questions_n_one_p0_path = os.path.join(questions_directory, 'two-predecessors-negative-questions-negative-one-p0.json')
    questions_f_n_one_p0_path = os.path.join(questions_directory, 'two-predecessors-negative-questions-negative-one-p0_w_triplets.json')

    questions_n_one_p1_path = os.path.join(questions_directory, 'two-predecessors-negative-questions-negative-one-p1.json')
    questions_f_n_one_p1_path = os.path.join(questions_directory, 'two-predecessors-negative-questions-negative-one-p1_w_triplets.json')

    questions_n_two_path = os.path.join(questions_directory, 'two-predecessors-negative-questions-negative-two.json')
    questions_f_n_two_path = os.path.join(questions_directory, 'two-predecessors-negative-questions-negative-two_w_triplets.json')

    questions_one_shot_path = os.path.join(questions_directory, 'two-predecessors-one-shot-questions.json')
    questions_f_one_shot_path = os.path.join(questions_directory, 'two-predecessors-one-shot-questions_w_triplets.json')

    questions_n_one_p0_one_shot_path = os.path.join(questions_directory,
                                           'two-predecessors-negative-one-shot-questions-negative-one-p0.json')
    questions_f_n_one_p0_one_shot_path = os.path.join(questions_directory,
                                             'two-predecessors-negative-one-shot-questions-negative-one-p0_w_triplets.json')

    questions_n_one_p1_one_shot_path = os.path.join(questions_directory,
                                           'two-predecessors-negative-one-shot-questions-negative-one-p1.json')
    questions_f_n_one_p1_one_shot_path = os.path.join(questions_directory,
                                             'two-predecessors-negative-one-shot-questions-negative-one-p1_w_triplets.json')

    questions_n_two_one_shot_path = os.path.join(questions_directory, 'two-predecessors-negative-one-shot-questions-negative-two.json')
    questions_f_n_two_one_shot_path = os.path.join(questions_directory,
                                          'two-predecessors-negative-one-shot-questions-negative-two_w_triplets.json')

    write_to_json(sentences, questions_path, zh_flag)
    write_to_json(sentences_f, questions_f_path, zh_flag)

    write_to_json(sentences_n_one_p0, questions_n_one_p0_path, zh_flag)
    write_to_json(sentences_f_n_one_p0, questions_f_n_one_p0_path, zh_flag)

    write_to_json(sentences_n_one_p1, questions_n_one_p1_path, zh_flag)
    write_to_json(sentences_f_n_one_p1, questions_f_n_one_p1_path, zh_flag)

    write_to_json(sentences_n_two, questions_n_two_path, zh_flag)
    write_to_json(sentences_f_n_two, questions_f_n_two_path, zh_flag)

    write_to_json(sentences_one_shot, questions_one_shot_path, zh_flag)
    write_to_json(sentences_f_one_shot, questions_f_one_shot_path, zh_flag)

    write_to_json(sentences_n_one_p0_one_shot, questions_n_one_p0_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_one_p0_one_shot, questions_f_n_one_p0_one_shot_path, zh_flag)

    write_to_json(sentences_n_one_p1_one_shot, questions_n_one_p1_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_one_p1_one_shot, questions_f_n_one_p1_one_shot_path, zh_flag)

    write_to_json(sentences_n_two_one_shot, questions_n_two_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_two_one_shot, questions_f_n_two_one_shot_path, zh_flag)

    print(f"Done processing {path}!")


def generate_three_predecessors_data(args, path):
    print(f"Processing {path} for three predecessors data...")
    dataset_default = path.split('/')[-1].split('.')[0]
    zh_flag = False
    if "WDKG" in dataset_default:
        zh_flag = True
    processed_data_directory = 'logs/processed_data/' + dataset_default
    questions_directory = 'logs/questions/' + dataset_default
    data_processor = DataPreprocessor(path)

    # Build the queries both positive and negative
    query = data_processor.construct_paths_nodes_with_three_predecessors()
    negative_query_negative_one_p0 = data_processor.construct_paths_nodes_with_three_predecessors_negative_one(choice=0)
    negative_query_negative_one_p1 = data_processor.construct_paths_nodes_with_three_predecessors_negative_one(choice=1)
    negative_query_negative_one_p2 = data_processor.construct_paths_nodes_with_three_predecessors_negative_one(choice=2)
    negative_query_negative_two_p01 = data_processor.construct_paths_nodes_with_three_predecessors_negative_two(
        replace_indices=(0, 1)
    )
    negative_query_negative_two_p02 = data_processor.construct_paths_nodes_with_three_predecessors_negative_two(
        replace_indices=(0, 2)
    )
    negative_query_negative_two_p12 = data_processor.construct_paths_nodes_with_three_predecessors_negative_two(
        replace_indices=(1, 2)
    )
    negative_query_negative_three = data_processor.construct_paths_nodes_with_three_predecessors_negative_three()

    # break if no two-hops:
    if len(query) == 0:
        print("CURRENT DATASET HAS NO THREE-PREDECESSORS")
        return

    # get the ones for two-shot reasoning
    gt_series = unmatching_query_w_gt(query)

    # save the queries
    query_path = os.path.join(processed_data_directory, 'three-predecessors-query.csv')
    negative_query_negative_one_p0_path = os.path.join(processed_data_directory,
                                                       'three-predecessors-query-negative-one-p0.csv')
    negative_query_negative_one_p1_path = os.path.join(processed_data_directory,
                                                       'three-predecessors-query-negative-one-p1.csv')
    negative_query_negative_one_p2_path = os.path.join(processed_data_directory,
                                                       'three-predecessors-query-negative-one-p2.csv')
    negative_query_negative_two_p01_path = os.path.join(processed_data_directory,
                                                        'three-predecessors-query-negative-two-p01.csv')
    negative_query_negative_two_p02_path = os.path.join(processed_data_directory,
                                                        'three-predecessors-query-negative-two-p02.csv')
    negative_query_negative_two_p12_path = os.path.join(processed_data_directory,
                                                        'three-predecessors-query-negative-two-p12.csv')
    negative_query_negative_three_path = os.path.join(processed_data_directory,
                                                        'three-predecessors-query-negative-three.csv')
    gt_series_path = os.path.join(processed_data_directory, 'three-predecessors-one-shot-series.csv')

    write_to_csv(query, query_path)
    write_to_csv(negative_query_negative_one_p0, negative_query_negative_one_p0_path)
    write_to_csv(negative_query_negative_one_p1, negative_query_negative_one_p1_path)
    write_to_csv(negative_query_negative_one_p2, negative_query_negative_one_p2_path)
    write_to_csv(negative_query_negative_two_p01, negative_query_negative_two_p01_path)
    write_to_csv(negative_query_negative_two_p02, negative_query_negative_two_p02_path)
    write_to_csv(negative_query_negative_two_p12, negative_query_negative_two_p12_path)
    write_to_csv(negative_query_negative_three, negative_query_negative_three_path)
    write_to_csv(gt_series, gt_series_path)

    # generate the questions
    sentences = query_3p_to_sentence_one_hop_reasoning(query)
    sentences_f = query_3p_to_sentence_w_query_one_hop_reasoning(query)

    sentences_n_one_p0 = query_3p_to_sentence_one_hop_reasoning(negative_query_negative_one_p0)
    sentences_f_n_one_p0 = query_3p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_one_p0)

    sentences_n_one_p1 = query_3p_to_sentence_one_hop_reasoning(negative_query_negative_one_p1)
    sentences_f_n_one_p1 = query_3p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_one_p1)

    sentences_n_one_p2 = query_3p_to_sentence_one_hop_reasoning(negative_query_negative_one_p2)
    sentences_f_n_one_p2 = query_3p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_one_p2)

    sentences_n_two_p01 = query_3p_to_sentence_one_hop_reasoning(negative_query_negative_two_p01)
    sentences_f_n_two_p01 = query_3p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_two_p01)

    sentences_n_two_p02 = query_3p_to_sentence_one_hop_reasoning(negative_query_negative_two_p02)
    sentences_f_n_two_p02 = query_3p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_two_p02)

    sentences_n_two_p12 = query_3p_to_sentence_one_hop_reasoning(negative_query_negative_two_p12)
    sentences_f_n_two_p12 = query_3p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_two_p12)

    sentences_n_three = query_3p_to_sentence_one_hop_reasoning(negative_query_negative_three)
    sentences_f_n_three = query_3p_to_sentence_w_query_one_hop_reasoning(negative_query_negative_three)

    sentences_one_shot = query_3p_to_sentence_one_hop_reasoning_one_shot(query, gt_series)
    sentences_f_one_shot = query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(query, gt_series)

    sentences_n_one_p0_one_shot = query_3p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_one_p0, gt_series)
    sentences_f_n_one_p0_one_shot = query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_one_p0, gt_series)

    sentences_n_one_p1_one_shot = query_3p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_one_p1, gt_series)
    sentences_f_n_one_p1_one_shot = query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_one_p1, gt_series)

    sentences_n_one_p2_one_shot = query_3p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_one_p2, gt_series)
    sentences_f_n_one_p2_one_shot = query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_one_p2, gt_series)

    sentences_n_two_p01_one_shot = query_3p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_two_p01, gt_series)
    sentences_f_n_two_p01_one_shot = query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_two_p01, gt_series)

    sentences_n_two_p02_one_shot = query_3p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_two_p02, gt_series)
    sentences_f_n_two_p02_one_shot = query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_two_p02, gt_series)

    sentences_n_two_p12_one_shot = query_3p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_two_p12, gt_series)
    sentences_f_n_two_p12_one_shot = query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_two_p12, gt_series)

    sentences_n_three_one_shot = query_3p_to_sentence_one_hop_reasoning_one_shot(negative_query_negative_three, gt_series)
    sentences_f_n_three_one_shot = query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(negative_query_negative_three, gt_series)

    # save the questions
    questions_path = os.path.join(questions_directory, 'three-predecessors-questions.json')
    questions_f_path = os.path.join(questions_directory, 'three-predecessors-questions_w_triplets.json')

    questions_n_one_p0_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-one-p0.json')
    questions_f_n_one_p0_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-one-p0_w_triplets.json')

    questions_n_one_p1_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-one-p1.json')
    questions_f_n_one_p1_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-one-p1_w_triplets.json')

    questions_n_one_p2_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-one-p2.json')
    questions_f_n_one_p2_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-one-p2_w_triplets.json')

    questions_n_two_p01_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-two-p01.json')
    questions_f_n_two_p01_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-two-p01_w_triplets.json')

    questions_n_two_p02_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-two-p02.json')
    questions_f_n_two_p02_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-two-p02_w_triplets.json')

    questions_n_two_p12_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-two-p12.json')
    questions_f_n_two_p12_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-two-p12_w_triplets.json')

    questions_n_three_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-three.json')
    questions_f_n_three_path = os.path.join(questions_directory, 'three-predecessors-negative-questions-negative-three_w_triplets.json')

    questions_one_shot_path = os.path.join(questions_directory, 'three-predecessors-one-shot-questions.json')
    questions_f_one_shot_path = os.path.join(questions_directory, 'three-predecessors-one-shot-questions_w_triplets.json')

    questions_n_one_p0_one_shot_path = os.path.join(questions_directory,
                                           'three-predecessors-negative-one-shot-questions-negative-one-p0.json')
    questions_f_n_one_p0_one_shot_path = os.path.join(questions_directory,
                                             'three-predecessors-negative-one-shot-questions-negative-one-p0_w_triplets.json')

    questions_n_one_p1_one_shot_path = os.path.join(questions_directory,
                                           'three-predecessors-negative-one-shot-questions-negative-one-p1.json')
    questions_f_n_one_p1_one_shot_path = os.path.join(questions_directory,
                                             'three-predecessors-negative-one-shot-questions-negative-one-p1_w_triplets.json')

    questions_n_one_p2_one_shot_path = os.path.join(questions_directory,
                                           'three-predecessors-negative-one-shot-questions-negative-one-p2.json')
    questions_f_n_one_p2_one_shot_path = os.path.join(questions_directory,
                                             'three-predecessors-negative-one-shot-questions-negative-one-p2_w_triplets.json')

    questions_n_two_p01_one_shot_path = os.path.join(questions_directory,
                                            'three-predecessors-negative-one-shot-questions-negative-two-p01.json')
    questions_f_n_two_p01_one_shot_path = os.path.join(questions_directory,
                                              'three-predecessors-negative-one-shot-questions-negative-two-p01_w_triplets.json')

    questions_n_two_p02_one_shot_path = os.path.join(questions_directory,
                                            'three-predecessors-negative-one-shot-questions-negative-two-p02.json')
    questions_f_n_two_p02_one_shot_path = os.path.join(questions_directory,
                                              'three-predecessors-negative-one-shot-questions-negative-two-p02_w_triplets.json')

    questions_n_two_p12_one_shot_path = os.path.join(questions_directory,
                                            'three-predecessors-negative-one-shot-questions-negative-two-p12.json')
    questions_f_n_two_p12_one_shot_path = os.path.join(questions_directory,
                                              'three-predecessors-negative-one-shot-questions-negative-two-p12_w_triplets.json')

    questions_n_three_one_shot_path = os.path.join(questions_directory,
                                          'three-predecessors-negative-one-shot-questions-negative-three.json')
    questions_f_n_three_one_shot_path = os.path.join(questions_directory,
                                            'three-predecessors-negative-one-shot-questions-negative-three_w_triplets.json')

    write_to_json(sentences, questions_path, zh_flag)
    write_to_json(sentences_f, questions_f_path, zh_flag)

    write_to_json(sentences_n_one_p0, questions_n_one_p0_path, zh_flag)
    write_to_json(sentences_f_n_one_p0, questions_f_n_one_p0_path, zh_flag)

    write_to_json(sentences_n_one_p1, questions_n_one_p1_path, zh_flag)
    write_to_json(sentences_f_n_one_p1, questions_f_n_one_p1_path, zh_flag)

    write_to_json(sentences_n_one_p2, questions_n_one_p2_path, zh_flag)
    write_to_json(sentences_f_n_one_p2, questions_f_n_one_p2_path, zh_flag)

    write_to_json(sentences_n_two_p01, questions_n_two_p01_path, zh_flag)
    write_to_json(sentences_f_n_two_p01, questions_f_n_two_p01_path, zh_flag)

    write_to_json(sentences_n_two_p02, questions_n_two_p02_path, zh_flag)
    write_to_json(sentences_f_n_two_p02, questions_f_n_two_p02_path, zh_flag)

    write_to_json(sentences_n_two_p12, questions_n_two_p12_path, zh_flag)
    write_to_json(sentences_f_n_two_p12, questions_f_n_two_p12_path, zh_flag)

    write_to_json(sentences_n_three, questions_n_three_path, zh_flag)
    write_to_json(sentences_f_n_three, questions_f_n_three_path, zh_flag)

    write_to_json(sentences_one_shot, questions_one_shot_path, zh_flag)
    write_to_json(sentences_f_one_shot, questions_f_one_shot_path, zh_flag)

    write_to_json(sentences_n_one_p0_one_shot, questions_n_one_p0_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_one_p0_one_shot, questions_f_n_one_p0_one_shot_path, zh_flag)

    write_to_json(sentences_n_one_p1_one_shot, questions_n_one_p1_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_one_p1_one_shot, questions_f_n_one_p1_one_shot_path, zh_flag)

    write_to_json(sentences_n_one_p2_one_shot, questions_n_one_p2_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_one_p2_one_shot, questions_f_n_one_p2_one_shot_path, zh_flag)

    write_to_json(sentences_n_two_p01_one_shot, questions_n_two_p01_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_two_p01_one_shot, questions_f_n_two_p01_one_shot_path, zh_flag)

    write_to_json(sentences_n_two_p02_one_shot, questions_n_two_p02_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_two_p02_one_shot, questions_f_n_two_p02_one_shot_path, zh_flag)

    write_to_json(sentences_n_two_p12_one_shot, questions_n_two_p12_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_two_p12_one_shot, questions_f_n_two_p12_one_shot_path, zh_flag)

    write_to_json(sentences_n_three_one_shot, questions_n_three_one_shot_path, zh_flag)
    write_to_json(sentences_f_n_three_one_shot, questions_f_n_three_one_shot_path, zh_flag)

    print(f"Done processing {path}!")


def generate_node_pairs_data(args, path):
    print(f"Processing {path} for node-pairs data for feature extraction...")
    dataset_default = path.split('/')[-1].split('.')[0]
    zh_flag = False
    if "WDKG" in dataset_default:
        zh_flag = True
    processed_data_directory = 'logs/processed_data/' + dataset_default
    questions_directory = 'logs/questions/' + dataset_default
    data_processor = DataPreprocessor(path)

    # Build the queries both positive and negative
    query = data_processor.get_query_for_relation_extraction(one_one_one=True, n=0)

    if len(query) == 0:
        print("CURRENT DATASET HAS NO NODE-PAIRS")
        return

    # save the queries
    query_path = os.path.join(processed_data_directory, 'node-pairs-query.csv')

    write_to_csv(query, query_path)

    # generate the questions
    sentences = node_pairs_to_sentence_relation_extraction(query)
    sentences_f = node_pairs_to_sentence_w_float_relation_extraction(query)

    sentences_one_shot = node_pairs_to_sentence_relation_extraction_one_shot(query)
    sentences_f_one_shot = node_pairs_to_sentence_w_float_relation_extraction_one_shot(query)

    # save the questions
    questions_path = os.path.join(questions_directory, 'node-pairs-questions.json')
    questions_f_path = os.path.join(questions_directory, 'node-pairs-questions_w_floats.json')

    questions_one_shot_path = os.path.join(questions_directory, 'node-pairs-one-shot-questions.json')
    questions_f_one_shot_path = os.path.join(questions_directory, 'node-pairs-one-shot-questions_w_floats.json')

    write_to_json(sentences, questions_path, zh_flag)
    write_to_json(sentences_f, questions_f_path, zh_flag)

    write_to_json(sentences_one_shot, questions_one_shot_path, zh_flag)
    write_to_json(sentences_f_one_shot, questions_f_one_shot_path, zh_flag)

    print(f"Done processing {path}!")


def generate_sub_graph_data(args, path):
    print(f"Processing {path} for sub_graph data for feature extraction...")
    dataset_default = path.split('/')[-1].split('.')[0]
    zh_flag = False
    if "WDKG" in dataset_default:
        zh_flag = True
    processed_data_directory = 'logs/processed_data/' + dataset_default
    questions_directory = 'logs/questions/' + dataset_default
    data_processor = DataPreprocessor(path)

    sizes = [5, 10, 15]

    for size in sizes:
        # Build the queries both positive and negative
        query = data_processor.get_query_for_relation_extraction(one_one_one=False, k=size, n=10)

        if len(query) == 0:
            print(f"CURRENT DATASET HAS NO SUB-GRAPH OF CURRENT SIZE {size}")
            continue

        # save the queries
        query_path = os.path.join(processed_data_directory, f"sub-graph-query-size-{size}.csv")

        write_to_csv(query, query_path)

        # generate the questions
        sentences = subgraph_node_pairs_to_sentence_relation_extraction(query)
        sentences_f = subgraph_node_pairs_to_sentence_w_float_relation_extraction(query)

        sentences_one_shot = subgraph_node_pairs_to_sentence_relation_extraction_one_shot(query)
        sentences_f_one_shot = subgraph_node_pairs_to_sentence_w_float_relation_extraction_one_shot(query)

        # save the questions
        questions_path = os.path.join(questions_directory, f'sub-graph-questions-size-{size}.json')
        questions_f_path = os.path.join(questions_directory, f'sub-graph-questions_w_floats-size-{size}.json')

        questions_one_shot_path = os.path.join(questions_directory, f'sub-graph-one-shot-questions-size-{size}.json')
        questions_f_one_shot_path = os.path.join(questions_directory, f'sub-graph-one-shot-questions_w_floats-size-{size}.json')

        write_to_json(sentences, questions_path, zh_flag)
        write_to_json(sentences_f, questions_f_path, zh_flag)

        write_to_json(sentences_one_shot, questions_one_shot_path, zh_flag)
        write_to_json(sentences_f_one_shot, questions_f_one_shot_path, zh_flag)

        print(f"Done processing {path} with the size {size} subgraphs!")

    print(f"Done processing {path}!")