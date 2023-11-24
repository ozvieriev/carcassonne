angular.module("app.controllers").controller("lobbyController",
    ["$q", "$state", "$scope", "$api", ($q, $state, $scope, $api) => {

        $scope.createGame = () => {
            $api.lobby().then((response) => {
                $state.go("game", { id: response.data.id });
            });
        };
    }]);
