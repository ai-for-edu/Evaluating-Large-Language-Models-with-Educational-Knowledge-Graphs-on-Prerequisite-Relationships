from Edu_KG_Eval.global_config import *
from Edu_KG_Eval import llm_engine
from Edu_KG_Eval.arg_parser import parse_args
from Edu_KG_Eval.eval_utils import ReadQuestionsFromLocal
import time


def get_one_hop_answers(questions, model, use_sampled=True):
    if model == 'gpt-4':
        first_run = True
    else:
        first_run = False
    if first_run:
        use_sampled = False
    time_checkpoint_0 = time.time()
    # # For One-hop positive LLM answers
    selected = questions.read_one_hop(
        negative=False,
        sampling=True,
        samples=50,
        use_sampled=use_sampled
    )
    keys = list(selected.keys())
    time_checkpoint_1 = time.time()
    data_loading_time = time_checkpoint_1 - time_checkpoint_0
    print(f"The loading time is {data_loading_time} seconds.")

    for key in keys:
        print("--Now dealing with ", key, " --")
        key_string = key.split('/')[-2] + '-' + key.split('/')[-1]
        key_string = key_string.replace('.', '-')
        llm_client = llm_engine.ApiFoxAnswer(modelname=model)  # args.llm
        llm_client.log_answer(
            key_strings=key_string,
            premise_questions=selected[key]
        )
        time_checkpoint_2 = time.time()
        print(f"The llm answer time for <{key_string}> is {time_checkpoint_2 - time_checkpoint_1} seconds.")
        time_checkpoint_1 = time_checkpoint_2
        # save at 'logs/answers/' + key_string + model + '_answers.txt'
        # save at 'logs/answers/' + key_string + model + '_answers.csv'

    # dealing with negative samples
    selected = questions.read_one_hop(
        negative=True,
        sampling=True,
        samples=50,
        use_sampled=use_sampled
    )
    keys = list(selected.keys())
    time_checkpoint_1 = time.time()
    data_loading_time = time_checkpoint_1 - time_checkpoint_0
    print(f"The loading time is {data_loading_time} seconds.")
    for key in keys:
        print("--Now dealing with ", key, " --")
        key_string = key.split('/')[-2] + '-' + key.split('/')[-1]
        key_string = key_string.replace('.', '-')
        llm_client = llm_engine.ApiFoxAnswer(modelname=model)  # args.llm
        llm_client.log_answer(
            key_strings=key_string,
            premise_questions=selected[key]
        )
        time_checkpoint_2 = time.time()
        print(f"The llm answer time for <{key_string}> is {time_checkpoint_2 - time_checkpoint_1} seconds.")
        time_checkpoint_1 = time_checkpoint_2
        # save at 'logs/answers/' + key_string + model + '_answers.txt'
        # save at 'logs/answers/' + key_string + model + '_answers.csv'
    return


def two_hop_answers_basic(
        questions,
        model,
        use_sampled=True,
        negative=False,
        path_distruption=False,
        invert_relations=False,
        replace_intermediate=False,
        replace_terminal=False,):

    if model == 'gpt-4':
        first_run = True
    else:
        first_run = False
    if first_run:
        use_sampled = False
    time_checkpoint_0 = time.time()
    # For Two-hop LLM answers
    selected = questions.read_two_hop(
        negative=negative,
        path_distruption=path_distruption,
        invert_relations=invert_relations,
        replace_intermediate=replace_intermediate,
        replace_terminal=replace_terminal,
        sampling=True,
        samples=32,
        use_sampled=use_sampled
    )
    keys = list(selected.keys())
    time_checkpoint_1 = time.time()
    data_loading_time = time_checkpoint_1 - time_checkpoint_0
    print(f"The loading time is {data_loading_time} seconds.")

    for key in keys:
        print("--Now dealing with ", key, " --")
        key_string = key.split('/')[-2] + '-' + key.split('/')[-1]
        key_string = key_string.replace('.', '-')
        llm_client = llm_engine.ApiFoxAnswer(modelname=model)  # args.llm
        llm_client.log_answer(
            key_strings=key_string,
            premise_questions=selected[key]
        )
        time_checkpoint_2 = time.time()
        print(f"The llm answer time for <{key_string}> is {time_checkpoint_2 - time_checkpoint_1} seconds.")
        time_checkpoint_1 = time_checkpoint_2
        # save at 'logs/answers/' + key_string + model + '_answers.txt'
        # save at 'logs/answers/' + key_string + model + '_answers.csv'
    return


