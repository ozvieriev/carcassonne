angular.module('app.directives')
    .directive('ngMove', ['$filter', ($filter) => {

        return {
            restrict: 'A',
            scope: {
                move: '=ngMove',
                offset: '=ngOffset'
            },
            link: (scope, element, attrs) => {

                if (!scope.move || !scope.offset)
                    return;

                let offset = scope.offset;

                element.addClass(`tile r-${scope.move.rotation}`);

                element.css({
                    'grid-column': scope.move.location.x + offset.x,
                    'grid-row': scope.move.location.y + offset.y
                });

                element.html(`<img src="img/tiles/${scope.move.tile.img}" title="${scope.move.location.x}:${scope.move.location.y}"/>`);
            }
        };
    }]);