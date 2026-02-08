angular.module('app.services').factory('$api', ["$http", ($http) => {

    let baseAddress = 'https://localhost:7053'
    let service = {};

    service.gameHubConnection = () => {

        let connection = new signalR.HubConnectionBuilder()
            .withUrl(`${baseAddress}/game-hub`)
            .build();

        return connection;
    };

    service.connect = (id) => {
        const scheme = location.protocol === 'https:' ? 'wss' : 'ws';
        const url = `${scheme}://${location.host}/ws/${id}`;
        
        let ws = new WebSocket(url);
        

        return ws;
    };

    service.game = (id) => {
        return $http.get(`/game/${id}`);
    };

    //     let ws = null;

    // const addLog = (message) => {
    //     let $log = $('#log');

    //     $log.prepend(message + "<br>");
    // }

    // $(document).on('submit', '[name="connectForm"]', (event) => {
    //     event.preventDefault();

    //     const id = $('[name="gameId"]').val().trim();

    //     if (!id)
    //         return addLog('Please fill game id first');

    //     const scheme = location.protocol === 'https:' ? 'wss' : 'ws';
    //     const url = `${scheme}://${location.host}/ws/${encodeURIComponent(id)}`;

    //     ws && ws.close();

    //     ws = new WebSocket(url);
    //     ws.onopen = () => addLog('ws open ' + url);
    //     ws.onclose = () => addLog('ws closed');
    //     ws.onerror = (error) => addLog('ws error');
    //     ws.onmessage = (ev) => {

    //         addLog(['ws ' + ev.data]);
    //     };
    // });


    // const params = new URLSearchParams(window.location.search);
    // const gameId = params.get("gameId");

    // $('[name="gameId"]').val(gameId);

    // if (gameId)
    //     $('[name="connectForm"]').submit();


    return service;
}]);
