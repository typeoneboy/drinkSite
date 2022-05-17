from os import read
import time
import json
import threading
from drinks import drink_list, drink_options
from menu import MenuItem, Menu, Back
from pathlib import Path

FLOW_RATE = 60.0 / 100.0

class Bartender():
    def __init__(self, running=False):
        self.running = running
        self.pump_configuration = self.readPumpConfiguration()

    @staticmethod
    def readPumpConfiguration():
        path = Path(__file__).parent / "./static/pump_config.json"
        with path.open(mode="r") as f:
            f = json.load(f)
        return f
    
    @staticmethod
    def writePumpConfiguration(configuration):
        path = Path(__file__).parent / "./static/pump_config.json"
        with path.open(mode="w") as jsonFile:
            json.dump(configuration, jsonFile)

    def buildMenu(self, drink_list: list[dict[str, any]], drink_options:list[dict[str, str]]):
        # create a new main menu
        m = Menu('Main Menu')
        # add drink options
        drink_opts = []
        for d in drink_list:
            drink_opts.append(MenuItem('drink', d['name'], {'ingredients': d['ingredients']}))
        configuration_menu = Menu('Configure')
        pump_opts = []
        for p in sorted(self.pump_configuration.keys()):
            config = Menu(self.pump_configuration[p]['name'])
            for opt in drink_options:
                config.addOption(MenuItem('pump_selection', opt['name'], {'key': p, 'value': opt['value'], 'name': opt['name']}))
            config.addOption(Back('Back'))
            config.setParent(configuration_menu)
            pump_opts.append(config)
        configuration_menu.addOptions(pump_opts)
        configuration_menu.addOption(Back('Back'))
        configuration_menu.addOption(MenuItem('clean', 'Clean'))
        configuration_menu.setParent(m)

        m.addOptions(drink_opts)
        m.addOption(configuration_menu)

    def filterDrinks(self, unfilteredMenu:Menu):
        filteredMenu = Menu('filteredMenu')
        for i in unfilteredMenu.options:
            i:MenuItem
            if (i.type == 'drink'):
                i.visible = False
                ingredients = i.attributes['ingredients']
                ingredients: dict[str, int]
                presentIng:int = 0  
                for ing in ingredients.keys():
                    for p in self.pump_configuration.keys():
                        if (ing == self.pump_configuration[p]["value"]):
                            presentIng += 1
                if (presentIng == len(ingredients.keys())):
                    i.visible = True
                    filteredMenu.addOption(i)
            elif (i.type == 'menu'):
                self.filterDrinks(i)
        return filteredMenu
                
    def selectConfigurations(self, menu:Menu):
        for i in menu.options:
            i:MenuItem
            if i.type == 'pump_selection':
                key = i.attributes['key']
                if (self.pump_configuration[key]['value']  == i.attributes['value']):
                    i.name = '%s %s' % (i.attributes['name'], '*')
                else:
                    i.name = i.attributes['name']
            elif i.type == 'menu':
                self.selectConfigurations(i)

    def prepareForRender(self, menu:Menu):
        self.filterDrinks(menu)
        self.selectConfigurations(menu)
        return True

    def menuItemClicked(self, menuItem:MenuItem):
        if menuItem.type == 'drink':
            self.makeDrink(menuItem.name, menuItem.attributes['ingredients'])
            return True
        elif menuItem.type == 'pump_selection':
            self.pump_configuration[menuItem.attributes['key']]['value'] = menuItem.attributes['value']
            Bartender.writePumpConfiguration(self.pump_configuration)
            return True
        elif menuItem.type == 'clean':
            self.clean()
            return True
        return False

    def clean(self):
        waitTime = 20
        pumpThreads = []
        self.running = True
        for pump in self.pump_configuration.keys():
            pump_t = threading.Thread(target=self.pour,
                    args=(self.pump_configuration[pump]['pin'],
                    waitTime))
            pumpThreads.append(pump_t)
        for thread in pumpThreads:
            thread:threading.Thread
            thread.start()
        for thread in pumpThreads:
            thread:threading.Thread
            thread.join()
        time.sleep(2)
        self.running = False

    def pour(self, pin:int, waitTime:int):
        # GPIO.output(pin, GPIO.LOW)
        time.sleep(waitTime)
        # GPIO.output(pin, GPIO.HIGH)

    def makeDrink(self, drink:MenuItem, ingredients: dict[str, int]):
        self.running = True
        print('Making your drink...')
        maxTime = 0
        pumpThreads = []
        sepTimes:list[float] = []
        for ing in ingredients.keys():
            for pump in self.pump_configuration.keys():
                if ing == self.pump_configuration[pump]['value']:
                    waitTime = ingredients[ing] * FLOW_RATE
                    if waitTime > maxTime:
                        maxTime = waitTime
                    pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]['pin'], waitTime))
                    pumpThreads.append(pump_t)
                    sepTimes.append(waitTime)
        totalWaitTime = sum(sepTimes)
        print(f"Making {drink.name}! {totalWaitTime}s left")

        for thread in pumpThreads:
            thread:threading.Thread
            thread.start()
            thread.join()
        self.running = False

    def run(self):
        while self.running is True:
            time.sleep(2)

bartender = Bartender()
bartender.buildMenu(drink_list, drink_options)
bartender.run()