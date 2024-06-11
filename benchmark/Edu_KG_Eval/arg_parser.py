import time
import argparse
import pickle
import os
import datetime
import numpy as np


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset', type=str, default='DBE_KT22',
        help="The name of the dataset: ['DBE_KT22', 'WDKG_Course', 'WDKG_KnowledgePoints', 'Junyi_Prerequisites']."
    )
    parser.add_argument(
        '--llm', type=str, default='gemini-1.5-pro',
        help="Name of the llm to use for evaluation: "
             "['gpt-4', 'qwen-turbo', 'moonshot-v1-128k', "
             "'claude-3-haiku-20240307', 'yi-34b-chat-0205', 'gemini-1.5-pro']."
    )
    parser.add_argument('--store_path', type=str, default='logs', help="Path to store logs.")
    parser.add_argument('--b-shuffle', action='store_true', default=False,
                        help='Shuffle the data for benchmarking?.')
    args = parser.parse_args()

    return args