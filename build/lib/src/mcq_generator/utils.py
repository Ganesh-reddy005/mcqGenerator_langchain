import PyPDF2
import json
import os
import traceback

#creating function to read file
def read_file(file):
    if(file.name.endswith('.pdf')):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error loading file ")
        
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise Exception("Unsupported file format ")
    
#to create data frame
def get_table_data(quiz_str):
        try:
            quiz_table=[]
            for keys,value in quiz_str.items():
                mcq=value['mcq']
                options=" | ".join(
                    [
                     f"{option} : {option_value}"
                    for option,option_value in value['options'].items()
                    ]
                )
                correct=value['correct']
                quiz_table.append({"MCQ":mcq,"Choices":options,"Correct":correct})
            return quiz_table
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            return False


