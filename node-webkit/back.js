var spawn = require('child_process').spawn

function startBack() {
  process.send({status: 'starting Pallas back end'});

  var pallas = spawn('python', ['Pallas/pallas.py']);

  pallas.stdout.on('data', function (data) {
    process.send({status: 'stdout: ' + data});
  });

  pallas.stderr.on('data', function (data) {
    process.send({status: 'stderr: ' + data});
  });

  pallas.on('close', function (code) {
    process.send({status: 'child process exited with code ' + code});
  });
}

process.on('message', function(data) {
  startBack();
});
