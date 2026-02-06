// Minimal demo client for the Carcassonne websocket + REST API
let currentGame = null;
let ws = null;
let lastGamePayload = null;

function log(msg) {
    const el = document.getElementById('log');
    const p = document.createElement('div');
    p.textContent = `[${new Date().toLocaleTimeString()}] ${typeof msg === 'string' ? msg : JSON.stringify(msg)}`;
    el.prepend(p);
}

async function createGame() {
    log('Creating game...');
    const resp = await fetch('/game/', { method: 'PUT' });
    if (!resp.ok) {
        log('Create game failed: ' + resp.status);
        return;
    }
    const json = await resp.json();
    currentGame = json;
    lastGamePayload = json;
    document.getElementById('gameId').value = json.id || '';
    renderGameInfo(json);
    log('Game created: ' + json.id);
}

function renderGameInfo(g) {
    document.getElementById('gameInfo').textContent = JSON.stringify(g, null, 2);
}

function connectWs() {
    const id = document.getElementById('gameId').value.trim();
    if (!id) {
        log('Please fill game id first');
        return;
    }
    const scheme = location.protocol === 'https:' ? 'wss' : 'ws';
    const url = `${scheme}://${location.host}/ws/${encodeURIComponent(id)}`;
    ws = new WebSocket(url);
    ws.onopen = () => log('ws open ' + url);
    ws.onclose = () => log('ws closed');
    ws.onerror = (e) => log('ws error');
    ws.onmessage = (ev) => {
        let data = null;
        try { data = JSON.parse(ev.data); } catch (e) { data = ev.data; }
        log(['ws message', data]);
        if (data && data.type === 'tile_placed') {
            lastGamePayload = data.board;
            renderGameInfo(data);
        }
    };
}

async function placeNext() {
    const id = document.getElementById('gameId').value.trim();
    
    const body = { location: {x: 0, y:-1}, rotation: 0 };
    const resp = await fetch(`/game/${id}/placeTile`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createGame').addEventListener('click', createGame);
    document.getElementById('connectWs').addEventListener('click', connectWs);
    document.getElementById('placeNext').addEventListener('click', placeNext);
});
