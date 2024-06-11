API_KEY = ''  # OpenAI API key, or other key

DBE_KT22 = 'data/DBE-KT22/DBE-KT22.graphml'
WDKG_Course = 'data/WDKG/WDKG-Course.graphml'
WDKG_KnowledgePoints = 'data/WDKG/WDKG-KnowledgePoints.graphml'  # no-two-hops  # no p2_query
Junyi_Prerequisites = 'data/Junyi/Junyi-Prerequisites.graphml'

DATA_PATHS = [DBE_KT22, WDKG_Course, WDKG_KnowledgePoints, Junyi_Prerequisites]

MODEL_NAME = 'gpt-3.5-turbo'  # OpenAI model name,
# may also use: 'qwen-turbo', 'gpt-4-turbo-preview', 'gpt-4-0125-preview', 'moonshot-v1-128k',
# 'yi-34b-chat-0205', 'claude-3-haiku-20240307'
