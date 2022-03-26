const search = document.getElementById('search');
const match = document.getElementById('match');

// function get_player_data(json) {
//     // console.log(json)
//     return
// }
var guess;
class Player {
    constructor(name, pos, age, height, team, number, div, conf) {
        this.name = name;
        this.position = pos;
        this.age = age;
        this.height = height;
        this.team = team;
        this.number = number;
        this.division = div;
        this.conference = conf;
    }
}
function userInput(fName){
    guess = document.getElementById(fName).textContent
    $.getJSON( "players.json")
            .done(function(data) {
                for (var i = 0; i < data.length; i++){
                    if (data[i].name === guess){
                        console.log(data[i].name);
                        console.log(guess)
                    }
                }

            })
    // $('#compare').html(guess)
}

const searchStates = async searchText => {
    const res = await fetch('players.json')
    const players = await res.json()

    let matches = players.filter(player => {
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
            <button class=button id=${match.name} value=${match.height} onClick = userInput(this.id)>${match.name}</button>
            
        `).join('');
        match.innerHTML = html;
    }
}

search.addEventListener('input', () => searchStates(search.value));
fetch("players.json")

    .then(response => response.json())
    .then(json => {
        var ranNum = Math.floor(Math.random() * json.length);
        var player = new Player(json[ranNum].name, json[ranNum].pos, json[ranNum].age, json[ranNum].height, json[ranNum].team, json[ranNum].number, json[ranNum].div, json[ranNum].conf);
        
    }); 


        
// fetch("http://127.0.0.1:8000/")
//     .then(response => response.json())
//     .then(json => console.log(json))



