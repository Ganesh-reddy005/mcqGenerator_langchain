import os 
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import get_table_data,read_file
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcq_generator.MCQ_Generator import generate_chain
from src.mcq_generator.logger import logging

#loading json file
with open("/Users/ganeshreddybodireddy/Desktop/genai_mcq_project/response.json",'r') as file:
    RESPONSE_JSON=json.load(file)

#creating title
st.title("MCQ's Generator- With Langchain")

#creating form
with st.form("user_inputs"):
    #file upload
    upload_file=st.file_uploader("Upload Your File Here")

    #input fields 
    mcq_count=st.number_input("No. of MCQS: ",min_value=1, max_value=25)

    #subject input
    mcq_subject=st.text_input("Enter the subject: ", max_chars=25)

    #quiz tome
    mcq_tone=st.text_input("complexity level : ", max_chars=50)

    #adding button
    button =st.form_submit_button("Create MCQ's")

    #checking if button is clicked and all other fields are entered correctly
    if button and upload_file is not None and mcq_count and mcq_subject and mcq_tone:
        with st.spinner("loading.."):
            try:
                text=read_file(upload_file)
                #counting tokens
                with get_openai_callback() as cb:
                    response=generate_chain(
                    {
                    'text':text,
                    'number':mcq_count,
                    'subject':mcq_subject,
                    'tone':mcq_tone,
                    'RESPONSE_JSON':json.dumps(RESPONSE_JSON)
                    }
                )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error "+str(e))
            else:
                print(f"total tokens: {cb.total_tokens}")
                print(f"Prompt tokens: {cb.prompt_tokens}")
                print(f"Completion tokens: {cb.completion_tokens}")

                if isinstance(response,dict):
                    #extracting quiz data from response
                    quiz=response.get("quiz",None)
                    if quiz:
                        table_data=get_table_data(quiz)
                       # st.write(table_data)
                        if table_data and isinstance(table_data, list) and all(isinstance(row, dict) for row in table_data):
                            df=pd.DataFrame(table_data)
                            df.index+=1
                            st.table(df)
                            #displaying review in a box as well
                            st.text_area(label="review",value=response["review"])
                        else:
                            st.error("Error in Table")
                    else:
                        st.warning("No quiz data found in response.")
                else:
                    st.write(response)

                    



