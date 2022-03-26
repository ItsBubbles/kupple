const search = document.getElementById('search');
const match = document.getElementById('match');

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
});


