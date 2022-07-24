import streamlit as st
import requests
import os
import openai
from PIL import Image


API_KEY = "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"
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


#天気情報都道府県
area_dic = {'北海道/釧路':'014100',
            '北海道/旭川':'012000',
            '北海道/札幌':'016000',
            '青森県':'020000',
            '岩手県':'030000',
            '宮城県':'040000',
            '秋田県':'050000',
            '山形県':'060000',
            '福島県':'070000',
            '茨城県':'080000',
            '栃木県':'090000',
            '群馬県':'100000',
            '埼玉県':'110000',
            '千葉県':'120000',
            '東京都':'130000',
            '神奈川県':'140000',
            '新潟県':'150000',
            '富山県':'160000',
            '石川県':'170000',
            '福井県':'180000',
            '山梨県':'190000',
            '長野県':'200000',
            '岐阜県':'210000',
            '静岡県':'220000',
            '愛知県':'230000',
            '三重県':'240000',
            '滋賀県':'250000',
            '京都府':'260000',
            '大阪府':'270000',
            '兵庫県':'280000',
            '奈良県':'290000',
            '和歌山県':'300000',
            '鳥取県':'310000',
            '島根県':'320000',
            '岡山県':'330000',
            '広島県':'340000',
            '山口県':'350000',
            '徳島県':'360000',
            '香川県':'370000',
            '愛媛県':'380000',
            '高知県':'390000',
            '福岡県':'400000',
            '佐賀県':'410000',
            '長崎県':'420000',
            '熊本県':'430000',
            '大分県':'440000',
            '宮崎県':'450000',
            '鹿児島県':'460100',
            '沖縄県/那覇':'471000',
            '沖縄県/石垣':'474000'
            }
jma_url=jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/XXX.json"
def area_name_url(text):
  
  for k , v in area_dic.items():
    #都道府県
    if k[0:-1] in text:
      area_no=area_dic[k]
      area_descript=k +"の天気"
      #print("都道府県")
      break
    elif k[-2:] in text:
      #札幌のようなとき
      area_no=area_dic[k]
      area_descript=k[-2:] +"の天気"
      #print("札幌")
      break

    elif k[:3]=="北海道" and k[:3] in text:
      #北海道
      area_no=area_dic["北海道/札幌"]
      area_descript="北海道の天気"
      #print("北海道")
      break
    elif k[:2]=="沖縄" and k[:2] in text:
      #沖縄
      area_no=area_dic["沖縄県/那覇"]
      area_descript="沖縄の天気"
      #print("沖縄")
      break
  return area_no,area_descript



def weather_output(area_name_no): 
  jma_url_new=jma_url.replace('XXX', area_name_no)
  jma_json = requests.get(jma_url_new).json()
  jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
  #全角スペースを削除
  weather=jma_weather.replace('　', '')
  jma_temp=jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][2]
  temp=jma_json[0]["timeSeries"][2]["areas"][0]["temps"]
  #print(temp)
  max_temp=temp[1]
  min_temp=temp[2]

  retuen_sent=area_name_desc+"は" + jma_weather+"。"+"最高気温は"+max_temp+"、"+"最低気温は"+min_temp+"°です。"

  return retuen_sent


#st.image(image, caption='サンプル',use_column_width=True)
T=st.button("送信")
if T:
    #ボタンを押したときの条件分岐。
    #message(ユーザーのインプット)に天気が含まれるなら、天気情報を返す。

    if "天気" in message:
        print(message)
        try:
            area_name_no=area_name_url(message)[0]
            print(area_name_no)
            area_name_desc=area_name_url(message)[1]
            w=weather_output(area_name_no)
            st.write(w)
        except:
            st.write("エリアがわかりません。以下のようにエリア名も入力してください。\n- 例)東京の天気は？")

    else:
        send_pya3rt()
st.image(image, caption='サンプル',use_column_width=True)