def get_two_hop_answers(questions, model, use_sampled=True):
    two_hop_answers_basic(
        questions=questions,
        model=model,
        negative=False,
        path_distruption=False,
        invert_relations=False,
        replace_intermediate=False,
        replace_terminal=False,
    )
    two_hop_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        path_distruption=True,
        invert_relations=False,
        replace_intermediate=False,
        replace_terminal=False,
    )
    two_hop_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        path_distruption=False,
        invert_relations=True,
        replace_intermediate=False,
        replace_terminal=False,
    )
    two_hop_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        path_distruption=False,
        invert_relations=False,
        replace_intermediate=True,
        replace_terminal=False,
    )
    two_hop_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        path_distruption=False,
        invert_relations=False,
        replace_intermediate=False,
        replace_terminal=True,
    )
    return


def three_hop_answers_basic(
        questions,
        model,
        use_sampled=True,
        negative=False,
    ):

    if model == 'gpt-4':
        first_run = True
    else:
        first_run = False
    if first_run:
        use_sampled = False
    time_checkpoint_0 = time.time()
    # For Three-hop LLM answers
    selected = questions.read_three_hop(
        negative=negative,
        sampling=True,
        samples=25,
        use_sampled=use_sampled
    )
    keys = list(selected.keys())
    time_checkpoint_1 = time.time()
    data_loading_time = time_checkpoint_1 - time_checkpoint_0
    print(f"The loading time is {data_loading_time} seconds.")

    for key in keys:
        print("--Now dealing with ", key, " --")
        key_string = key.split('/')[-2] + '-' + key.split('/')[-1]
        key_string = key_string.replace('.', '-')
        llm_client = llm_engine.ApiFoxAnswer(modelname=model)  # args.llm
        llm_client.log_answer(
            key_strings=key_string,
            premise_questions=selected[key]
        )
        time_checkpoint_2 = time.time()
        print(f"The llm answer time for <{key_string}> is {time_checkpoint_2 - time_checkpoint_1} seconds.")
        time_checkpoint_1 = time_checkpoint_2
        # save at 'logs/answers/' + key_string + model + '_answers.txt'
        # save at 'logs/answers/' + key_string + model + '_answers.csv'
    return


def get_three_hop_answers(questions, model, use_sampled=True):
    three_hop_answers_basic(
        questions=questions,
        model=model,
        negative=False,
    )
    three_hop_answers_basic(
        questions=questions,
        model=model,
        negative=True,
    )
    return


def conjunction_two_answers_basic(
        questions,
        model,
        use_sampled=True,
        negative=False,
        p0=False,
        p1=False,
        two=False,
    ):

    if model == 'gpt-4':
        first_run = True
    else:
        first_run = False
    if first_run:
        use_sampled = False
    time_checkpoint_0 = time.time()
    # For Three-hop LLM answers
    selected = questions.read_two_predecessor(
            negative=negative,
            p0=p0,
            p1=p1,
            two=two,
            sampling=True,
            samples=20,
            use_sampled=use_sampled
        )
    keys = list(selected.keys())
    time_checkpoint_1 = time.time()
    data_loading_time = time_checkpoint_1 - time_checkpoint_0
    print(f"The loading time is {data_loading_time} seconds.")

    for key in keys:
        print("--Now dealing with ", key, " --")
        key_string = key.split('/')[-2] + '-' + key.split('/')[-1]
        key_string = key_string.replace('.', '-')
        llm_client = llm_engine.ApiFoxAnswer(modelname=model)  # args.llm
        llm_client.log_answer(
            key_strings=key_string,
            premise_questions=selected[key]
        )
        time_checkpoint_2 = time.time()
        print(f"The llm answer time for <{key_string}> is {time_checkpoint_2 - time_checkpoint_1} seconds.")
        time_checkpoint_1 = time_checkpoint_2
        # save at 'logs/answers/' + key_string + model + '_answers.txt'
        # save at 'logs/answers/' + key_string + model + '_answers.csv'
    return


def get_conjunction_two_answers(questions, model, use_sampled=True):
    conjunction_two_answers_basic(
        questions=questions,
        model=model,
        negative=False,
        p0=False,
        p1=False,
        two=False,
    )
    conjunction_two_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        p0=True,
        p1=False,
        two=False,
    )
    conjunction_two_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        p0=False,
        p1=True,
        two=False,
    )
    conjunction_two_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        p0=False,
        p1=False,
        two=True,
    )
    return


