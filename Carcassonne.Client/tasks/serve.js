
const gulp = require('gulp');
const browserSync = require('browser-sync').create();

gulp.task('serve', function () {

    browserSync.init({ notify: false, server: { baseDir: "./dist" } });

    gulp
        .watch(['dist/index.html', 'dist/**/*.css', 'dist/**/*.js'])
        .on("change", browserSync.reload);
});