async function fetchData() {
    const response = await fetch('https://tuo-user-github.github.io/usernames.json');
    const data = await response.json();
    return data;
}

function extractStatsFromPage(username, url) {
    return new Promise((resolve) => {
        const iframe = document.createElement('iframe');
        iframe.style.display = "none";
        iframe.src = url;
        document.body.appendChild(iframe);

        iframe.onload = () => {
            try {
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                let heroStats = doc.querySelector(".hero-stats-class"); // Sostituire con il vero selettore CSS
                resolve(heroStats ? heroStats.innerText : "Nessun dato trovato");
            } catch (error) {
                resolve("Errore nell'accesso ai dati");
            }
            document.body.removeChild(iframe);
        };
    });
}

async function updateTable() {
    const data = await fetchData();
    const table = document.getElementById('userTable');

    for (const username of data.usernames) {
        const url = `https://tracker.gg/marvel-rivals/profile/ign/${username}/heroes?mode=competitive&season=2`;
        const stats = await extractStatsFromPage(username, url);

        let row = `<tr>
            <td>${username}</td>
            <td>${stats}</td>
        </tr>`;
        table.innerHTML += row;
    }
}

updateTable();
