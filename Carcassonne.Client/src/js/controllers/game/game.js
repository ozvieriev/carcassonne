angular.module('app.controllers').controller('gameController',
    ['$q', '$state', '$stateParams', '$scope', '$api', ($q, $state, $stateParams, $scope, $api) => {

        $scope.game = null;
        $scope.gameHubConnection = null;
        $scope.gameHubConnectionStart = null;

        $scope.joinGame = () => {

            
        };

        $api.game($stateParams.id).then((response) => {
            $scope.game = response.data;

            let connection = $api.gameHubConnection();

            connection.on('user-joined', (gameId, user, game) => {

                console.log('user-joined', gameId, user)
            });

            connection.start().then(() => {

                connection.invoke("Join", $scope.game.id, 'navigator.userAgent')
            })

        }, (error) => { alert(error.status); });

    }]);
