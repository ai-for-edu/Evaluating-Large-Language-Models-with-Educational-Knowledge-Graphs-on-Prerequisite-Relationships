import networkx as nx
import pandas as pd

# For example, loading from a pickle file
# Ensure your file path and format are correctly specified
data_path = '/Users/aaronwang/PycharmProjects/LLMs_n_KGs_for_Education/data/WDKG/WDKG-KnowledgePoints.graphml'
G = nx.read_graphml(data_path)

# Print out the first few nodes to check their attributes
print("Before: ")
for node, attrs in list(G.nodes(data=True))[:5]:  # Adjust the slice for larger graphs
    print(node, attrs)
print("-" * 25)
# Iterate over all nodes and their attributes
for node, attrs in G.nodes(data=True):
    # Check if the 'course_name' attribute exists
    if 'knowledge_point' in attrs:
        # Assign the value of 'course_name' to a new attribute 'name'
        attrs['name'] = attrs['knowledge_point']
        # Optionally, delete the old 'course_name' attribute
        del attrs['knowledge_point']
print("After: ")
# Print out the first few nodes to check their attributes
for node, attrs in list(G.nodes(data=True))[:5]:  # Adjust the slice for larger graphs
    print(node, attrs)

nx.write_graphml(G, data_path)