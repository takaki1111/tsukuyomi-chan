import streamlit as st
import requests
import os
import openai
from PIL import Image


API_KEY = "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
"
openai.api_key = API_KEY

st.title("つくよみちゃんとチャットするWebアプリ")
st.subheader("メッセージを入力してから送信をタップしてね！")
message = st.text_input("メッセージ")
image = Image.open('normal.png')
size = (image.width //4, image.height //4)
image = image.resize(size)





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


def text_summary(prompt):
 

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
    return response['choices'][0]['text']

#感情の分類辞書
emo_dict= {"怒り":"mad","喜び":"joy","悲しみ":"sad","驚き":"surprise","普通":"normal"}





chat_logs = []

def send_pya3rt():
    ans = talk_api(message)
    prompt="以下は分類の一覧です。\n1. 怒り\n2. 喜び\n3. 悲しみ\n4. 驚き\n5. 普通\n\nセリフの感情を分類一覧から一つ決定します。\nセリフ：output\n感情:"
    prompt=prompt.replace('output',ans)
    print(prompt)
    emo=text_summary(prompt)
    chat_logs.append('you: ' + message)
    chat_logs.append('つくよみちゃん: ' + ans)
    chat_logs.append('つくよみちゃんの感情: ' + emo)
    for chat_log in chat_logs:
        st.write(chat_log)
    
    #emo_nameは写真の名前
    emo_name=emo_dict[emo.replace(' ', '')]
    
    pic_name= emo_name + '.png'
    print(pic_name)
    image = Image.open(pic_name)
    st.image(image, caption='サンプル',use_column_width=True)




#st.image(image, caption='サンプル',use_column_width=True)
T=st.button("送信")
if T:
    #ボタンを押したときの条件分岐。
    #message(ユーザーのインプット)に天気が含まれるなら、天気情報を返す。
    send_pya3rt()
st.image(image, caption='サンプル',use_column_width=True)
