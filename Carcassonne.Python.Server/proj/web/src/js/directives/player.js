angular.module('app.directives')
    .directive('ngPlayer', ['$filter', ($filter) => {

        return {
            restrict: 'A',
            scope: {
                player: '=ngPlayer'
            },
            link: (scope, element, attrs) => {

                if (!scope.player)
                    return;

                let player = scope.player;
            }
        };
    }]);