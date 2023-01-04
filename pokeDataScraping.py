import requests
from bs4 import BeautifulSoup
import time
import json
import re


#アクセント文字の変換
def accent(text):
    text_a = re.sub(r'à|â', "a", text)
    text_i = re.sub(r'ï|î', "i", text_a)
    text_u = re.sub(r'û|ù', "u", text_i)
    text_e = re.sub(r'è|é|ê|ë', "e", text_u)
    text_o = re.sub(r'Ô', "o", text_e)
    text_A = re.sub(r'À|Â', "A", text_o)
    text_I = re.sub(r'Ï|Î', "I", text_A)
    text_U = re.sub(r'Û|Ù', "U", text_I)
    text_E = re.sub(r'È|É|Ê|Ë', "E", text_U)
    text_O = re.sub(r'Ô', "O", text_E)
    text_Re = re.sub(r' ', "-", text_O)
    return text_Re

#リストをまとめて翻訳
def listTranslation(jaTextName,enTextName,dataList):
    jaText = open(jaTextName, 'r', encoding='UTF-8')
    eText = open(enTextName, 'r', encoding='UTF-8')
    eData = eText.readlines()
    jaData = jaText .readlines()
    jaData = list(map(lambda l: l.rstrip("\n"), jaData))
    eData = list(map(lambda l: l.rstrip("\n"), eData))

    for z in range(len(dataList )):
       data = dataList[z]
       if( data in eData):
        idx = eData.index(data)
        dataList[z] = jaData[idx]
    jaText.close()
    eText.close()
    return dataList

#翻訳
def translation(jaTextName,enTextName,data):
    jaText = open(jaTextName, 'r', encoding='UTF-8')
    eText = open(enTextName, 'r', encoding='UTF-8')
    eData = eText.readlines()
    jaData = jaText .readlines()
    
    jaData = list(map(lambda l: l.rstrip("\n"), jaData))
    eData = list(map(lambda l: l.rstrip("\n"), eData))
    
    if( data in eData):
        idx = eData.index(data)
        data = jaData[idx]
    jaText.close()
    eText.close()
    return data


# ポケモンの名前を取得
pokeNameURL = 'https://pokemondb.net/pokedex/game/scarlet-violet'
pokeNameSoup = BeautifulSoup(requests.get(pokeNameURL).content, 'lxml')
pokeNameList = []
for nameData in pokeNameSoup.find_all(class_ = 'ent-name'):
    pokeName = accent(nameData.text)
    pokeNameList.append(pokeName)


#ポケモンのデータを取得
#必要なデータだけ取得する
#基本データ、種族値、技一覧
pokeDataURL = 'https://pokemondb.net/pokedex/'
sleep_time = 1
pokeJsonList = []

