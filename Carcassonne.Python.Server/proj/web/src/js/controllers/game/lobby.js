angular.module("app.controllers").controller("lobbyController",
    ["$q", "$state", "$scope", "$api", ($q, $state, $scope, $api) => {

        $scope.createGame = () => {
            $state.go("game", { id: 123 });
        };
    }]);
