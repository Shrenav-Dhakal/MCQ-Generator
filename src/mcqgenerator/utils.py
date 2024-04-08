# helper file
import os
import json
import PyPDF2
import traceback
import ast

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("error reading PDF File")
    
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception("Unwanted file format")


def get_table_data(quiz_str):
    try:
        quiz_dict = ast.literal_eval(quiz_str)
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
        return formatted_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None