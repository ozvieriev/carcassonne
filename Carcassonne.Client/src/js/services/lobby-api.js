angular.module("app.services").factory("$lobbyApi", [
    "$http",
    "$q",
    ($http, $q) => {
        let service = {};

        service.createGame = () => {
            return $q.resolve("123");
        };

        return service;
    },
]);
