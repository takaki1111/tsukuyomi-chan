import streamlit as st
import requests
import os
import openai
from PIL import Image


st.title("Chatbot with streamlit")
st.subheader("メッセージを入力してから送信をタップしてください")
message = st.text_input("メッセージ")




def talk_api(message):
    apikey = "DZZxwzUDGaJiwSEiIqJW1rtEAX8aTWJH"  #@param {type:"string",title:"キー入力"}
    talk_url = "https://api.a3rt.recruit.co.jp/talk/v1/smalltalk"
    payload = {"apikey": apikey, "query": message}
    response = requests.post(talk_url, data=payload)
    try:
        return response.json()["results"][0]["reply"]
    except:
        print(response.json())
        return "ごめんなさい。もう一度教えて下さい。"








chat_logs = []

def send_pya3rt():
    ans = talk_api(message)
    
    chat_logs.append('you: ' + message)
    chat_logs.append('AI: ' + ans)
    for chat_log in chat_logs:
        st.write(chat_log)



image = Image.open('test.png')

if st.button("送信"):
    send_pya3rt()
    st.image(image, caption='サンプル',use_column_width=True)