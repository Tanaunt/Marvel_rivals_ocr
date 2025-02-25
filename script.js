async function fetchData() {
    const statusElement = document.getElementById('status'); // Elemento per notifiche di stato
    try {
        const timestamp = new Date().getTime(); // Aggiunge un parametro per evitare la cache
        const response = await fetch(`https://Tanaunt.github.io/Marvel_rivals_ocr/usernames.json?t=${timestamp}`);
        
        if (!response.ok) {
            throw new Error(`Errore ${response.status}: Impossibile caricare il JSON`);
        }

        const data = await response.json();

        // ✅ Se tutto è andato bene, aggiorniamo il messaggio di stato
        statusElement.innerHTML = `✅ JSON caricato con successo - ${new Date().toLocaleTimeString()}`;
        statusElement.style.color = "green";

        return data;
    } catch (error) {
        // ❌ Se c'è un errore, aggiorniamo lo stato con un messaggio di errore
        statusElement.innerHTML = `❌ Errore nel caricamento del JSON: ${error.message}`;
        statusElement.style.color = "red";
        return null;
    }
}

async function updateTable() {
    const data = await fetchData();
    if (!data) return; // Se il JSON non è stato caricato, fermiamo l'esecuzione

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
