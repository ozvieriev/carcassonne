angular.module("app.services").factory("$api", [
  "$http",
  function factory($http) {
    var service = {};

    service.lobby = () => {
      return $http.get("https://localhost:7053/api/game/lobby");
    };

    return service;
  },
]);
