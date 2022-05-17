from drinks import drink_list
from script import initBartender

goodDrinks = initBartender(drink_list)
for drink in goodDrinks:
    print(drink.name)