def conjunction_three_answers_basic(
        questions,
        model,
        use_sampled=True,
        negative=False,
        one_p0=False,
        one_p1=False,
        one_p2=False,
        two_p01=False,
        two_p02=False,
        two_p12=False,
        three=False,
    ):

    if model == 'gpt-4':
        first_run = True
    else:
        first_run = False
    if first_run:
        use_sampled = False
    time_checkpoint_0 = time.time()
    # For Three-hop LLM answers
    selected = questions.read_three_predecessor(
        negative=negative,
        one_p0=one_p0,
        one_p1=one_p1,
        one_p2=one_p2,
        two_p01=two_p01,
        two_p02=two_p02,
        two_p12=two_p12,
        three=three,
        sampling=True,
        samples=20,
        use_sampled=use_sampled
    )
    keys = list(selected.keys())
    time_checkpoint_1 = time.time()
    data_loading_time = time_checkpoint_1 - time_checkpoint_0
    print(f"The loading time is {data_loading_time} seconds.")

    for key in keys:
        print("--Now dealing with ", key, " --")
        key_string = key.split('/')[-2] + '-' + key.split('/')[-1]
        key_string = key_string.replace('.', '-')
        llm_client = llm_engine.ApiFoxAnswer(modelname=model)  # args.llm
        llm_client.log_answer(
            key_strings=key_string,
            premise_questions=selected[key]
        )
        time_checkpoint_2 = time.time()
        print(f"The llm answer time for <{key_string}> is {time_checkpoint_2 - time_checkpoint_1} seconds.")
        time_checkpoint_1 = time_checkpoint_2
        # save at 'logs/answers/' + key_string + model + '_answers.txt'
        # save at 'logs/answers/' + key_string + model + '_answers.csv'
    return


def get_conjunction_three_answers(questions, model, use_sampled=True):
    conjunction_three_answers_basic(
        questions=questions,
        model=model,
        negative=False,
        one_p0=False,
        one_p1=False,
        one_p2=False,
        two_p01=False,
        two_p02=False,
        two_p12=False,
        three=False,
    )
    conjunction_three_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        one_p0=True,
        one_p1=False,
        one_p2=False,
        two_p01=False,
        two_p02=False,
        two_p12=False,
        three=False,
    )
    conjunction_three_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        one_p0=False,
        one_p1=True,
        one_p2=False,
        two_p01=False,
        two_p02=False,
        two_p12=False,
        three=False,
    )
    conjunction_three_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        one_p0=False,
        one_p1=False,
        one_p2=True,
        two_p01=False,
        two_p02=False,
        two_p12=False,
        three=False,
    )
    conjunction_three_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        one_p0=False,
        one_p1=False,
        one_p2=False,
        two_p01=True,
        two_p02=False,
        two_p12=False,
        three=False,
    )
    conjunction_three_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        one_p0=False,
        one_p1=False,
        one_p2=False,
        two_p01=False,
        two_p02=True,
        two_p12=False,
        three=False,
    )
    conjunction_three_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        one_p0=False,
        one_p1=False,
        one_p2=False,
        two_p01=False,
        two_p02=False,
        two_p12=True,
        three=False,
    )
    conjunction_three_answers_basic(
        questions=questions,
        model=model,
        negative=True,
        one_p0=False,
        one_p1=False,
        one_p2=False,
        two_p01=False,
        two_p02=False,
        two_p12=False,
        three=True,
    )
    return


def get_node_pairs_answers(questions, model, use_sampled=True):
    if model == 'gpt-4':
        first_run = True
    else:
        first_run = False
    if first_run:
        use_sampled = False
    time_checkpoint_0 = time.time()

    # For Node-pairs LLM answers
    selected = questions.read_node_pairs(
        one_shot=False,
        sampling=True,
        samples=25,
        use_sampled=use_sampled
    )

    keys = list(selected.keys())
    time_checkpoint_1 = time.time()
    data_loading_time = time_checkpoint_1 - time_checkpoint_0
    print(f"The loading time is {data_loading_time} seconds.")

    for key in keys:
        print("--Now dealing with ", key, " --")
        key_string = key.split('/')[-2] + '-' + key.split('/')[-1]
        key_string = key_string.replace('.', '-')
        llm_client = llm_engine.ApiFoxAnswer(modelname=model)  # args.llm
        llm_client.log_answer(
            key_strings=key_string,
            premise_questions=selected[key]
        )
        time_checkpoint_2 = time.time()
        print(f"The llm answer time for <{key_string}> is {time_checkpoint_2 - time_checkpoint_1} seconds.")
        time_checkpoint_1 = time_checkpoint_2
        # save at 'logs/answers/' + key_string + model + '_answers.txt'
        # save at 'logs/answers/' + key_string + model + '_answers.csv'
    return


