const gulp = require('gulp');
const concat = require('gulp-concat');
const cleanCSS = require('gulp-clean-css');

gulp.task('json:i18n', () => {

    return gulp.src('src/i18n/**/*.json')
        .pipe(gulp.dest('dist/i18n'))
});
gulp.task('json:app:watch', () => {
    return gulp.watch('src/i18n/**/*.json', gulp.series('json:i18n'));
});
gulp.task('json', gulp.parallel('json:i18n'));