from Edu_KG_Eval.global_config import *
from Edu_KG_Eval.arg_parser import parse_args
from Edu_KG_Eval.eval_pipeline import generate_one_hop_data, generate_two_hop_data, generate_three_hop_data
from Edu_KG_Eval.eval_pipeline import generate_two_predecessors_data, generate_three_predecessors_data
from Edu_KG_Eval.eval_pipeline import generate_node_pairs_data, generate_sub_graph_data
import time

def generate_questions(args):
    data_path0 = 'data/DBE-KT22/DBE-KT22.graphml'
    data_path1 = 'data/WDKG/WDKG-Course.graphml'
    data_path2 = 'data/WDKG/WDKG-KnowledgePoints.graphml'  # no-two-hops  # no p2_query
    data_path3 = 'data/Junyi/Junyi-Prerequisites.graphml'  # no p2_query

    paths = [data_path0, data_path1, data_path2, data_path3]
    for path in paths:
        # Choose what to do by uncommenting the function calls in generate_questions()
        generate_one_hop_data(args, path)
        generate_two_hop_data(args, path)
        generate_three_hop_data(args, path)
        generate_two_predecessors_data(args, path)
        generate_three_predecessors_data(args, path)
        generate_node_pairs_data(args, path)
        generate_sub_graph_data(args, path)


if __name__ == "__main__":
    # Record the start time
    start_time = time.time()

    args = parse_args()

    generate_questions(args)

    # Record the end time
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")


