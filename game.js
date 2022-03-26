const search = document.getElementById('search');
const match = document.getElementById('match');


function get_player_data(json) {
    // console.log(json)
    return
}

$(document).ready(function() {

    const searchStates = async searchText => {
        const res = await fetch('players.json')
        const players = await res.json()

        let matches = players.filter(player => {
            const regex = new RegExp(`^${searchText}`, 'gi');
            return player.name.match(regex) 
        });
        if(searchText.length === 0) {
            matches = []
            match
        }
        outputHtml(matches);
    }
    const outputHtml = matches => {
        if(matches.length > 0){
            const html = matches.map(match => `
                <button class=button value="${match.name}">${match.name}</button>
                
            `).join('');
            match.innerHTML = html;
        }
    }
    search.addEventListener('input', () => searchStates(search.value));
    
    fetch("players.json")
    
      .then(response => response.json())
      .then(json => get_player_data(json))

    fetch("http://127.0.0.1:8000/")
        .then(response => response.json())
        .then(json => console.log(json))
});


