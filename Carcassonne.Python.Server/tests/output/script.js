(function ($) {


    
    $(function () {
        var $board = $('.board');
            var isDown = false;

            var startX = 0, startY = 0, scrollLeft = 0, scrollTop = 0;

            $board.on('mousedown touchstart', function (e) {
                isDown = true;

                startX = e.pageX;
                startY =  e.pageY;
                scrollLeft = $board.scrollLeft();
                scrollTop = $board.scrollTop();
                
                e.preventDefault();
            });

            $(document).on('mousemove touchmove', function (e) {
                
                if (!isDown) 
                    return;

                var dx = e.pageX - startX;
                var dy = e.pageY - startY;

                $board.scrollLeft(scrollLeft - dx);
                $board.scrollTop(scrollTop - dy);
                e.preventDefault();
            });

            $(document).on('mouseup touchend touchcancel', () => {
                isDown = false;
            });
    });
})(jQuery);