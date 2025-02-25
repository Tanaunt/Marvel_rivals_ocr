async function fetchData() {
    const timestamp = new Date().getTime(); // Aggiunge un parametro per evitare la cache
    const response = await fetch(`https://Tanaunt.github.io/Marvel_rivals_ocr/usernames.json?t=${timestamp}`);
    const data = await response.json();
    return data;
}

async function updateTable() {
    const data = await fetchData();
    const table = document.getElementById('userTable');
    table.innerHTML = ""; // Pulisce la tabella prima di riempirla

    for (const username of data.usernames) {
        const url = `https://tracker.gg/marvel-rivals/profile/ign/${username}/heroes?mode=competitive&season=2`;
        
        let row = `<tr>
            <td>${username}</td>
            <td><a href="${url}" target="_blank">Apri Profilo</a></td>
        </tr>`;
        table.innerHTML += row;
    }
}

// 🔄 Aggiorna i dati ogni 10 secondi
setInterval(updateTable, 10000);

// Carica i dati all’avvio
updateTable();
