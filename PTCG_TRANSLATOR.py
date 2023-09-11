import pandas as pd
import os
from google.cloud import translate_v2 as translate

#PROJECT_ID = "applied-flag-381002"
PTCG_API_KEY = "c914e24f-8c5f-4141-a635-9cccd687ad3c"
#TRANSLATION_API_KEY = "AIzaSyC69zStzA6p2vmUXk12NH430BGABGFz25s"
#GLOSSARY_ID = "storage_for_translator"
WORD_FILENAME = "WordDictionary.csv"
CARD_FILENAME = "CardDictionary.csv"

def sort_EN_By_Length(df, column_name):
    def key_function(row):
        sentence = row[column_name]
        words_count = len(sentence.split())  # 단어 개수 계산
        return (words_count, len(sentence))  # (단어 개수, 문장 길이)를 반환하여 정렬 순서 결정
    sorted_df = df.sort_values(by=[column_name], key=key_function)
    return sorted_df

def open_CSV_as_DF():
    return pd.read_csv(WORD_FILENAME)

def addWord_EN_KO(df, en, ko):
    df.loc[len(df)] = [en, ko]

def deleteWord_EN_KO(df, en):
    df = df[df.apply(lambda row: en not in row.values, axis=1)]

def DF_to_CSV(df):
    df.to_csv(WORD_FILENAME, index=False)
    print("saved as", WORD_FILENAME)

def apply_Word_Dict(text):
    df = open_CSV_as_DF()
    for en, ko in df.values:
        text = text.replace(en, ko)
    return text

def translate_text(text, target_language='ko'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\imt02\\성재승\\API\\applied-flag-381002-1955f93102e9.json"
    original_text = text
    text = apply_Word_Dict(text)
    client = translate.Client()
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']
