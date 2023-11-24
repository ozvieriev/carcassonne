angular.module("app.controllers").controller("lobbyCreateGameController", [
  "$q",
  "$state",
  "$scope",
  "$api",
  ($q, $state, $scope, $api) => {
    $scope.createGame = () => {
      let lobby = $api.lobby();

      lobby.then((response) => {
        let json = response.data;

        $state.go("lobby/game", { id: json.id });
      });
    };

    $scope.$on("$destroy", () => {});
  },
]);
