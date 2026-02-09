const { src, dest, task, parallel, series } = require('gulp');

task('img:tiles', () => {
    return src(['src/img/tiles/*.*'], { encoding: false })
        .pipe(dest('dist/img/tiles'))
});
task('img', series(parallel('img:tiles')));