angular.module('app.services').factory('$api', ["$http", ($http) => {

    let baseAddress = 'https://localhost:7053'
    let service = {};

    service.gameHubConnection = () => {

        let connection = new signalR.HubConnectionBuilder()
            .withUrl(`${baseAddress}/game-hub`)
            .build();

        return connection;
    };

    service.lobby = () => {
        return $http.get(`${baseAddress}/api/game/lobby`);
    };

    service.game = (id) => {
        return $http.get(`${baseAddress}/api/game/${id}`);
    };


    return service;
}]);
