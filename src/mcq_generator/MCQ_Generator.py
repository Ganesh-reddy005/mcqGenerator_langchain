import os
import json
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,get_table_data
from src.mcq_generator.logger import logging

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


load_dotenv()
KEY=os.getenv("MY_API_KEY")

llm=ChatOpenAI( model_name="google/gemma-2-9b-it:free", base_url="https://openrouter.ai/api/v1",openai_api_key=KEY,temperature=0.4)

template="""
Text:{text}
You are a expert in making Multiple Choice Questions. Given the above text its your Job to create {number} multiple choice questions
for {subject} students with {tone} tone (difficulty level).
Make sure the questions are not repeated and all the questions to be conforming the text as well.
Make sure to format your questions in json format - RESPONSE_JSON as given below and use it as guide.
Ensure to only make {number} questions.
###RESPONSE_JSON
{RESPONSE_JSON}.
If you cannot make MCQ's with the given data of if there is no enough data given just ask them to provide more data.
Make sure to format your response as raw JSON only. Do not include Markdown formatting like ```json or any explanation text.Just return the JSON object directly.

"""


quiz_generator_prompt=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=template
)

#now will start creating chains
quiz_chain=LLMChain(llm=llm,prompt=quiz_generator_prompt,
                    output_key='quiz',
                    verbose=True,
                    )


#next prompt to ensure correctness and difficulty level
template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of teh question and give a complete analysis of the quiz if the students
will be able to unserstand the questions and answer them. Only use at max 50 words for complexity analysis. 
if the quiz is not at par with the cognitive and analytical abilities of the students,\
update tech quiz questions which needs to be changed  and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evalution_prompt=PromptTemplate(
    input_variables=['subject','quiz'],
    template=template2
)
review_chain=LLMChain(llm=llm,prompt=quiz_evalution_prompt,output_key="review",verbose=True)

#using SequentialChain to put all together
generate_chain=SequentialChain(chains=[quiz_chain,review_chain],input_variables=['RESPONSE_JSON', 'number', 'subject', 'text', 'tone'],
                               output_variables=["quiz", "review"], verbose=True)
