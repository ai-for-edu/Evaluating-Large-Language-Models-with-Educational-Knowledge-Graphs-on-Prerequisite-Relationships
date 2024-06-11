import sys
import os
import csv
from tqdm import tqdm
import logging
import pickle as pkl
import argparse
import multiprocessing as mp
from .data_preprocessing import is_chinese
import random


logging.basicConfig(level=logging.INFO)


def triplet_to_sentence_one_hop_reasoning(triplets):
    zh_flag = 0
    for triplet in triplets:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(triplet[0])
        zh_flag += is_chinese(triplet[-1])

    sentences = []
    if zh_flag > 0:
        for subj, pred, obj in triplets:
            sentence = f"给定教育学前置知识点的场景，请问{subj.replace('_', ' ')}是{obj.replace('_', ' ')}的{pred}吗？"
            sentences.append(sentence)
    else:
        for subj, pred, obj in triplets:
            sentence = f"Given the concept of prerequisite relationships in education, is {subj.replace('_', ' ')} {pred} {obj.replace('_', ' ')}?"
            sentences.append(sentence)
    return sentences


def triplet_to_sentence_w_triplets_one_hop_reasoning(triplets):
    zh_flag = 0
    for triplet in triplets:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(triplet[0])
        zh_flag += is_chinese(triplet[-1])

    sentences = []
    if zh_flag > 0:
        for subj, pred, obj in triplets:
            sentence = f"给定Resource Description Framework用于描述教育学前置知识点：<知识点1> <关联> <知识点2>代表知识点1是知识点2的关联，以下关于知识的描述是否正确？<{obj}> <{pred}> <{subj}>"
            # the order is changed to match the Chinese common language
            sentences.append(sentence)
    else:
        for subj, pred, obj in triplets:
            sentence = f"Given the Resource Description Framework to describe the concept of prerequisite relationships in education: <entity 1> <relationship> <entity 2> means entity 1 is the relationship of entity 2, iIs the following relationship about the knowledge correct? <{subj}><{pred}> <{obj}>"
            sentences.append(sentence)
    return sentences


def paths_to_sentence_two_hop_reasoning(two_hop_paths):
    """
    Direct Inference Questions of two-hops
    :param two_hop_paths: from construct_two_hop_paths
    :return:
    """
    zh_flag = 0
    for path in two_hop_paths:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(path[0])
        zh_flag += is_chinese(path[-1])

    sentences = []
    if zh_flag > 0:
        for subj, rel1, successor, rel2, second_hop in two_hop_paths:
            sentence = (f"给定教育学前置知识点的场景，请问如果{subj.replace('_', ' ')}是{successor.replace('_', ' ')}的{rel1}，"
                        f"且{successor.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}，"
                        f"那么{subj.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}吗？")
            sentences.append(sentence)
    else:
        for subj, rel1, successor, rel2, second_hop in two_hop_paths:
            sentence = (f"Given the concept of prerequisite relationships in education, if {subj.replace('_', ' ')} is {rel1} {successor.replace('_', ' ')}, "
                        f"and {successor.replace('_', ' ')} is {rel2} {second_hop.replace('_', ' ')}, "
                        f"then is {subj.replace('_', ' ')} {rel2} {second_hop.replace('_', ' ')}?")
            sentences.append(sentence)
    return sentences


def paths_to_sentence_w_paths_two_hop_reasoning(two_hop_paths):
    zh_flag = 0
    for triplet in two_hop_paths:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(triplet[0])
        zh_flag += is_chinese(triplet[-1])

    sentences = []
    if zh_flag > 0:
        for subj, rel1, successor, rel2, second_hop in two_hop_paths:
            sentence = (f"给定Resource Description Framework用于描述教育学前置知识点：<知识点1> <关联> <知识点2> <关联> <知识点3>代表知识点1是知识点2的关联，知识点2是知识点3的关联，以下关于知识的描述是否正确？如果 <{subj}> <{rel1}> <{successor}> <{rel2}> <{second_hop}>，"
                        f"以下关于知识的描述是否正确？<{subj}> <{rel2}> <{second_hop}>")
            # the order is changed to match the Chinese common language
            sentences.append(sentence)
    else:
        for subj, rel1, successor, rel2, second_hop in two_hop_paths:
            sentence = (f"Given the Resource Description Framework to describe the concept of prerequisite relationships in education: <entity 1> <relationship> <entity 2> <relationship> <entity 3> means entity 1 is the relationship of entity 2, and entity 2 is the relationship of entity 3. Given <{subj}> <{rel1}> <{successor}> <{rel2}> <{second_hop}> "
                        f"then is <{subj}> <{rel2}> <{second_hop}> correct?")
            sentences.append(sentence)
    return sentences


def paths_to_sentence_three_hop_reasoning(three_hop_paths):
    """
    Direct Inference Questions of three-hops
    :param three_hop_paths: from construct_three_hop_paths
    :return:
    """
    zh_flag = 0
    for path in three_hop_paths:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(path[0])
        zh_flag += is_chinese(path[-1])

    sentences = []
    if zh_flag > 0:
        for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
            sentence = (f"给定教育学前置知识点的场景，请问如果{subj.replace('_', ' ')}是{successor.replace('_', ' ')}的{rel1}，"
                        f"且{successor.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}，"
                        f"且{second_hop.replace('_', ' ')}是{third_hop.replace('_', ' ')}的{rel3}，"
                        f"那么{subj.replace('_', ' ')}是{third_hop.replace('_', ' ')}的{rel3}吗？")
            sentences.append(sentence)
    else:
        for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
            sentence = (f"Given the concept of prerequisite relationships in education, if {subj.replace('_', ' ')} is {rel1} {successor.replace('_', ' ')}, "
                        f"and {successor.replace('_', ' ')} is {rel2} {second_hop.replace('_', ' ')}, "
                        f"and {second_hop.replace('_', ' ')} is {rel3} {third_hop.replace('_', ' ')}, "
                        f"then is {subj.replace('_', ' ')} {rel3} {third_hop.replace('_', ' ')}?")
            sentences.append(sentence)
    return sentences