def sub_graph_answers_basic(
        questions,
        model,
        use_sampled=True,
        size_5=False,
        size_10=False,
        size_15=False,
):
    if model == 'gpt-4':
        first_run = True
    else:
        first_run = False
    if first_run:
        use_sampled = False
    time_checkpoint_0 = time.time()

    # For Sub-graph LLM answers
    selected = questions.read_sub_graph(
        size_5=size_5,
        size_10=size_10,
        size_15=size_15,
        sampling=True,
        samples=5,
        use_sampled=use_sampled
    )
    keys = list(selected.keys())
    time_checkpoint_1 = time.time()
    data_loading_time = time_checkpoint_1 - time_checkpoint_0
    print(f"The loading time is {data_loading_time} seconds.")

    for key in keys:
        print("--Now dealing with ", key, " --")
        key_string = key.split('/')[-2] + '-' + key.split('/')[-1]
        key_string = key_string.replace('.', '-')
        llm_client = llm_engine.ApiFoxAnswer(modelname=model)  # args.llm
        llm_client.log_answer(
            key_strings=key_string,
            premise_questions=selected[key]
        )
        time_checkpoint_2 = time.time()
        print(f"The llm answer time for <{key_string}> is {time_checkpoint_2 - time_checkpoint_1} seconds.")
        time_checkpoint_1 = time_checkpoint_2
        # save at 'logs/answers/' + key_string + model + '_answers.txt'
        # save at 'logs/answers/' + key_string + model + '_answers.csv'
    return


def get_subgraph_answers(questions, model, use_sampled=True):
    sub_graph_answers_basic(
        questions=questions,
        model=model,
        size_5=True,
        size_10=False,
        size_15=False,
    )
    sub_graph_answers_basic(
        questions=questions,
        model=model,
        size_5=False,
        size_10=True,
        size_15=False,
    )
    sub_graph_answers_basic(
        questions=questions,
        model=model,
        size_5=False,
        size_10=False,
        size_15=True,
    )
    return


def get_llm_answers(args):
    data_path0 = 'data/DBE-KT22/DBE-KT22.graphml'
    data_path1 = 'data/WDKG/WDKG-Course.graphml'
    data_path2 = 'data/WDKG/WDKG-KnowledgePoints.graphml'  # no-two-hops  # no p2_query # no three-hops
    data_path3 = 'data/Junyi/Junyi-Prerequisites.graphml'  # no p2_query  # no p3_query

    paths = [data_path0, data_path1, data_path2, data_path3]

    models = ['gpt-4', 'qwen-turbo', 'moonshot-v1-128k', 'claude-3-haiku-20240307', 'yi-34b-chat-0205', 'gemini-1.5-pro']

    use_sampled = True
    first_run = False
    for model in models:
        for path in paths:
            time_checkpoint_0 = time.time()
            # read questions from local:e.g. one-hop
            print("----- Dealing with ", path, " -----")
            questions = ReadQuestionsFromLocal(path)
            get_one_hop_answers(questions, model, use_sampled)
            get_two_hop_answers(questions, model, use_sampled)
            get_three_hop_answers(questions, model, use_sampled)
            get_conjunction_two_answers(questions, model, use_sampled)
            get_conjunction_three_answers(questions, model, use_sampled)
            get_node_pairs_answers(questions, model, use_sampled)
            get_subgraph_answers(questions, model, use_sampled)
            print("Choose what to do by uncommenting the function calls in generate_questions()")

            print("All answers of ", model, " on ", path.split('/')[-1], " have been obtained.")
    return


def main(args):

    get_llm_answers()


if __name__ == "__main__":
    start_time = time.time()
    args = parse_args()

    # feel free to play around with the args to customize the function calls
    get_llm_answers(args)


