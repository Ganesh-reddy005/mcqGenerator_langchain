import PyPDF2
import json
import os
import traceback

#creating function to read file
def read_file(file):
    if(file.name.endswith('.pdf')):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                page_text=page.extract_text()
                if page_text:
                    text+=page_text
            return text
        except Exception as e:
            raise Exception("Error loading file "+str(e))
        
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise Exception("Unsupported file format ")
    
#to create data frame
def get_table_data(quiz_data):
    try:
        if isinstance(quiz_data, str):
            quiz_data = quiz_data.strip()
            if quiz_data.startswith("```json"):
                quiz_data = quiz_data[len("```json"):].strip()
            if quiz_data.endswith("```"):
                quiz_data = quiz_data[:-len("```")].strip()
            quiz_data = json.loads(quiz_data)

        quiz_table = []

        # Handle list of MCQs
        if isinstance(quiz_data, list):
            for item in quiz_data:
                mcq = item.get('mcq', '')
                options = " | ".join([
                    f"{opt}: {val}" for opt, val in item.get('options', {}).items()
                ])
                correct = item.get('correct', '')
                quiz_table.append({
                    "MCQ": mcq,
                    "Choices": options,
                    "Correct": correct
                })

        # Handle dict of MCQs
        elif isinstance(quiz_data, dict):
            for key, value in quiz_data.items():
                mcq = value.get('mcq', '')
                options = " | ".join([
                    f"{opt}: {val}" for opt, val in value.get('options', {}).items()
                ])
                correct = value.get('correct', '')
                quiz_table.append({
                    "MCQ": mcq,
                    "Choices": options,
                    "Correct": correct
                })

        else:
            print("Unexpected quiz data format:", type(quiz_data))
            return None

        return quiz_table

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None



