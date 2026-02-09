const { task, parallel, series } = require('gulp');

// Load tasks from the tasks/ folder (if any)
require('fs').readdirSync('./tasks/').forEach(function (task) {
  require('./tasks/' + task);
});

task('build', series('clean', parallel('html', 'css', 'js', 'img', 'json', 'font')));
task('release', series('build'));
// gulp.task('qa', gulp.series('release'));
task('default', series('build', parallel('watch'))); //, 'serve'