def paths_to_sentence_w_paths_three_hop_reasoning(three_hop_paths):
    zh_flag = 0
    for path in three_hop_paths:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(path[0])
        zh_flag += is_chinese(path[-1])

    sentences = []
    if zh_flag > 0:
        for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
            sentence = (f"给定Resource Description Framework用于描述教育学前置知识点：<知识点1> <关联> <知识点2> <关联> <知识点3> <关联> <知识点4>代表知识点1是知识点2的关联，知识点2是知识点3的关联，知识点3又是知识点4的关联，以下关于知识的描述是否正确？如果<{third_hop}> <{rel3}> <{second_hop}> <{rel2}> <{successor}>"
                        f" <{rel1}> <{subj}>，"
                        f"以下关于知识的描述是否正确？<{third_hop}> <{rel3}> <{subj}>")
            # the order is changed to match the Chinese common language
            sentences.append(sentence)
    else:
        for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
            sentence = (f"Given the Resource Description Framework to describe the concept of prerequisite relationships in education: <entity 1> <relationship> <entity 2> <relationship> <entity 3> <relationship> <entity 4> means entity 1 is the relationship of entity 2, entity 2 is the relationship of entity 3, and entity 3 is the relationship of entity 4. Given <{subj}> <{rel1}> <{successor}> <{rel2}> "
                        f"{second_hop}> <{rel3}> <{third_hop}>, "
                        f"then is <{third_hop}> <{rel3}> <{subj}> correct?")
            sentences.append(sentence)
    return sentences


def query_2p_to_sentence_one_hop_reasoning(query):
    zh_flag = 0
    for q in query:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[-1])

    sentences = []
    if zh_flag > 0:
        for subj1, subj2, pred, obj in query:
            sentence = f"给定教育学前置知识点的场景，请问{subj1.replace('_', ' ')}和{subj2.replace('_', ' ')}都是{obj.replace('_', ' ')}的{pred}吗？"
            sentences.append(sentence)
    else:
        for subj1, subj2, pred, obj in query:
            sentence = (f"Given the concept of prerequisite relationships in education, are both of <{subj1.replace('_', ' ')}> and <{subj2.replace('_', ' ')}> <{pred}> <{obj.replace('_', ' ')}>?")
            sentences.append(sentence)
    return sentences


def query_2p_to_sentence_w_query_one_hop_reasoning(query):
    zh_flag = 0
    for q in query:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[-1])

    sentences = []
    if zh_flag > 0:
        for subj1, subj2, pred, obj in query:
            sentence = f"给定Resource Description Framework用于描述教育学前置知识点：<知识点1> <知识点2> <关联> <知识点3> 代表知识点1和知识点2同时是知识点3的关联，以下关于知识的描述是否正确？<{subj1.replace('_', ' ')}> <{subj2.replace('_', ' ')}> <{pred}> <{obj.replace('_', ' ')}>"
            # the order is changed to match the Chinese common language
            sentences.append(sentence)
    else:
        for subj1, subj2, pred, obj in query:
            sentence = (f"Given the Resource Description Framework to describe the concept of prerequisite relationships in education: <entity 1> <entity 2> <relationship> <entity 3> means entity 1 and entity 2 are the relationship of entity 3 simultaneously, is <{subj1.replace('_', ' ')}> <{subj2.replace('_', ' ')}> <{pred}> <{obj.replace('_', ' ')}> correct?")
            sentences.append(sentence)
    return sentences


def query_3p_to_sentence_one_hop_reasoning(query):
    zh_flag = 0
    for q in query:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[-1])

    sentences = []
    if zh_flag > 0:
        for subj1, subj2, subj3, pred, obj in query:
            sentence = (f"给定教育学前置知识点的场景，请问{subj1.replace('_', ' ')}、{subj2.replace('_', ' ')}和{subj3.replace('_', ' ')}"
                        f"都是{obj.replace('_', ' ')}的{pred}吗？")
            sentences.append(sentence)
    else:
        for subj1, subj2, subj3, pred, obj in query:
            sentence = (f"Given the concept of prerequisite relationships in education, are all of {subj1.replace('_', ' ')}, {subj2.replace('_', ' ')} and {subj3.replace('_', ' ')}"
                        f" {pred} {obj.replace('_', ' ')}?")
            sentences.append(sentence)
    return sentences


def query_3p_to_sentence_w_query_one_hop_reasoning(query):
    zh_flag = 0
    for q in query:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[-1])

    sentences = []
    if zh_flag > 0:
        for subj1, subj2, subj3, pred, obj in query:
            sentence = f"给定Resource Description Framework用于描述教育学前置知识点：<知识点1> <知识点2> <知识点3> <关联> <知识点4>代表知识点1、知识点2和知识点3同时是知识点4的关联，以下关于知识的描述是否正确？<{subj1.replace('_', ' ')}> <{subj2.replace('_', ' ')}> <{subj3.replace('_', ' ')}> <{pred}> <{obj.replace('_', ' ')}>"
            # the order is changed to match the Chinese common language
            sentences.append(sentence)
    else:
        for subj1, subj2, subj3, pred, obj in query:
            sentence = (f"Given the Resource Description Framework to describe the concept of prerequisite relationships in education: <entity 1> <entity 2> <entity 3> <relationship> <entity 4> means entity 1, entity 2 and entity 3 are the relationship of entity 4 simultaneously, is <{subj1.replace('_', ' ')}> <{subj2.replace('_', ' ')}> <{subj3.replace('_', ' ')}> <{pred}> <{obj.replace('_', ' ')}>")
            sentences.append(sentence)
    return sentences


