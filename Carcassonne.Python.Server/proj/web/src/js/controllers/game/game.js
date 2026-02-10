angular.module('app.controllers').controller('gameController',
    ['$q', '$state', '$stateParams', '$scope', '$api', '$location', ($q, $state, $stateParams, $scope, $api, $location) => {

        let ws = null;

        const playerId = $location.search().playerId;

        $scope.board = {
            size: { width: 0, height: 0 },
            offset: { x: 0, y: 0 },
            nextTile: null,
            nextPlayerId: null,
            currentPlayerId: playerId,
            moves: [],
            availablePositions: [],
            players: []
        };

        let safeApply = (fn) => {

            $scope.$$phase ? fn() : $scope.$apply(fn);
        }

        let apply = (response) => {

            if (response.moves) {
                calculateOffset(response.moves, response.availablePositions);

                $scope.board.moves = response.moves;
                $scope.board.availablePositions = response.availablePositions || [];
            }

            $scope.board.nextTile = response.nextTile;
            $scope.board.nextPlayerId = response.nextPlayerId;
            $scope.board.players = response.players || [];

            if($scope.board.currentPlayerId != $scope.board.nextPlayerId)
                $scope.board.availablePositions = [];
        }

        let calculateOffset = (moves, availablePositions) => {

            if (!moves.length)
                return;

            availablePositions = availablePositions || [];

            const minX = Math.min(...moves.map(move => move.location.x));
            const maxX = Math.max(...moves.map(move => move.location.x));

            const minY = Math.min(...moves.map(move => move.location.y));
            const maxY = Math.max(...moves.map(move => move.location.y));

            const x = Math.abs(minX) + Math.abs(maxX) + 1;
            const y = Math.abs(minY) + Math.abs(maxY) + 1;
            const borders = 2

            $scope.board.size = {
                width: x + borders,
                height: y + borders
            };

            $scope.board.offset = { x: Math.abs(minX) + borders, y: Math.abs(minY) + borders };
        }

        $scope.onOpen = () => {
            console.log('ws open');
        };

        $scope.onMessage = (ev) => {
            let response = JSON.parse(ev.data);
            let type = response.type;

            safeApply(function () {
                switch (type) {
                    case 'connect': break;
                    case 'placeTile': apply(response); break;
                    default: console.log('unknown message type', type);
                }
            });

        };

        $scope.onClose = () => {
            console.log('ws closed');
        };

        $scope.onError = () => {
            console.log('ws error', error);
        };

        $api.game($stateParams.id)
            .then((response) => {
                apply(response.data);

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
