angular.module("app.controllers").controller("lobbyCreateGameController", [
  "$scope",
  "$lobbyApi",
  ($scope, $lobbyApi) => {
    $scope.createGame = () => {
      $lobbyApi.createGame().then((response) => {
        alert(response)
      });
    };

    $scope.$on("$destroy", () => {});
  },
]);
