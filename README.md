# :sparkles: Evaluating Large Language Models with Educational Knowledge Graphs: Challenges with Prerequisite Relationships and Multi-Hop Reasoning :sparkles:

<p align="center">
  <img src="websites/websites/assets/theme/iamges/favicon.png" alt="Project Icon" width="150"/>
</p>


![Last Commit](https://img.shields.io/github/last-commit/divelab/DIG)
[![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by]. 

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey

[**Project Website**](https://ai-for-edu.github.io/Evaluating-Large-Language-Models-with-Educational-Knowledge-Graphs-on-Prerequisite-Relationships/)

This repo maintains and updates benchmark on evaluating LLMs with Educational KGs, with a focus on prerequistie relationships. :smile:

## Installation

Download the whole reporitory. Or clone:


```sh
$> git clone https://github.com/ai-for-edu/Evaluating-Large-Language-Models-with-Educational-Knowledge-Graphs-on-Prerequisite-Relationships
```

## How to benchmark

After clone or download the Repositorym redirect to /benchmark/ folder:
```sh
$> cd benchmark/
```

#### 1. Install requirements
```sh
$> pip install -r requirements.txt
```

#### 2. Generate question queries

To generate questions on all of the tasks and on all of the datasets:
```sh
$> python generate_question_query.py
```
Feel free to play around the code to customize the query generation.

#### 3. Set API connection

Please fill in the 'API_KEY' in /benchmark/Edu_KG_Eval/global_config.py.
Besides that, also modify the following connection details in function generate_answer of class ApiFoxAnswer:

- HTTPS path in 'conn = http.client.HTTPSConnection()'
- 'User-Agent' in dictionary 'headers'

#### 4. Get answers from LLMs

To get the answers on all of the queries generated in the last step:
```sh
$> python obtain_llm_answers.py
```

#### 5. Evaluate LLM answers

As this step may require manual check, we provide some methods may be helpful to calculate accuracy, precision, recall, AUROC and AUPRC in the following script: 'auto_eval_test.py'.


## Dataset

The KGs with KCs and prerequsites relationships dataset are in /data folder with each subfolder inside holding one KG. 


## Citation

TBA

## Contact

Authors: 

Aoran Wang: aoran.wang@uni.lu, Chaoli Zhang: chaolizcl@zjnu.edu.cn, Jun Pang: jun.pang@uni.lu, Qingsong Wen: qingsongedu@gmail.com
