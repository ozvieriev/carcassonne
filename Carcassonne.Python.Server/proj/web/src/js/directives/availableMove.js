angular.module('app.directives')
    .directive('ngAvailableMove', ['$filter', ($filter) => {

        return {
            restrict: 'A',
            scope: {
                availableMove: '=ngAvailableMove',
                offset: '=ngOffset'
            },
            link: (scope, element, attrs) => {

                if (!scope.availableMove || !scope.offset)
                    return;

                let offset = scope.offset;

                element.addClass(`tile`);

                element.css({
                    'grid-column': scope.availableMove.location.x + offset.x,
                    'grid-row': scope.availableMove.location.y + offset.y
                });
            }
        };
    }]);