def node_pairs_to_sentence_relation_extraction(node_pairs):
    zh_flag = 0
    for q in node_pairs:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[1])

    sentences = []
    for node1, node2, _, _ in node_pairs:
        if zh_flag > 0:
            sentence = f"给定教育学前置知识点的场景，请问{node1.replace('_', ' ')}是{node2.replace('_', ' ')}的直接前置知识点吗？"
            sentences.append(sentence)
        else:
            sentence = (f"Given the concept of prerequisite relationships in education, is {node1.replace('_', ' ')} the direct prerequisite knowledge of {node2.replace('_', ' ')}? "
                        )
            sentences.append(sentence)
    return sentences


def node_pairs_to_sentence_w_float_relation_extraction(node_pairs):
    zh_flag = 0
    for q in node_pairs:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[1])

    sentences = []
    for node1, node2, _, _ in node_pairs:
        if zh_flag > 0:
            sentence = (f"给定教育学前置知识点的场景，请问{node1.replace('_', ' ')}是{node2.replace('_', ' ')}的直接前置知识点的可能性是多大？"
                        f"请给我一个0.0到1.0之间的浮点数。")
            sentences.append(sentence)
        else:
            sentence = (f"Given the concept of prerequisite relationships in education, how essential is {node1.replace('_', ' ')} as a direct prerequisite of "
                        f"{node2.replace('_', ' ')}? Assign a float value between 0.0 and 1.0.")
            sentences.append(sentence)
    return sentences


def subgraph_node_pairs_to_sentence_relation_extraction(subgraphs):
    zh_flag = 0
    for q in subgraphs:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0][0])
        zh_flag += is_chinese(q[0][1])

    sentences = []
    for node_pairs in subgraphs:
        if zh_flag > 0:
            cache = f"给定教育学前置知识点的场景，接下来的问题是关于以下知识点的关系的。"
        else:
            cache = f"Given the concept of prerequisite relationships in education, the following questions are about the relationships between the following knowledge points."
        for node1, node2, _, _ in node_pairs:
            if zh_flag > 0:
                part = f"请问{node1.replace('_', ' ')}是{node2.replace('_', ' ')}的直接前置知识点吗？"
                cache = cache + part
            else:
                part = (f"Is {node1.replace('_', ' ')} the direct prerequisite knowledge of {node2.replace('_', ' ')}? "
                        )
                cache = cache + ' ' + part
        sentences.append(cache)
    return sentences


def subgraph_node_pairs_to_sentence_w_float_relation_extraction(subgraphs):
    zh_flag = 0
    for q in subgraphs:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0][0])
        zh_flag += is_chinese(q[0][1])

    sentences = []
    for node_pairs in subgraphs:
        if zh_flag > 0:
            cache = f"给定教育学前置知识点的场景，接下来的问题是关于以下知识点的关系的。"
        else:
            cache = f"Given the concept of prerequisite relationships in education, the following questions are about the relationships between the following knowledge points."
        for node1, node2, _, _ in node_pairs:
            if zh_flag > 0:
                part = (f"请问{node1.replace('_', ' ')}是{node2.replace('_', ' ')}的直接前置知识点的可能性是多大？"
                        f"请给我一个0.0到1.0之间的浮点数。")
                cache = cache + part
            else:
                part = (f"How essential is {node1.replace('_', ' ')} as a direct prerequisite of "
                        f"{node2.replace('_', ' ')}? Assign a float value between 0.0 and 1.0.")
                cache = cache + ' ' + part
        sentences.append(cache)
    return sentences


"""
The following functions are for the one-shot tasks
"""


def triplet_to_sentence_one_hop_reasoning_one_shot(triplets, gt_triplets):
    """
    One-shot reasoning questions with ground truth
    :param triplets:
    :param gt_triplets:
    :return:
    """
    if len(gt_triplets) == 1:

        zh_flag = 0
        for triplet in triplets:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(triplet[0])
            zh_flag += is_chinese(triplet[-1])

        sentences = []
        for subj_gt, pred_gt, obj_gt in gt_triplets:
            if zh_flag > 0:
                for subj, pred, obj in triplets:
                    sentence = (f"已知{subj_gt.replace('_', ' ')}是{obj_gt.replace('_', ' ')}的{pred_gt}。"
                                f"请问{subj.replace('_', ' ')}是{obj.replace('_', ' ')}的{pred}吗？")
                    sentences.append(sentence)
            else:
                for subj, pred, obj in triplets:
                    sentence = (f"{subj_gt.replace('_', ' ')} {pred_gt} {obj_gt.replace('_', ' ')}."
                                f"Is {subj.replace('_', ' ')} {pred} {obj.replace('_', ' ')}?")
                    sentences.append(sentence)
        return sentences

    elif len(gt_triplets) > 1:
        zh_flag = 0
        for triplet in triplets:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(triplet[0])
            zh_flag += is_chinese(triplet[-1])

        sentences = []
        if zh_flag > 0:
            for subj, pred, obj in triplets:
                for i in range(len(gt_triplets)):
                    gt_triplets_nested = random.choice(gt_triplets[i])
                    subj_gt, pred_gt, obj_gt = gt_triplets_nested
                    sentence = (f"已知{subj_gt.replace('_', ' ')}是{obj_gt.replace('_', ' ')}的{pred_gt}。"
                                f"请问{subj.replace('_', ' ')}是{obj.replace('_', ' ')}的{pred}吗？")
                    sentences.append(sentence)
        else:
            for subj, pred, obj in triplets:
                for i in range(len(gt_triplets)):
                    gt_triplets_nested = random.choice(gt_triplets[i])
                    subj_gt, pred_gt, obj_gt = gt_triplets_nested
                    sentence = (f"{subj_gt.replace('_', ' ')} {pred_gt} {obj_gt.replace('_', ' ')}."
                                f"Is {subj.replace('_', ' ')} {pred} {obj.replace('_', ' ')}?")
                    sentences.append(sentence)
        return sentences
    else:
        return []


