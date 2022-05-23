const search = document.getElementById('search');
const match = document.getElementById('match');

// $.getJSON("https://api.myip.com", async function(data, _callback) {
// // Display the visitor's IP in the console
//     var myHeaders = new Headers();
//     myHeaders.append("Content-Type", "application/json");

//     var requestOptions = {
//         method: 'POST',
//         headers: myHeaders,
//         redirect: 'follow',
//         credentials:'include'
//         };
//     await fetch("http://127.0.0.1:8000/create_session/" + data.ip, requestOptions)
//         .then(response => response.json())
// });
const userAction = async () => {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        redirect: 'follow',
        credentials:'include'
        };
    if (localStorage.getItem('key')==null){
        localStorage.setItem('key', Math.random().toString(36).substr(2))
    }
    await fetch('http://127.0.0.1:8000/create_session/' + localStorage.getItem('key'), requestOptions)
        .then(response => response.json())
        .then(console.log)
  }
userAction()
var app = Vue.createApp({
    data(){
        return {
            players: [],
        }
    },
    methods: {
    addNewPlay(player, playerResults){
        let playerClass = []
        if(playerResults == 1)
            {
                playerClass.push(player)
                playerClass.push("has-background-success has-text-primary-light has-text-weight-bold")
                playerClass.push("has-background-success has-text-primary-light has-text-weight-bold")
                playerClass.push("has-background-success has-text-primary-light has-text-weight-bold")
                playerClass.push("")
                playerClass.push("has-background-success has-text-primary-light has-text-weight-bold")
                playerClass.push("")
                playerClass.push("has-background-success has-text-primary-light has-text-weight-bold")
                playerClass.push("")
                playerClass.push("has-background-success has-text-primary-light has-text-weight-bold")
                this.players.push(playerClass)
            }
        else{
            
            playerClass.push(player)
            playerClass.push(playerResults.posClass)
            playerClass.push(playerResults.divClass)
            
            // playerClass.push(player)
            // playerClass.push(playerResults)

            let ageArrowString = playerResults.ageClass[0]
            let ageArrowIndex = ageArrowString.lastIndexOf(" ")
            let ageArrow = ageArrowString.split(" ").pop()
            let ageArrowSubClass = ageArrowString.substring(0, ageArrowIndex)


            let heightArrowString = playerResults.heightClass[0]
            let heightArrowIndex = heightArrowString.lastIndexOf(" ")
            let heightArrow = heightArrowString.split(" ").pop()
            let heightArrowSubClass = heightArrowString.substring(0, heightArrowIndex)

            let numberArrowString = playerResults.numberClass[0]
            let numberArrowIndex = numberArrowString.lastIndexOf(" ")
            let numberArrow = numberArrowString.split(" ").pop()
            let numberArrowSubClass = numberArrowString.substring(0, numberArrowIndex)
            
            
            playerClass.push(ageArrowSubClass)
            if (ageArrow == "triangle_up" || ageArrow == "triangle_down"){
                playerClass.push(ageArrow)
            }
            else{
                playerClass.push("")
            }

            playerClass.push(heightArrowSubClass)
            if(heightArrow == "triangle_up" || heightArrow == "triangle_down"){
                playerClass.push(heightArrow)
            }
            else{
                playerClass.push("")
            }
            playerClass.push(numberArrowSubClass)
            if(numberArrow == "triangle_up" || numberArrow == "triangle_down"){
                playerClass.push(numberArrow)
            }
            else{
                playerClass.push("")
            }
            playerClass.push(playerResults.teamClass)
            // console.log(playerResults.ageClass[0])
            this.players.push(playerClass)
            
        }
    }
    }
}).mount('.tableDiv')

var data = [];
var guess;

async function userInput(playerId){ 
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: JSON.stringify(data[0][playerId]),
        redirect: 'follow',
        credentials:'include'
    };

    
    await fetch("http://127.0.0.1:8000/compare", requestOptions)
    .then(response => response.text())         
    .then(data =>{
        newData = JSON.parse(data)
        app.addNewPlay(newData.player, newData.results)
    })         
}

const searchStates = async searchText => {
    let matches = data[0].filter(player => {
        //regex for string is contained in a string 
        const regex = new RegExp(`${searchText}`, 'gi');
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
fetch("http://127.0.0.1:8000/")
    .then(response => response.json())
    .then(json => get_player_data(json))

