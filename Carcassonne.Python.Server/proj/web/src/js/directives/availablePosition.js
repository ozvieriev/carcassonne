angular.module('app.directives')
    .directive('ngAvailablePosition', ['$filter', ($filter) => {

        return {
            restrict: 'A',
            scope: {
                availablePosition: '=ngAvailablePosition',
                offset: '=ngOffset'
            },
            link: (scope, element, attrs) => {

                if (!scope.availablePosition || !scope.offset)
                    return;

                let offset = scope.offset;

                element.addClass(`tile`);

                element.css({
                    'grid-column': scope.availablePosition.x + offset.x,
                    'grid-row': scope.availablePosition.y + offset.y
                });
            }
        };
    }]);