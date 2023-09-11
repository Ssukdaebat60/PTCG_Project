from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pokemontcgsdk import RestClient
import json
import requests
import pandas as pd
from PTCG_TRANSLATOR import *

def get_Standard_Card(): # in Block 카드의 객체들을 Supertype으로 분류하고 리스트로 반환
    RestClient.configure("c914e24f-8c5f-4141-a635-9cccd687ad3c")
    return {"energy":Card.where(q="legalities.standard:legal supertype:Energy"),
            "pokemon":Card.where(q="legalities.standard:legal supertype:Pokémon"),
            "trainer":Card.where(q="legalities.standard:legal supertype:Trainer")}

def get_JSON_from_Card(ptcg_card): # 카드를 json파일로 변환하고 데이터를 편집하여 반환
    if ptcg_card.supertype == "Pokémon":
        return get_JSON_from_Pokemon(ptcg_card)
    elif ptcg_card.supertype == "Trainer":
        return get_JSON_from_Trainer(ptcg_card)
    else : #Energy
        return get_JSON_from_Energy(ptcg_card)

def get_JSON_from_Pokemon(ptcg_card):
    return {
        "pokemon": {
            "id": ptcg_card.id,
            "name": ptcg_card.name,
            "eng_name": ptcg_card.name,
            "set": {
                "id": ptcg_card.set.id,
                "name": ptcg_card.set.name
            },
            "supertype": ptcg_card.supertype,
            "subtypes": ptcg_card.subtypes,
            "images": ptcg_card.images.small,
            "types": ptcg_card.types,
            "rarity": ptcg_card.rarity,
            "rule": ptcg_card.rules,
            "regulationMark": ptcg_card.regulationMark,
            "resistances": None if ptcg_card.resistances == None else ptcg_card.resistances[0].type + ptcg_card.resistances[0].value,
            "artist": ptcg_card.artist,
            "hp": ptcg_card.hp,
            "evolvesFrom": ptcg_card.evolvesFrom,
            "ability": {
                "name": None if ptcg_card.abilities == None else ptcg_card.abilities[0].name,
                "text": None if ptcg_card.abilities == None else ptcg_card.abilities[0].text
            },
            "attacks": [
                        {
                        "name":atk.name, 
                        "cost": atk.cost,
                        "convertedEnergyCost" : atk.convertedEnergyCost,
                        "damage" : atk.damage,
                        "text" : atk.text
                        }
                        for atk in ptcg_card.attacks],
            "convertedAttacksNum" : len(ptcg_card.attacks),
            "weaknesses": None if ptcg_card.weaknesses == None else ptcg_card.weaknesses[0].type + ptcg_card.weaknesses[0].value,
            "retreatCost": ptcg_card.retreatCost,
            "convertedRetreatCost": ptcg_card.convertedRetreatCost
        }
    }

def get_JSON_from_Trainer(ptcg_card):
    return {
        "trainer": {
            "id": ptcg_card.id,
            "name": ptcg_card.name,
            "eng_name": ptcg_card.name,
            "set": {
                "id": ptcg_card.set.id,
                "name": ptcg_card.set.name
            },
            "supertype": ptcg_card.supertype,
            "subtypes": ptcg_card.subtypes,
            "images": ptcg_card.images.small,
            "rarity": ptcg_card.rarity,
            "rule": ptcg_card.rules,
            "regulationMark": ptcg_card.regulationMark,
            "artist": ptcg_card.artist
        }
    }


def get_JSON_from_Energy(ptcg_card):
    return {
        "energy": {
            "id": ptcg_card.id,
            "name": ptcg_card.name,
            "eng_name": ptcg_card.name,
            "set": {
                "id": ptcg_card.set.id,
                "name": ptcg_card.set.name
            },
            "supertype": ptcg_card.supertype,
            "subtypes": ptcg_card.subtypes,
            "images": ptcg_card.images.small,
            "types": ptcg_card.types,
            "rarity": ptcg_card.rarity,
            "rule": ptcg_card.rules,
            "regulationMark": ptcg_card.regulationMark,
            "artist": ptcg_card.artist
        }
    }

def translate_value(value):
    if isinstance(value, str):
        return translate_text(value)
    elif isinstance(value, dict):
        return get_kr_from_en_json(value)  # 중첩된 딕셔너리 번역
    elif isinstance(value, list):
        return [translate_value(x) for x in value]
    else:
        return value

def get_kr_from_en_json(ptcg_card_dict):
    kr_dict = {}
    for key, value in ptcg_card_dict.items():
        k = translate_text(key)
        v = translate_value(value)
        kr_dict[k]=v
    return kr_dict

def search_by_card_name(name):
    RestClient.configure("c914e24f-8c5f-4141-a635-9cccd687ad3c")
    return Card.where(q=f"name:*{name}* legalities.standard:legal")

def json_to_str(json_data):
    transfered_str = ""
    for k, v in json_data.items():
        transfered_str = transfered_str + str(k) + "\n\t"
        if isinstance(v, dict):
            transfered_str = transfered_str + json_to_str(v)
        else:
            transfered_str = transfered_str + str(v) +"\n\n"
    return transfered_str




