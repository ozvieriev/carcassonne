angular.module('app.directives')
    .directive('ngBoard', ['$filter', ($filter) => {

        let size = 75;

        return {
            restrict: 'A',
            scope: {
                size: '=ngSize'
            },
            link: (scope, element, attrs) => {

                if (!scope.size)
                    return;

                scope.$watch('size', function (newValue, oldValue) {

                    if (newValue && (newValue.width != oldValue.width || newValue.height != oldValue.height)) {
                        
                        element.css({
                            'grid-template-columns': `repeat(${scope.size.width}, ${size}px)`,
                            'grid-template-rows': `repeat(${scope.size.height}, ${size}px)`,
                        });
                    }
                });
            }
        };
    }]);