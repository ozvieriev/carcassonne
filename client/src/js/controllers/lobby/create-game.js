angular.module("app.controllers").controller("lobbyCreateGameController", [
  "$q",
  "$state",
  "$scope",
  "$lobbyApi",
  ($q, $state, $scope, $lobbyApi) => {
    $scope.createGame = () => {
      $lobbyApi.createGame().then((response) => {
        $state.go("lobby/game", { id: 123 });
      });
    };

    $scope.$on("$destroy", () => {});
  },
]);