def triplet_to_sentence_w_triplets_one_hop_reasoning_one_shot(triplets, gt_triplets):
    if len(gt_triplets) == 1:
        zh_flag = 0
        for triplet in triplets:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(triplet[0])
            zh_flag += is_chinese(triplet[-1])

        sentences = []
        for subj_gt, pred_gt, obj_gt in gt_triplets:
            if zh_flag > 0:
                for subj, pred, obj in triplets:
                    sentence = (f"已知以下关于知识的描述<{obj_gt}, {pred_gt}, {subj_gt}>。"
                                f"以下关于知识的描述是否正确？<{obj}, {pred}, {subj}>")
                    # the order is changed to match the Chinese common language
                    sentences.append(sentence)
            else:
                for subj, pred, obj in triplets:
                    sentence = (f"The following relationship is correct: <{subj_gt}, {pred_gt}, {obj_gt}>. "
                                f"Is the following relationship about the knowledge correct? <{subj}, {pred}, {obj}>")
                    sentences.append(sentence)
        return sentences
    elif len(gt_triplets) > 1:
        zh_flag = 0
        for triplet in triplets:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(triplet[0])
            zh_flag += is_chinese(triplet[-1])

        sentences = []
        if zh_flag > 0:
            for subj, pred, obj in triplets:
                for i in range(len(gt_triplets)):
                    gt_triplets_nested = random.choice(gt_triplets[i])
                    subj_gt, pred_gt, obj_gt = gt_triplets_nested
                    sentence = (f"已知以下关于知识的描述<{obj_gt}, {pred_gt}, {subj_gt}>。"
                                f"以下关于知识的描述是否正确？<{obj}, {pred}, {subj}>")
                    # the order is changed to match the Chinese common language
                    sentences.append(sentence)
        else:
            for subj, pred, obj in triplets:
                for i in range(len(gt_triplets)):
                    gt_triplets_nested = random.choice(gt_triplets[i])
                    subj_gt, pred_gt, obj_gt = gt_triplets_nested
                    sentence = (f"The following relationship is correct: <{subj_gt}, {pred_gt}, {obj_gt}>. "
                                f"Is the following relationship about the knowledge correct? <{subj}, {pred}, {obj}>")
                    sentences.append(sentence)
        return sentences
    else:
        return []


def paths_to_sentence_two_hop_reasoning_one_shot(two_hop_paths, gt_paths):
    """
    Direct Inference Questions of two-hops
    :param gt_paths:
    :param two_hop_paths: from construct_two_hop_paths
    :return:
    """
    if len(gt_paths) == 1:
        zh_flag = 0
        for path in two_hop_paths:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(path[0])
            zh_flag += is_chinese(path[-1])

        sentences = []
        for subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt in gt_paths:
            if zh_flag > 0:
                for subj, rel1, successor, rel2, second_hop in two_hop_paths:
                    sentence = (f"已知因为{subj_gt.replace('_', ' ')}是{successor_gt.replace('_', ' ')}的{rel1_gt},"
                                f"且{successor_gt.replace('_', ' ')}是{second_hop_gt.replace('_', ' ')}的{rel2_gt},"
                                f"由此得到{subj_gt.replace('_', ' ')}是{second_hop_gt.replace('_', ' ')}的{rel2}。"
                                f"请问如果{subj.replace('_', ' ')}是{successor.replace('_', ' ')}的{rel1}，"
                                f"且{successor.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}，"
                                f"那么{subj.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}吗？")
                    sentences.append(sentence)
            else:
                for subj, rel1, successor, rel2, second_hop in two_hop_paths:
                    sentence = (f"It is sure that if "
                                f"{subj_gt.replace('_', ' ')} is {rel1_gt} {successor_gt.replace('_', ' ')},"
                                f"and {successor_gt.replace('_', ' ')} is {rel2_gt} {second_hop_gt.replace('_', ' ')},"
                                f"then {subj_gt.replace('_', ' ')} is {rel2_gt} {second_hop_gt.replace('_', ' ')}."
                                f"If {subj.replace('_', ' ')} is {rel1} {successor.replace('_', ' ')}, "
                                f"and {successor.replace('_', ' ')} is {rel2} {second_hop.replace('_', ' ')}, "
                                f"then is {subj.replace('_', ' ')} {rel2} {second_hop.replace('_', ' ')}?")
                    sentences.append(sentence)
        return sentences
    elif len(gt_paths) > 1:
        zh_flag = 0
        for path in two_hop_paths:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(path[0])
            zh_flag += is_chinese(path[-1])

        sentences = []
        if zh_flag > 0:
            for subj, rel1, successor, rel2, second_hop in two_hop_paths:
                for i in range(len(gt_paths)):
                    gt_path_nested = random.choice(gt_paths[i])
                    subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt = gt_path_nested
                    sentence = (f"已知因为{subj_gt.replace('_', ' ')}是{successor_gt.replace('_', ' ')}的{rel1_gt},"
                                f"且{successor_gt.replace('_', ' ')}是{second_hop_gt.replace('_', ' ')}的{rel2_gt},"
                                f"由此得到{subj_gt.replace('_', ' ')}是{second_hop_gt.replace('_', ' ')}的{rel2}。"
                                f"请问如果{subj.replace('_', ' ')}是{successor.replace('_', ' ')}的{rel1}，"
                                f"且{successor.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}，"
                                f"那么{subj.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}吗？")
                    sentences.append(sentence)
        else:
            for subj, rel1, successor, rel2, second_hop in two_hop_paths:
                for i in range(len(gt_paths)):
                    gt_path_nested = random.choice(gt_paths[i])
                    subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt = gt_path_nested
                    sentence = (f"It is sure that if "
                                f"{subj_gt.replace('_', ' ')} is {rel1_gt} {successor_gt.replace('_', ' ')},"
                                f"and {successor_gt.replace('_', ' ')} is {rel2_gt} {second_hop_gt.replace('_', ' ')},"
                                f"then {subj_gt.replace('_', ' ')} is {rel2_gt} {second_hop_gt.replace('_', ' ')}."
                                f"If {subj.replace('_', ' ')} is {rel1} {successor.replace('_', ' ')}, "
                                f"and {successor.replace('_', ' ')} is {rel2} {second_hop.replace('_', ' ')}, "
                                f"then is {subj.replace('_', ' ')} {rel2} {second_hop.replace('_', ' ')}?")
                    sentences.append(sentence)
        return sentences
    else:
        return []


