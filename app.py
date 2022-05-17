from flask import Flask, render_template, request
from bartender import Bartender
from script import  initBartender, onLoadScript, addDrinkToDrinkList, deleteDrinkFromList
from drinks import drink_list
app = Flask(__name__)


def nestedAction(drinkName:str):
    goodDrinks = initBartender(drink_list)
    for drink in goodDrinks:
        if drink.name == drinkName:
            Bartender().makeDrink(drink, drink.attributes['ingredients'])

@app.route("/wait", methods=['GET', 'POST'])
def wait():
    if request.method == 'GET':
        return render_template('wait.html')
    
    if request.method == 'POST':
        drink:str = request.args['drink']
        nestedAction(drink)
        return 'done'
    
@app.route("/addDrink", methods=['GET', 'POST'])
def addDrink():
    if request.method == 'GET':
        return render_template('newDrink.html')
    if request.method == 'POST':
        numOfIngsStr = request.args['numIngs']
        print(numOfIngsStr)
        numOfIngs = int(numOfIngsStr) + 1
        drinkName = request.form['name']
        print(drinkName)
        ingredients = {}
        for x in range(1, numOfIngs):
            x = str(x)
            ingNameID = f"ingredient{x}"
            ingAmountID = f"amount{x}"
            
            ingName = request.form[ingNameID]
            ingAmount = request.form[ingAmountID]
            ingredients[ingName] = ingAmount
        print(ingredients)
        addDrinkToDrinkList(drinkName, ingredients)
        return 'done'
        
@app.route("/deleteDrink", methods=['POST'])
def deleteDrink():
    print('deleteDrink triggered')
    drinkName = request.args['drink']
    print(drinkName)
    deleteDrinkFromList(drinkName)
    print('Deleted')
    return 'done'
    

@app.route("/")
def index():
    onLoadScript()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000, debug=True)