angular.module('app.controllers').controller('gameController',
    ['$q', '$state', '$stateParams', '$scope', '$api', ($q, $state, $stateParams, $scope, $api) => {

        let ws = null;

        $scope.game = null;
        $scope.gameHubConnection = null;
        $scope.gameHubConnectionStart = null;

        $scope.joinGame = () => {


        };

        $scope.onOpen = () => {
            console.log('ws open');
        };
        $scope.onMessage = (ev) => {

            let response = JSON.parse(ev.data);
            let type = response.type;

            switch (type) {
                case 'placeTile':
                    $scope.$apply(() => {
                        $scope.game = response.game;
                    });
                    break;
                default:
                    console.log('unknown message type', type);
            }

        };
        $scope.onClose = () => {
            console.log('ws closed');
        };
        $scope.onError = () => {
            console.log('ws error', error);
        };

        $api.game($stateParams.id)
            .then((response) => {
                $scope.game = response.data;

                ws = $api.connect($stateParams.id);
                ws.onopen = $scope.onOpen;
                ws.onmessage = $scope.onMessage;
                ws.onclose = $scope.onClose;
                ws.onerror = $scope.onError;

            }, (error) => { alert(error.status); });

        $scope.$on('$destroy', () => {

            ws && ws.close();
        })

    }]);