def paths_to_sentence_w_paths_two_hop_reasoning_one_shot(two_hop_paths, gt_paths):
    if len(gt_paths) == 1:
        zh_flag = 0
        for triplet in two_hop_paths:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(triplet[0])
            zh_flag += is_chinese(triplet[-1])

        sentences = []
        for subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt in gt_paths:
            if zh_flag > 0:
                for subj, rel1, successor, rel2, second_hop in two_hop_paths:
                    sentence = (f"已知以下知识关联：<{second_hop_gt}, {rel2_gt}, {successor_gt},"
                                f" {rel1_gt}, {subj_gt}>，"
                                f"可以得到以下关于知识的描述：<{second_hop}, {rel2}, {subj_gt}>。"
                                f"已知有以下知识关联：<{second_hop}, {rel2}, {successor}, {rel1}, {subj}>，"
                                f"以下关于知识的描述是否正确？<{second_hop}, {rel2}, {subj}>")
                    # the order is changed to match the Chinese common language
                    sentences.append(sentence)
            else:
                for subj, rel1, successor, rel2, second_hop in two_hop_paths:
                    sentence = (f"It is sure that if we have the following relation of knowledge <{subj_gt}, {rel1_gt}, {successor_gt},"
                                f" {rel2_gt}, {second_hop_gt}>, "
                                f"then we can get the following relationship about the knowledge: <{subj_gt}, {rel2_gt}, {second_hop_gt}>."
                                f"If we have the following relation of knowledge <{subj}, {rel1}, {successor}, {rel2}, {second_hop}>, "
                                f"then is the following relationship about the knowledge correct? <{subj}, {rel2}, {second_hop}>")
                    sentences.append(sentence)
        return sentences
    elif len(gt_paths) > 1:
        zh_flag = 0
        for triplet in two_hop_paths:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(triplet[0])
            zh_flag += is_chinese(triplet[-1])

        sentences = []
        if zh_flag > 0:
            for subj, rel1, successor, rel2, second_hop in two_hop_paths:
                for i in range(len(gt_paths)):
                    gt_path_nested = random.choice(gt_paths[i])
                    subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt = gt_path_nested
                    sentence = (f"已知以下知识关联：<{second_hop_gt}, {rel2_gt}, {successor_gt},"
                                f" {rel1_gt}, {subj_gt}>，"
                                f"可以得到以下关于知识的描述：<{second_hop}, {rel2}, {subj_gt}>。"
                                f"已知有以下知识关联：<{second_hop}, {rel2}, {successor}, {rel1}, {subj}>，"
                                f"以下关于知识的描述是否正确？<{second_hop}, {rel2}, {subj}>")
                    # the order is changed to match the Chinese common language
                    sentences.append(sentence)
        else:
            for subj, rel1, successor, rel2, second_hop in two_hop_paths:
                for i in range(len(gt_paths)):
                    gt_path_nested = random.choice(gt_paths[i])
                    subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt = gt_path_nested
                    sentence = (
                        f"It is sure that if we have the following relation of knowledge <{subj_gt}, {rel1_gt}, {successor_gt},"
                        f" {rel2_gt}, {second_hop_gt}>, "
                        f"then we can get the following relationship about the knowledge: <{subj_gt}, {rel2_gt}, {second_hop_gt}>."
                        f"If we have the following relation of knowledge <{subj}, {rel1}, {successor}, {rel2}, {second_hop}>, "
                        f"then is the following relationship about the knowledge correct? <{subj}, {rel2}, {second_hop}>")
                    sentences.append(sentence)
        return sentences
    else:
        return []


