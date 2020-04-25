$(document).ready(function() {
namespace = '/test';

// Connect to the Socket.IO server.
// The connection URL has the following format, relative to the current page:
//     http[s]://<domain>:<port>[/<namespace>]
var socket = io(namespace);

socket.on('connect', function() {
	console.log('Connected');
});

// Event handler for server sent data.
// The callback function is invoked whenever the server emits data
// to the client. The data is then displayed in the "Received"
// section of the page.
socket.on('my_response', function(msg, cb) {
 if (msg.data.hasOwnProperty('filename'))
   $("#slider").prepend('<div class="slide" style="background-image: url(\'' + msg.data.filename + '\');"></div>');
   $("#slider").scrollLeft(0);
 	//$("#image").css("background-image", "url('"+msg.data.filename+"')");
 if (cb)
     cb();
});

// Interval function that tests message latency by sending a "ping"
// message. The server then responds with a "pong" message and the
// round trip time is measured.
var ping_pong_times = [];
var start_time;
window.setInterval(function() {
    start_time = (new Date).getTime();
    socket.emit('my_ping');
}, 1000);

// Handlers for the different forms in the page.
// These accept data from the user and send it to the server in a
// variety of ways
$('form#emit').submit(function(event) {
 socket.emit('my_event', {data: $('#emit_data').val()});
 return false;
});
$('form#broadcast').submit(function(event) {
 socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
 return false;
});
  });