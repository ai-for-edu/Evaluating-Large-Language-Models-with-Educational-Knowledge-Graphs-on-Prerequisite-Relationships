import openai
import os
import time
from .global_config import *
import http.client
import json, csv


class GPTAnswer:
    """
    This class is used to generate answers for the questions using GPT-3.5 or GPT-3.5-turbo model from OpenAI.
    """
    def __init__(self, modelname="gpt-3.5-turbo"):
        openai.organization = os.getenv("OPENAI_ORG_ID")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.modelname = modelname

    def generate_answer(self, premise_questions):
        answers = []
        if "gpt-3.5" in self.modelname:
            for premise_question in premise_questions:
                response = openai.ChatCompletion.create(
                                model=self.modelname,
                                messages=[
                                    {"role": "user", "content": premise_question}
                                    ],
                                max_tokens=512,
                                n=1,
                                stop=None,
                                temperature=0,
                            )
            answers.append(response["choices"][0].message.content)
        else:
            completion = openai.Completion.create(
                            engine=self.modelname,
                            prompts=premise_questions,
                            max_tokens=512,
                            n=1,
                            stop=None,
                            temperature=0,
                        )
            for choice in completion.choices:
                answers.append(choice.text)
        return answers

    def log_answer(self, qtype, premise_questions={}, output_path=""):
        question_ids = list(premise_questions.keys())
        premise_questions = list(premise_questions.values())
        predicted_answers = self.generate_answer(premise_questions)
        time.sleep(60)
        for idx, prediction in enumerate(predicted_answers):
            with open(os.path.join(f"{output_path}",f"{qtype}_{question_ids[idx]}_predicted_answer.txt"),"w") as prediction_file:
                print(prediction, file=prediction_file)


class ApiFoxAnswer:
    """
    This class is used to generate answers for the questions using v1/chat/completions model from Apifox.
    Has to be used with the Apifox API key.
    """
    def __init__(self, modelname="gpt-3.5-turbo"):
        # openai.organization = os.getenv("OPENAI_ORG_ID")
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        self.modelname = modelname
        self.key = API_KEY

    def generate_answer(self, premise_questions):
        answers = []
        usage = []
        for i, premise_question in enumerate(premise_questions):
            conn = http.client.HTTPSConnection("api2.aigcbest.top")
            payload = json.dumps({
                "model": self.modelname,
                "messages": [
                    {
                        "role": "user",
                        "content": premise_question
                    }
                ]
            })
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.key}',
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/v1/chat/completions", payload, headers)
            res = conn.getresponse()
            try:
                data = res.read()
                data_dict = json.loads(data)
                if self.modelname == 'gemini-1.5-pro':
                    time.sleep(10)
                if data_dict is None or data_dict.get('choices') is None or data_dict.get('choices')[0].get('message') is None:
                    answers.append('No answer found.')
                    usage.append({'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0})
                else:
                    answers.append(data_dict.get('choices')[0].get('message').get('content'))
                    usage.append(data_dict.get('usage'))
            except http.client.IncompleteRead as e:
                print(f'An IncompleteRead error occurred: {e}')
                answers.append(f'An IncompleteRead error occurred: {e}')
                usage.append({'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0})

            except json.decoder.JSONDecodeError as e:
                print(f'A JSONDecodeError occurred: {e}')
                answers.append(f'A JSONDecodeError occurred: {e}')
                usage.append({'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0})
            if i % 10 == 0:
                print(f"Question {i+1} completed.")

        return answers, usage

    def calculate_usage(self, usage):
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        for token_dict in usage:
            prompt_tokens += token_dict.get('prompt_tokens', 0)
            completion_tokens += token_dict.get('completion_tokens', 0)
            total_tokens += token_dict.get('total_tokens', 0)
        return prompt_tokens, completion_tokens, total_tokens

    def log_answer(self, key_strings, premise_questions=[], output_path="logs/answers/"):
        if key_strings == 'DBE-KT22-one-hop-questions-json':
            print("Already done this one")
            return
        predicted_answers, usages = self.generate_answer(premise_questions)
        time.sleep(10)
        file_path = os.path.join(f"{output_path}", f"{key_strings}_{self.modelname}_answer.csv")
        data = [{"question": q, "answer": a, "usage": u} for q, a, u in zip(premise_questions, predicted_answers, usages)]
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["question", "answer", "usage"])
            writer.writeheader()
            writer.writerows(data)
        prompt_tokens, completion_tokens, total_tokens = self.calculate_usage(usages)
        print("Total prompt tokens: ", prompt_tokens, "Total completion tokens: ", completion_tokens,
              "Total tokens: ", total_tokens)
        print("Data has been written to", file_path)