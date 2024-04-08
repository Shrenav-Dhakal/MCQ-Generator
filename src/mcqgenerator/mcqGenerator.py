import os
import json
import langchain_google_genai as genai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

from src.mcqgenerator.utils import read_file, get_table_data

from dotenv import load_dotenv
load_dotenv()

google_api = os.getenv("GOOGLE_API_KEY") 

model = genai.GoogleGenerativeAI(google_api_key=google_api, model="gemini-1.0-pro", temperature=0.3)



template = """
Text : {text} 
You are an expert MCQ maker. Based on the above text , you are to create \
{number} MCQ questions for {subject} students in {tone} tone.
Avoid asking questions from the text that are related to date.
Make sure the questions are not repeated and also confirm the question along with answer \
from the given text. You are to provide output in RESPONE_JSON format. 
Make sure you create {number} questions.
### RESPONSE_JSON
{response_json}
"""

quiz_template = PromptTemplate(
    input_variables=['text','number', 'subject', 'tone', 'response_json'],
    template=template
)

quiz_chain = LLMChain(llm=model, prompt=quiz_template, output_key="quiz", verbose=True)

template2 = """
You are an expert grammar evaluator and question checker.
Given the MCQ quiz questions for {subject} students, you are to \
evaluate the {quiz} questions to check its complexity. Make sure the question \
consist less than 50 words and also determine whether the questions align with \
the capabilites of the students. Make sure to update the question and also maintain the \
provided tone.
## MCQ quiz questions
{quiz}
Provid the MCQ quiz question in a dictionary.
"""

evaluate_prompt = PromptTemplate(
    template = template2,
    input_variables=['subject', 'quiz']
)

evaluate_chain = LLMChain(llm=model, prompt=evaluate_prompt, output_key='review', verbose=True)

final_chain = SequentialChain(chains=[quiz_chain, evaluate_chain],
                              input_variables=['text', 'number', 'subject', 'tone', 'response_json'],
                              output_variables=['quiz', 'review'],verbose=True)







