import json
from src.mcqgenerator.mcqGenerator import final_chain
import PyPDF2
import traceback
from langchain_core.output_parsers import JsonOutputParser
import ast

with open(r"D:\MCQ Generator\response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

def read_file(file):
    if file.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("error reading PDF File")
    
    elif file.endswith(".txt"):
        with open(file, "r") as file:
            return file.read().encode("utf-8")

    else:
        raise Exception("Unwanted file format")

text = read_file(r"D:\MCQ Generator\data.txt")
response = final_chain(
                    {
                        "text":text,
                        "number":3,
                        "subject":"transformers",
                        "tone":"beginner",
                        "response_json":RESPONSE_JSON,
                    }
                )

quiz_dict = ast.literal_eval(response.get('quiz'))



formatted_data = []
for key, value in quiz_dict.items():
    options = ' | '.join([f"{k}: {v}" for k, v in value['options'].items()])
    question_data = {
        'question_no': key,
        'question': value['question'],
        'options': options,
        'correct': value['correct']
    }
    formatted_data.append(question_data)

import pandas as pd

df = pd.DataFrame(formatted_data)
print(df)



# try:
#     quiz_dict = json.loads(quiz)

#     formatted_data = []
#     for key, value in quiz_dict.items():
#         options = ' | '.join([f"{k}: {v}" for k, v in value['options'].items()])
#         question_data = {
#             'question_no': key,
#             'question': value['question'],
#             'options': options,
#             'correct': value['correct']
#         }
#         formatted_data.append(question_data)

#     print(formatted_data)

# except Exception as e:
#     traceback.print_exception(type(e), e, e.__traceback__)

