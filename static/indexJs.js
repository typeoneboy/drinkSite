function toGoodCase(string) {
    const str2 = string.charAt(0).toUpperCase();
    const str3 = string.slice(1)
    return `${str2}${str3}`;
}

function thingToString(string) {
    const x = `${string}`;
    return x;
}

fetch("{{ url_for('static', filename='drinkList.json') }}")
    .then(response => response.json())
    .then(data => {
        const drinkHtml = data.map(obj => {
            const { name, ingredients } = obj;
            const newName = name.replace(' and ', ' & ');
            const nHtml = `<p class="drinkName">${newName}</p>`;
            const iEntries = Object.entries(ingredients);
            const iHtml = iEntries.map(([name, value]) => {
                const goodName = toGoodCase(name);
                return `<p class="drinkIngs">${goodName} - ${value}mls</p>`;
            }).join('');
            const nameString = thingToString(newName)
            const linkName = name.replace('&', 'and');
            const makeLink = `<a href="/wait?drink=${linkName}" class="makerLink">Make me!</a>`;
            const deleteLink = `<a href="#" class="deleteLink" id="deleteLink" onclick="delDrinkLink(${nameString})">Delete this drink</a>`;

            document.getElementById('deleteLink').addEventListener("click", function(event) {
                event.preventDefault();
                delDrinkLink(newName);
            })

            return `<div class="drink"><p>${nHtml}</p><p>${iHtml}</p>${makeLink}<br>${deleteLink}</div>`;
        }).join('');
        var newDrinkLink = `<a href='/addDrink' class='newDrink'>Add a drink</a>`;
        const html = newDrinkLink + drinkHtml;
        document.querySelector('#main').innerHTML = html;  
    })

function delDrinkLink(drinkName) {
    const request = new XMLHttpRequest();
    request.open('POST', `/deleteDrink?drink=${drinkName}`)
    console.log('POST to ' + `/deleteDrink?drink=${drinkName}`)

    request.onload = function() {
        if (request.status == 200 && request.responseText == 'done') {
            window.location = '/';
        } else {
            alert('Something went wrong');
        }
    };

    request.onerror = function() {
        alert("Oops,  we've had an error.");
    };

    request.send()
}