This is the folder of codes of this benchmark. 

Here are relevant instructions to reproduce the results in this project.


#### 1. Clone the Repo


First, please clone the GitHub Repo at: [https://github.com/ai-for-edu/Evaluating-Large-Language-Models-with-Educational-Knowledge-Graphs-on-Prerequisite-Relationships](https://github.com/ai-for-edu/Evaluating-Large-Language-Models-with-Educational-Knowledge-Graphs-on-Prerequisite-Relationships):

```sh
$> git clone https://github.com/ai-for-edu/Evaluating-Large-Language-Models-with-Educational-Knowledge-Graphs-on-Prerequisite-Relationships
```

Please note that although the data is provided in a separate folder /data/, there is a folder /benchmark/data/ holding exactly the same data and in similar setup.
So there is no need to copy the data from /data/ to /benchmark/data/ .

Redirect to /benchmark/ folder:
```sh
$> cd benchmark/
```

#### 2. Install requirements
```sh
$> pip install -r requirements.txt
```

#### 3. Generate question queries

To generate questions on all of the tasks and on all of the datasets:
```sh
$> python generate_question_query.py
```
Feel free to play around the code to customize the query generation.

#### 4. Set API connection

Please fill in the 'API_KEY' in /benchmark/Edu_KG_Eval/global_config.py.
Besides that, also modify the following connection details in function generate_answer of class ApiFoxAnswer:

- HTTPS path in 'conn = http.client.HTTPSConnection()'
- 'User-Agent' in dictionary 'headers'

#### 5. Get answers from LLMs

To get the answers on all of the queries generated in the last step:
```sh
$> python obtain_llm_answers.py
```

#### 6. Evaluate LLM answers

As this step may require manual check, we provide some methods may be helpful to calculate accuracy, precision, recall, AUROC and AUPRC in the following script: 'auto_eval_test.py'.