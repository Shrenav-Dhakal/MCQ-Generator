import streamlit as st
import os
import json
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from src.mcqgenerator.utils import read_file, get_table_data

from src.mcqgenerator.mcqGenerator import final_chain
from src.mcqgenerator.logger import logging

with open(r"D:\MCQ Generator\response.json", "r") as file:
    RESPONSE_JSON = json.load(file)


st.title("MCQ Generator ** Created by Shreenav Dhakal**")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a Text file or a pdf file")

    number = st.number_input("No of MCQ to generate:", min_value=3, max_value=50)

    subject = st.text_input("Enter Subject", max_chars=20)

    tone = st.selectbox("Enter difficulty level: ", ['Beginner', 'Intermediate', 'Advanced'])

    button = st.form_submit_button("Create MCQ's")

    if button and uploaded_file is not None and number and subject and tone:
        with st.spinner("loading"):
            try:
                text = read_file(uploaded_file)
                response = final_chain(
                    {
                        "text":text,
                        "number":number,
                        "subject":subject,
                        "tone":tone,
                        "response_json":RESPONSE_JSON,
                    }
                )
            except Exception as e:
                st.write("Error :", e)
            else:
                if isinstance(response, dict):
                    quiz = response.get('quiz',None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            st.table(df)
                            st.text_area("Review ", value=response['review'])
                        else:
                            st.error("Error in table data")
                else:
                    st.write(response)


