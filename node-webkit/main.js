var ch = require('child_process');
var nb_msg = 0;

console.log('Current directory: ' + process.cwd());

console.log("Spawning a new process");
var processing = ch.fork('node-webkit/back.js');

processing.on('close', function(code, signal) {
  var pid = this.pid;

  if (!!code) console.log('1: exit ' + code); else console.log('1: signal ' + signal);
});
processing.on('error', function(err) {
  console.log(err.message);
  process.exit(1);
});

processing.on('message', function(data) {
  console.log(data);
  nb_msg += 1;
  if (nb_msg == 2) {
    console.log("Redirecting to UI");
    window.location.replace('../Pallas/Handler/ui/index.html?from=node-webkit')
  }
});

processing.on('exit', function(code) {
  console.log('exited with code:', code);
});

processing.send({});
