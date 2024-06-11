import re


def extract_id_contents(file_path):
    # Open and read the markdown file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression to find all substrings starting with "id": and ending at the next period
    pattern = r'"id":"([^\"]*)\"'

    # Find all matches of the pattern
    matches = re.findall(pattern, content)

    # Return the list of matches
    return matches


file_path = '/Edu_KG_Eval/available_models.md'

# Call the function and print the results
id_contents = extract_id_contents(file_path)
for i in id_contents:
    print(i)
# print(id_contents)
print("Number of matches:", len(id_contents))