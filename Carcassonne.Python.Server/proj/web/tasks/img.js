const gulp = require('gulp');

gulp.task('img:img', () => {

    return gulp.src('src/img/**/*.png')
        .pipe(gulp.dest('dist/img'))
});
gulp.task('img:app:watch', () => {
    return gulp.watch('src/img/**/*.png', gulp.series('img:img'));
});
gulp.task('img', gulp.parallel('img:img'));