def paths_to_sentence_three_hop_reasoning_one_shot(three_hop_paths, gt_paths):
    """
    Direct Inference Questions of three-hops with one-shot
    :param gt_paths:
    :param three_hop_paths: from construct_three_hop_paths
    :return:
    """
    if len(gt_paths) == 1:
        zh_flag = 0
        for path in three_hop_paths:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(path[0])
            zh_flag += is_chinese(path[-1])

        sentences = []
        for subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt, rel3_gt, third_hop_gt in gt_paths:
            if zh_flag > 0:
                for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
                    sentence = (f"已知因为{subj_gt.replace('_', ' ')}是{successor_gt.replace('_', ' ')}的{rel1_gt},"
                                f"且{successor_gt.replace('_', ' ')}是{second_hop_gt.replace('_', ' ')}的{rel2_gt},"
                                f"且{second_hop_gt.replace('_', ' ')}是{third_hop_gt.replace('_', ' ')}的{rel3_gt},"
                                f"由此得到{subj_gt.replace('_', ' ')}是{third_hop_gt.replace('_', ' ')}的{rel3_gt}。"
                                f"请问如果{subj.replace('_', ' ')}是{successor.replace('_', ' ')}的{rel1}，"
                                f"且{successor.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}，"
                                f"且{second_hop.replace('_', ' ')}是{third_hop.replace('_', ' ')}的{rel3}，"
                                f"那么{subj.replace('_', ' ')}是{third_hop.replace('_', ' ')}的{rel3}吗？")
                    sentences.append(sentence)
            else:
                for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
                    sentence = (f"It is sure that if "
                                f"{subj_gt.replace('_', ' ')} is {rel1_gt} {successor_gt.replace('_', ' ')},"
                                f"and {successor_gt.replace('_', ' ')} is {rel2_gt} {second_hop_gt.replace('_', ' ')},"
                                f"and {second_hop_gt.replace('_', ' ')} is {rel3_gt} {third_hop_gt.replace('_', ' ')},"
                                f"then {subj_gt.replace('_', ' ')} is {rel3_gt} {third_hop_gt.replace('_', ' ')}."
                                f"If {subj.replace('_', ' ')} is {rel1} {successor.replace('_', ' ')}, "
                                f"and {successor.replace('_', ' ')} is {rel2} {second_hop.replace('_', ' ')}, "
                                f"and {second_hop.replace('_', ' ')} is {rel3} {third_hop.replace('_', ' ')}, "
                                f"then is {subj.replace('_', ' ')} {rel3} {third_hop.replace('_', ' ')}?")
                    sentences.append(sentence)
        return sentences
    elif len(gt_paths) > 1:
        zh_flag = 0
        for path in three_hop_paths:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(path[0])
            zh_flag += is_chinese(path[-1])

        sentences = []
        if zh_flag > 0:
            for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
                for i in range(len(gt_paths)):
                    gt_path_nested = random.choice(gt_paths[i])
                    subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt, rel3_gt, third_hop_gt = gt_path_nested
                    sentence = (f"已知因为{subj_gt.replace('_', ' ')}是{successor_gt.replace('_', ' ')}的{rel1_gt},"
                                f"且{successor_gt.replace('_', ' ')}是{second_hop_gt.replace('_', ' ')}的{rel2_gt},"
                                f"且{second_hop_gt.replace('_', ' ')}是{third_hop_gt.replace('_', ' ')}的{rel3_gt},"
                                f"由此得到{subj_gt.replace('_', ' ')}是{third_hop_gt.replace('_', ' ')}的{rel3_gt}。"
                                f"请问如果{subj.replace('_', ' ')}是{successor.replace('_', ' ')}的{rel1}，"
                                f"且{successor.replace('_', ' ')}是{second_hop.replace('_', ' ')}的{rel2}，"
                                f"且{second_hop.replace('_', ' ')}是{third_hop.replace('_', ' ')}的{rel3}，"
                                f"那么{subj.replace('_', ' ')}是{third_hop.replace('_', ' ')}的{rel3}吗？")
                    sentences.append(sentence)
        else:
            for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
                for i in range(len(gt_paths)):
                    gt_path_nested = random.choice(gt_paths[i])
                    subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt, rel3_gt, third_hop_gt = gt_path_nested
                    sentence = (f"It is sure that if "
                                f"{subj_gt.replace('_', ' ')} is {rel1_gt} {successor_gt.replace('_', ' ')},"
                                f"and {successor_gt.replace('_', ' ')} is {rel2_gt} {second_hop_gt.replace('_', ' ')},"
                                f"and {second_hop_gt.replace('_', ' ')} is {rel3_gt} {third_hop_gt.replace('_', ' ')},"
                                f"then {subj_gt.replace('_', ' ')} is {rel3_gt} {third_hop_gt.replace('_', ' ')}."
                                f"If {subj.replace('_', ' ')} is {rel1} {successor.replace('_', ' ')}, "
                                f"and {successor.replace('_', ' ')} is {rel2} {second_hop.replace('_', ' ')}, "
                                f"and {second_hop.replace('_', ' ')} is {rel3} {third_hop.replace('_', ' ')}, "
                                f"then is {subj.replace('_', ' ')} {rel3} {third_hop.replace('_', ' ')}?")
                    sentences.append(sentence)
        return sentences
    else:
        return []


def paths_to_sentence_w_paths_three_hop_reasoning_one_shot(three_hop_paths, gt_paths):
    if len(gt_paths) == 1:
        zh_flag = 0
        for path in three_hop_paths:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(path[0])
            zh_flag += is_chinese(path[-1])

        sentences = []
        for subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt, rel3_gt, third_hop_gt in gt_paths:
            if zh_flag > 0:
                for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
                    sentence = (f"已知以下知识关联：<{third_hop_gt}, {rel3_gt}, {second_hop_gt}, {rel2_gt}, {successor_gt},"
                                f" {rel1_gt}, {subj_gt}>，"
                                f"可以得到以下关于知识的描述：<{third_hop_gt.replace('_', ' ')}, {rel2_gt}, {subj_gt}>。"
                                f"已知有以下知识关联：<{third_hop}, {rel3}, {second_hop}, {rel2}, {successor},"
                                f" {rel1}, {subj}>，"
                                f"以下关于知识的描述是否正确？<{third_hop}, {rel3}, {subj}>")
                    # the order is changed to match the Chinese common language
                    sentences.append(sentence)
            else:
                for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
                    sentence = (f"It is sure that if we have the following relation of knowledge <{subj_gt}, {rel1_gt}, {successor_gt},"
                                f" {rel2_gt}, {second_hop_gt}, {rel3_gt}, {third_hop_gt}>, "
                                f"then we can get the following relationship about the knowledge: <{subj_gt}, {rel3_gt}, {third_hop_gt}>."
                                f"If we have the following relation of knowledge <{subj}, {rel1}, {successor}, {rel2}, "
                                f"{second_hop}, {rel3}, {third_hop}>, "
                                f"then is the following relationship about the knowledge correct? <{subj}, {rel3}, {third_hop}>")
                    sentences.append(sentence)
        return sentences
    elif len(gt_paths) > 1:
        zh_flag = 0
        for path in three_hop_paths:
            if zh_flag > 0:
                break
            zh_flag += is_chinese(path[0])
            zh_flag += is_chinese(path[-1])

        sentences = []
        if zh_flag > 0:
            for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
                for i in range(len(gt_paths)):
                    gt_path_nested = random.choice(gt_paths[i])
                    subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt, rel3_gt, third_hop_gt = gt_path_nested
                    sentence = (
                        f"已知以下知识关联：<{third_hop_gt}, {rel3_gt}, {second_hop_gt}, {rel2_gt}, {successor_gt},"
                        f" {rel1_gt}, {subj_gt}>，"
                        f"可以得到以下关于知识的描述：<{third_hop_gt.replace('_', ' ')}, {rel2_gt}, {subj_gt}>。"
                        f"已知有以下知识关联：<{third_hop}, {rel3}, {second_hop}, {rel2}, {successor},"
                        f" {rel1}, {subj}>，"
                        f"以下关于知识的描述是否正确？<{third_hop}, {rel3}, {subj}>")
                    # the order is changed to match the Chinese common language
                    sentences.append(sentence)
        else:
            for subj, rel1, successor, rel2, second_hop, rel3, third_hop in three_hop_paths:
                for i in range(len(gt_paths)):
                    gt_path_nested = random.choice(gt_paths[i])
                    subj_gt, rel1_gt, successor_gt, rel2_gt, second_hop_gt, rel3_gt, third_hop_gt = gt_path_nested
                    sentence = (
                        f"It is sure that if we have the following relation of knowledge <{subj_gt}, {rel1_gt}, {successor_gt},"
                        f" {rel2_gt}, {second_hop_gt}, {rel3_gt}, {third_hop_gt}>, "
                        f"then we can get the following relationship about the knowledge: <{subj_gt}, {rel3_gt}, {third_hop_gt}>."
                        f"If we have the following relation of knowledge <{subj}, {rel1}, {successor}, {rel2}, "
                        f"{second_hop}, {rel3}, {third_hop}>, "
                        f"then is the following relationship about the knowledge correct? <{subj}, {rel3}, {third_hop}>")
                    sentences.append(sentence)
        return sentences
    else:
        return []