for i in range(len(pokeNameList)):

    print(i)
    pokeDataUrlRequest = pokeDataURL  + pokeNameList[i]
    time.sleep(1)
    pokeDataSoup = BeautifulSoup(requests.get(pokeDataUrlRequest).content, 'lxml')
    pokeVitalsList = []
    pokeData = pokeDataSoup.find_all(class_ = 'vitals-table')
    # 基本データを取得
    pokeVitalsData = pokeData[0]
    pokeVitalsList = []
    tokuseiList = []
    for pokeVitalsTableContent in pokeVitalsData.find_all('td'):
        aContent = pokeVitalsTableContent.find_all(class_ = 'text-muted')
        flag = False
        if(aContent):          
            for aData in aContent:
                aText = aData.find('a')
                if(aText):
                    tokuseiList.append( aText.text)
                    flag = True
                else:
                    flag = False   
            if flag:
                pokeVitalsList.append(tokuseiList)
            else:
              pokeVitalsList.append(pokeVitalsTableContent.text.strip())  
        else:
            pokeVitalsList.append(pokeVitalsTableContent.text.strip())

    # 種族値を取得
    pokeBaseStats = pokeData[3]
    pokeBaseStatsList = []


    for pokeBaseStatsTableContent in pokeBaseStats.find_all('tr'):
        pokeBaseStatsContent = pokeBaseStatsTableContent.find('td')
        pokeBaseStatsList.append(pokeBaseStatsContent.text)
    #  技を取得
    #　スクレイピングで使用するカウンター
    # 技の種類がいくつあるか調べる
    wazaSyubetuList = []
    wazaDataSoup = pokeDataSoup.find_all(class_ = 'grid-col span-lg-6')
    for j in range(len(wazaDataSoup )):
        title = wazaDataSoup[j].find_all('h3')
        for wazaSyubetu in title:
            wazaSyubetuList.append(wazaSyubetu.text)
    wazaSyubetuListCount = 0
    wazaDataSoup = pokeDataSoup.find_all(class_ = 'data-table')
    levelWazaList = []
    evolutionWazaList = []
    reminderWazaList = []
    eggWazaList = []
    wazamachinList = []

    # レベル技
    if(wazaSyubetuList[wazaSyubetuListCount]=='Moves learnt by level up'):
        for wazaData in wazaDataSoup[wazaSyubetuListCount].find_all('tr'):
            wazalebel = wazaData.find(class_ ='cell-num')
            wazaname = wazaData.find(class_ = 'cell-name')
            if wazalebel:
                levelWazaList.append(wazaname.text)
        wazaSyubetuListCount = wazaSyubetuListCount +1; 
    if(wazaSyubetuList[wazaSyubetuListCount]=='Moves learnt on evolution'):
        for wazaData in wazaDataSoup[wazaSyubetuListCount].find_all('tr'):
            wazaname = wazaData.find(class_ = 'cell-name')
            if wazaname:
                evolutionWazaList.append(wazaname.text)
        wazaSyubetuListCount = wazaSyubetuListCount +1; 

    if(wazaSyubetuList[wazaSyubetuListCount]=='Moves learnt by reminder'):
        for wazaData in wazaDataSoup[wazaSyubetuListCount].find_all('tr'):
            wazaname = wazaData.find(class_ = 'cell-name')
            if wazaname:
                reminderWazaList.append(wazaname.text)
        wazaSyubetuListCount = wazaSyubetuListCount +1; 

    # たまご技
    if(wazaSyubetuList[wazaSyubetuListCount]=='Egg moves'):
        for wazaData in wazaDataSoup[wazaSyubetuListCount].find_all('tr'):
            wazaname = wazaData.find(class_ = 'cell-name')
            if wazaname:
                eggWazaList.append(wazaname.text)
        wazaSyubetuListCount =wazaSyubetuListCount  +1; 

    # 技マシン
    if(wazaSyubetuList[wazaSyubetuListCount]=='Moves learnt by TM'):
        for wazaData in wazaDataSoup[wazaSyubetuListCount].find_all('tr'):
            wazaname = wazaData.find(class_ = 'cell-name')
            if wazaname:
                wazamachinList.append(wazaname.text)
        wazaSyubetuListCount = wazaSyubetuListCount  +1;  

    sleep_time = 1

    # ポケモン名前
    #翻訳処理
    pokename = translation("trans/pokeName_ja.txt","trans/pokeName_en.txt",pokeNameList[i])
    
    # 全国図鑑No
    nationalNo = pokeVitalsList[0]

    #タイプ
    #2タイプあるか判定する
     
    typeData =   pokeVitalsList[1]
    type01 = ""
    type02 = "" 
    if(' 'in typeData ):
        typeList = typeData.split(' ')
         #翻訳処理
        type01 = translation("trans/types_ja.txt","trans/types_en.txt",typeList[0])
        type02 = translation("trans/types_ja.txt","trans/types_en.txt",typeList[1])
    else:
        type01 = translation("trans/types_ja.txt","trans/types_en.txt",typeData)
        type02 = "なし"

    height = pokeVitalsList[3]
    weight = pokeVitalsList[4]

    #特性
    #翻訳処理
    tokuseiList = listTranslation("trans/abilities_ja.txt","trans/abilities_en.txt",tokuseiList)
    localNo = pokeVitalsList[6].split(' ')[0]

    #種族値
    hp = pokeBaseStatsList[0]
    attack = pokeBaseStatsList[1]
    defense = pokeBaseStatsList[2]
    spAttack = pokeBaseStatsList[3]
    spDefense = pokeBaseStatsList[4]
    speed = pokeBaseStatsList[5]
    total = pokeBaseStatsList[6]

    #技
    #翻訳処理
    levelWazaList = listTranslation("trans/waza_ja.txt","trans/waza_en.txt",levelWazaList)
    evolutionWazaList = listTranslation("trans/waza_ja.txt","trans/waza_en.txt",evolutionWazaList)
    reminderWazaList = listTranslation("trans/waza_ja.txt","trans/waza_en.txt",reminderWazaList)
    eggWazaList = listTranslation("trans/waza_ja.txt","trans/waza_en.txt",eggWazaList)
    wazamachinList = listTranslation("trans/waza_ja.txt","trans/waza_en.txt",wazamachinList)

    #json設定
    pokeJsonData = {
        "pokeName": pokename,
        "nationalNo": nationalNo,
        "type01":type01,
        "type02": type02,
        "height":height,
        "weight":weight,
        "abilities":[
            tokuseiList
        ],
        "localNo":localNo,
        "hp":hp,
        "attack":attack,
        "defense":defense,
        "spAttack":spAttack,
        "spDefence":spDefense,
        "speed":speed,
        "total":total,
        "levelWazaList":[
            levelWazaList
        ],
        "evolutionWazaList":[
            evolutionWazaList
        ],
        "reminderWazaList":[
            reminderWazaList
        ],
        "eggWazaList":[
            eggWazaList
        ],
        "wazamachinList":[
            wazamachinList
        ]
    }
    pokeJsonList.append(pokeJsonData)

#Jsonに設定し出力
pokeJson = {
    "pokeData":[
        pokeJsonList
    ]
}

with open('pokeData.json', 'w',encoding='UTF-8') as f:
     json.dump(pokeJson, f, ensure_ascii=False, indent=4)





