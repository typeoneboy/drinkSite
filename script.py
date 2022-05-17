from asyncore import write
import json
import os
from typing import Any
from bartender import Bartender
from menu import Menu, MenuItem
from drinks import drink_list, drink_options
from pathlib import Path

def drinkListToJSON(drink_list:list[dict[str, Any]]):
    drinkListPath = Path(__file__).parent / './static/drinkList.json'
    if(os.path.isfile(drinkListPath)):
        os.remove(drinkListPath)
    
    with open(drinkListPath, "w") as outfile:
        json.dump(drink_list, outfile, indent=4)

def drinkOptionsToJSON(drink_options:list[dict[str, str]]):
    drinkOptionPath = Path(__file__).parent / './static/drinkOptions.json'
    if(os.path.isfile(drinkOptionPath)):
        os.remove(drinkOptionPath)
        
    with open(drinkOptionPath, "w") as outfile:
        json.dump(drink_options, outfile, indent=4)

goodDrinks:list[MenuItem] = []

def initBartender(drink_list:list[dict[str, Any]]):
    bartender = Bartender()

    unfilteredMenu:Menu = Menu('goodMenu')
    for drink in drink_list:
        rawDrinkName:str = drink['name']
        drinkName = rawDrinkName.replace('&', 'and')
        unfilteredMenu.addOption(MenuItem('drink', drinkName, {'ingredients': drink['ingredients']}))
            
    filteredMenu:Menu = bartender.filterDrinks(unfilteredMenu)
    for item in filteredMenu.options:
        item:MenuItem
        if item.visible == True:
            goodDrinks.append(item)
    return goodDrinks

def onLoadScript():
    goodDrinks = initBartender(drink_list)
    goodDrinkNames:list[str] = []
    for d in goodDrinks:
        goodDrinkNames.append(d.name)
    found_list:list[dict[str, Any]] = []
    
    for drink in drink_list:
        drinkName:str = drink["name"]
        newDrinkName = drinkName.replace('&', 'and')
        drink["name"] = newDrinkName
        
        if drink["name"] in goodDrinkNames:
            found_list.append(drink)
    
    drinkListToJSON(found_list)
    drinkOptionsToJSON(drink_options)

def write_json(data, filepath):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def addDrinkToDrinkList(name:str, ingredients={}):
    drink = {"name": name, "ingredients": ingredients}
    drink_list.append(drink)
    drinkListToJSON(drink_list)

def deleteDrinkFromList(name:str):
    name = name.lower()
    print("funcName" + name)
    
    for d in range(len(drink_list)):
        drinkName = drink_list[d]['name']
        drinkName:str
        drinkName = drinkName.lower()
        
        if drinkName == name:
            del drink_list[d]
            print('func deleted')
            break
        else:
            continue
    
    drinkListToJSON(drink_list)