def query_2p_to_sentence_one_hop_reasoning_one_shot(query, query_gt):
    zh_flag = 0
    for q in query:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[-1])

    sentences = []
    if zh_flag > 0:
        for (subj1, subj2, pred, obj), (subj1_gt, subj2_gt, pred_gt, obj_gt) in zip(query, query_gt):
            sentence = (
                f"已知{subj1_gt.replace('_', ' ')}和{subj2_gt.replace('_', ' ')}都是{obj_gt.replace('_', ' ')}的{pred_gt}。"
                f"请问{subj1.replace('_', ' ')}和{subj2.replace('_', ' ')}都是{obj.replace('_', ' ')}的{pred}吗？")
            sentences.append(sentence)
    else:
        for (subj1, subj2, pred, obj), (subj1_gt, subj2_gt, pred_gt, obj_gt) in zip(query, query_gt):
            sentence = (
                f"If both {subj1_gt.replace('_', ' ')} and {subj2_gt.replace('_', ' ')} are "
                f"{obj_gt.replace('_', ' ')}'s {pred_gt}. "
                f"Are both of {subj1.replace('_', ' ')} and {subj2.replace('_', ' ')} {pred} "
                f"{obj.replace('_', ' ')}?")
            sentences.append(sentence)
    return sentences


def query_2p_to_sentence_w_query_one_hop_reasoning_one_shot(query, query_gt):
    zh_flag = 0
    for q in query:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[-1])

    sentences = []
    if zh_flag > 0:
        for (subj1, subj2, pred, obj), (subj1_gt, subj2_gt, pred_gt, obj_gt) in zip(query, query_gt):
            sentence = (
                f"已知以下知识关联：<{obj_gt}, {pred_gt}, <{subj1_gt}, {subj2_gt}>>, "
                f"以下关于知识的描述是否正确？<{obj}, {pred}, <{subj1}, {subj2}>>"
            )
            # the order is changed to match the Chinese common language
            sentences.append(sentence)
    else:
        for (subj1, subj2, pred, obj), (subj1_gt, subj2_gt, pred_gt, obj_gt) in zip(query, query_gt):
            sentence = (
                f"The following relationship about the knowledge is correct: <<{subj1_gt}, {subj2_gt}>, "
                f"{pred_gt}, {obj_gt}>."
                f"Is the following relationship about the knowledge correct? <<{subj1}, {subj2}>, "
                f"{pred}, {obj}>")
            sentences.append(sentence)
    return sentences


def query_3p_to_sentence_one_hop_reasoning_one_shot(query, query_gt):
    zh_flag = 0
    for q in query:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[-1])

    sentences = []
    if zh_flag > 0:
        for (subj1, subj2, subj3, pred, obj), (subj1_gt, subj2_gt, subj3_gt, pred_gt, obj_gt) in zip(query, query_gt):
            sentence = (
                f"已知{subj1_gt.replace('_', ' ')}、{subj2_gt.replace('_', ' ')}和{subj3_gt.replace('_', ' ')}都是"
                f"{obj_gt.replace('_', ' ')}的{pred_gt}。"
                f"请问{subj1.replace('_', ' ')}、{subj2.replace('_', ' ')}和{subj3.replace('_', ' ')}"
                f"都是{obj.replace('_', ' ')}的{pred}吗？"
            )
            sentences.append(sentence)
    else:
        for (subj1, subj2, subj3, pred, obj), (subj1_gt, subj2_gt, subj3_gt, pred_gt, obj_gt) in zip(query, query_gt):
            sentence = (
                f"If all of {subj1_gt.replace('_', ' ')}, {subj2_gt.replace('_', ' ')} and {subj3_gt.replace('_', ' ')}"
                f" {pred_gt} {obj_gt.replace('_', ' ')}?"
                f"Are all of {subj1.replace('_', ' ')}, {subj2.replace('_', ' ')} and {subj3.replace('_', ' ')}"
                f" {pred} {obj.replace('_', ' ')}?"
            )
            sentences.append(sentence)
    return sentences


def query_3p_to_sentence_w_query_one_hop_reasoning_one_shot(query, query_gt):
    zh_flag = 0
    for q in query:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[-1])

    sentences = []
    if zh_flag > 0:
        for (subj1, subj2, subj3, pred, obj), (subj1_gt, subj2_gt, subj3_gt, pred_gt, obj_gt) in zip(query,
                                                                                                     query_gt):
            sentence = (
                f"已知以下知识关联：<{obj_gt}, {pred_gt}, <{subj1_gt}, {subj2_gt}, {subj3_gt}>>, "
                f"以下关于知识的描述是否正确？<{obj}, {pred}, <{subj1}, {subj2}, {subj3}>>"
            )
            # the order is changed to match the Chinese common language
            sentences.append(sentence)
    else:
        for (subj1, subj2, subj3, pred, obj), (subj1_gt, subj2_gt, subj3_gt, pred_gt, obj_gt) in zip(query,
                                                                                                     query_gt):
            sentence = (
                f"The following relationship about the knowledge is correct: <<{subj1_gt}, {subj2_gt}, {subj3_gt}>, "
                f"{pred_gt}, {obj_gt}>."
                f"Is the following relationship about the knowledge correct? <<{subj1}, {subj2}, {subj3}>, "
                f"{pred}, {obj}>"
            )
            sentences.append(sentence)
    return sentences


