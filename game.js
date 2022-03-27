const search = document.getElementById('search');
const match = document.getElementById('match');

var guess;
var data = [];

function userInput(playerId){
    console.log(playerId)
}

const searchStates = async searchText => {
    let matches = data[0].filter(player => {
        const regex = new RegExp(`^${searchText}`, 'gi');
        return player.name.match(regex) 
    });
    if(searchText.length === 0) {
        matches = []
    }
    outputHtml(matches);
}

const outputHtml = matches => {
    if(matches.length > 0){

        const html = matches.map(match => `
            <button class=button id=${data[0].indexOf(match)} onClick=userInput(this.id)>${match.name}</button>
            
        `).join('');
        match.innerHTML = html;
    }
}

search.addEventListener('input', () => searchStates(search.value));

// takes in api call
function get_player_data(json) {
    data.push(json)
    return
}

// sample call, need to POST index of player from JSON
// fetch("http://127.0.0.1:8000/answer")
//     .then(response => response.json())
//     .then(json => json)

fetch("http://127.0.0.1:8000/")
    .then(response => response.json())
    .then(json => get_player_data(json))
