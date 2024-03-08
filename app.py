from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
import re
import streamlit as st
from prompts import get_system_prompt
import os
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import pandas as pd
import traceback
from dotenv import load_dotenv


# Downloading the API Key
load_dotenv()

st.set_page_config(page_title="Synthetic Data Generator", page_icon="⚛️")
st.write("## Synthetica - Your assistant for data generation")

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.retry_counter = 0  # Initialize retry counter
    st.session_state.disabled = False
    st.session_state.selected_option = False

def select_option():
    if option is not None:
        st.session_state.selected_option = True
        st.session_state.disabled = True

def run_python_file(filepath):
    with open(filepath, 'r') as file:
        code = file.read()
    exec(code, globals(), globals())

# Sidebar
st.sidebar.title('Synthetica Qualities and Certifications')
llm_a_usar = st.sidebar.selectbox('**Choose your Model:**', ['GPT-4', 'GPT-3.5'], index=0)
industry_knowledge = st.sidebar.text_input('Industry Expertise:', '')
Academic_Background = st.sidebar.text_input('Academic Background:', '')
option = st.sidebar.button('Confirm',
                           on_click=select_option,
                           disabled=st.session_state.disabled)
# End of Sidebar
if llm_a_usar == "GPT-4": 
    llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.2)
elif llm_a_usar == "GPT-3.5":
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2)

if st.session_state.selected_option: 
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content = get_system_prompt()),
                                     HumanMessage(content = f"To get started, please briefly introduce yourself, your Industry Expertise and Academic Background ({industry_knowledge} and {Academic_Background}) and describe your function at a high level. Then provide two simple example questions that the user could ask you to illustrate your capabilities.", additional_kwargs={"first_prompt": True})]

    if prompt := st.chat_input():
        st.session_state.messages.append(HumanMessage(content = prompt))

    for message in st.session_state.messages:
        if message.dict()["type"] == "system":
            continue
        if "first_prompt" in message.dict()["additional_kwargs"]:
            continue
        with st.chat_message(message.dict()["type"]):
            st.write(message.content)
            if "results" in message.dict()["additional_kwargs"]:
                st.dataframe(message.dict()["additional_kwargs"]["results"])

    if st.session_state.messages[-1].dict()["type"] != "ai":
        with st.chat_message("ai"):
            response = ""
            resp_container = st.empty()
            for delta in llm.stream(st.session_state.messages):
                try:
                    response += delta.content
                except:
                    response += ""
                resp_container.markdown(response)

            python_match = re.search(r"```python\n(.*)\n```", response, re.DOTALL)
            if python_match:
                py_code = python_match.group(1)
                filename = "temp/script.py"
                with open(filename, 'w') as file:
                    file.write(py_code)

                try:
                    run_python_file(filename)
                    results = pd.read_csv("data/your_dataset.csv").head(10)
                    st.dataframe(results)
                    message = AIMessage(content = response, additional_kwargs={"results": results})
                    st.write("Your dataset has been generated successfully and can be downloaded below.")
                    with open("data/your_dataset.csv", "rb") as file:
                        st.download_button(label="Download dataset", data=file, file_name="your_dataset.csv")
                    st.session_state.retry_counter = 0  # Reset retry counter if successful
                    st.session_state.messages.append(message)
                
                except Exception as e:
                    #traceback.print_exc()
                    st.session_state.retry_counter += 1  # Increase retry counter
                    if st.session_state.retry_counter >= 3:  # Print error after 3 unsuccessful attempts
                        st.write("There seems to be an issue processing your request. Please retry later.")
                        st.write(e)
                        traceback.print_exc()
                        st.session_state.retry_counter = 0  # Reset retry counter
                        message=AIMessage(content = response)
                        st.session_state.messages.append(message)
                    else:
                        message=AIMessage(content = response)
                        st.session_state.messages.append(message)
                        st.session_state.messages.append(HumanMessage(content=repr(e)))  # Add error as human message
                        st.rerun()
            else:
                message = AIMessage(content = response)
                st.session_state.messages.append(message)