def node_pairs_to_sentence_relation_extraction_one_shot(node_pairs, t_node_pairs=None):
    zh_flag = 0
    for q in node_pairs:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[1])

    gt_node_pairs = [(node1, node2, has_edge, relation) for node1, node2, has_edge, relation in node_pairs if has_edge]

    sentences = []
    for node1, node2, _, _ in node_pairs:
        gt_node_pair = random.choice(gt_node_pairs)
        node1_gt, node2_gt, _, _ = gt_node_pair
        if zh_flag > 0:
            sentence = (
                f"已知{node1_gt.replace('_', ' ')}是{node2_gt.replace('_', ' ')}的直接前置知识点。"
                f"请问{node1.replace('_', ' ')}是{node2.replace('_', ' ')}的直接前置知识点吗？"
            )
            sentences.append(sentence)
        else:
            sentence = (
                f"If {node1_gt.replace('_', ' ')} is the direct prerequisite knowledge of {node2_gt.replace('_', ' ')}, "
                f"is {node1.replace('_', ' ')} the direct prerequisite knowledge of {node2.replace('_', ' ')}? "
            )
            sentences.append(sentence)
    return sentences


def node_pairs_to_sentence_w_float_relation_extraction_one_shot(node_pairs):
    zh_flag = 0
    for q in node_pairs:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0])
        zh_flag += is_chinese(q[1])

    gt_node_pairs = [(node1, node2, has_edge, relation) for node1, node2, has_edge, relation in node_pairs if has_edge]
    sentences = []

    for node1, node2, _, _ in node_pairs:
        gt_node_pair = random.choice(gt_node_pairs)
        node1_gt, node2_gt, _, _ = gt_node_pair
        if zh_flag > 0:
            sentence = (
                f"已知{node1_gt.replace('_', ' ')}是{node2_gt.replace('_', ' ')}的直接前置知识点的可能性是1.0。"
                f"请问{node1.replace('_', ' ')}是{node2.replace('_', ' ')}的直接前置知识点的可能性是多大？"
                f"请给我一个0.0到1.0之间的浮点数。"
            )
            sentences.append(sentence)
        else:
            sentence = (
                f"If the probability of {node1.replace('_', ' ')} being a direct prerequisite for understanding "
                f"{node2.replace('_', ' ')}is 1.0."
                f"How essential is {node1.replace('_', ' ')} as a direct prerequisite for understanding "
                f"{node2.replace('_', ' ')}? Assign a float value between 0.0 and 1.0."
            )
            sentences.append(sentence)
    return sentences


def subgraph_node_pairs_to_sentence_relation_extraction_one_shot(subgraphs):
    zh_flag = 0
    for q in subgraphs:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0][0])
        zh_flag += is_chinese(q[0][1])

    sentences = []
    for node_pairs in subgraphs:
        node_pairs_with_edges = [pair for pair in node_pairs if pair[2]]

        if zh_flag > 0:
            cache = f"接下来的问题是关于以下知识点的关系的。"
        else:
            cache = f"The following questions are about the relationships between the following knowledge points."
        for node1, node2, _, _ in node_pairs:
            sampled_node_pair = random.sample(node_pairs_with_edges, 1)[0]
            if zh_flag > 0:
                part = (
                    f"已知{sampled_node_pair[0].replace('_', ' ')}是{sampled_node_pair[1].replace('_', ' ')}的直接前置知识点，"
                    f"请问{node1.replace('_', ' ')}是{node2.replace('_', ' ')}的直接前置知识点吗？"
                )
                cache = cache + part
            else:
                part = (
                    f"If {sampled_node_pair[0].replace('_', ' ')} is the direct prerequisite knowledge of "
                    f"{sampled_node_pair[1].replace('_', ' ')}, "
                    f"Is {node1.replace('_', ' ')} the direct prerequisite knowledge of {node2.replace('_', ' ')}? "
                )
                cache = cache + ' ' + part
        sentences.append(cache)
    return sentences


def subgraph_node_pairs_to_sentence_w_float_relation_extraction_one_shot(subgraphs):
    zh_flag = 0
    for q in subgraphs:
        if zh_flag > 0:
            break
        zh_flag += is_chinese(q[0][0])
        zh_flag += is_chinese(q[0][1])

    sentences = []
    for node_pairs in subgraphs:
        node_pairs_with_edges = [pair for pair in node_pairs if pair[2]]
        if zh_flag > 0:
            cache = f"接下来的问题是关于以下知识点的关系的。"
        else:
            cache = f"The following questions are about the relationships between the following knowledge points."
        for node1, node2, _, _ in node_pairs:
            sampled_node_pair = random.sample(node_pairs_with_edges, 1)[0]
            if zh_flag > 0:
                part = (
                    f"已知{sampled_node_pair[0].replace('_', ' ')}是{sampled_node_pair[1].replace('_', ' ')}"
                    f"的直接前置知识点的可能性是1.0。"
                    f"请问{node1.replace('_', ' ')}是{node2.replace('_', ' ')}的直接前置知识点的可能性是多大？"
                    f"请给我一个0.0到1.0之间的浮点数。"
                )
                cache = cache + part
            else:
                part = (
                    f"If the probability of {sampled_node_pair[0].replace('_', ' ')} being a direct prerequisite for "
                    f"understanding {sampled_node_pair[1].replace('_', ' ')} is 1.0."
                    f"How essential is {node1.replace('_', ' ')} as a direct prerequisite for understanding "
                    f"{node2.replace('_', ' ')}? Assign a float value between 0.0 and 1.0."
                )
                cache = cache + ' ' + part
        sentences.append(cache)
    return sentences