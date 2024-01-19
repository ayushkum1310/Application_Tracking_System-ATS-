import google.generativeai as gemini
from dotenv import load_dotenv
import streamlit as st
import pdf2image
import os
import io
import base64
load_dotenv()

gemini.configure(api_key=os.environ.get("Api"))


def get_gemini_response(input,pdf_content,prompt):
    model=gemini.GenerativeModel(model_name="gemini-pro-vision")
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text


def input_pdf_setup(upload_file):
    if upload_file is not None:
        images=pdf2image.convert_from_bytes(upload_file.read())
        
        first_page=images[0]
        
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format="JPEG")
        img_byte_arr=img_byte_arr.getvalue()
        pdf_parts=[{
            "mime_type":"image/jpeg",
            "data":base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError(" No File Uploaded ")


st.set_page_config(page_title="Applicatin Tracking System")
st.header("ATS Powered by ")
input_text=st.text_area("Job Description.... ",key='input')
uploaded_file=st.file_uploader('Upload your resume(PDF)....',type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Sucessfully uloaded ")


submit1=st.button("Tell me about the resume")

submit2=st.button("Tell me about the Resume")

submit3=st.button("What is the percentage match")

input_prompt1='''
You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
'''
input_prompt2 = """
You are a seasoned career advisor providing guidance on skill development. The individual is seeking advice on how to enhance their skills 
to better align with the current job market and advance in their career. Please provide detailed recommendations and strategies for 
improving their skills based on their current background and the industry trends. Consider suggesting relevant courses, certifications, 
or practical experiences that can contribute to their professional growth. Additionally, highlight the importance of soft skills and 
any specific areas where they can focus to become a more well-rounded candidate in their field.
"""
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        respnse=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is... ")
        st.write(respnse)
    else:
        st.write("File not uploaded please uplod your file")
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        respnse=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is... ")
        st.write(respnse)
    else:
        st.write("File not uploaded please uplod your file")
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        respnse=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The response is... ")
        st.write(respnse)
    else:
        st.write("File not uploaded please uplod your file")
    
    
    
        
