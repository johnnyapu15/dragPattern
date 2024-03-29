//var socket_worker = new Worker("{{ url_for('static', filename='js/socketio_w.js') }}");
var socket_worker = new Worker('http://' + document.domain + ':' + location.port + "/static/js/socketio_w.js");
var ntpDelta = 0;
var ntpCount = 0;
socket_worker.postMessage({
    init:true,
    data: 'http://' + document.domain + ':' + location.port
});

// socket_worker.postMessage(
//     {emit: true, m:update, ... }
// );

socket_worker.onmessage = function(e) {
    switch (e.data["m"]) {
        case "update":
            //document.getElementById("textarea").innerHTML = "#Room: " + room_id + "\nDev Number: " + e.data["data"]["count"];
            break;
        // case "connect":
        //     socket_worker.postMessage({
        //         emit: true,
        //         m:"join",
        //         data:data
        //     });
        //     break;
        // case "ntp_0":
        //     socket_worker.postMessage({
        //         emit:true,
        //         m:"ntp_1",
        //         data:Date.now()
        //     });
        //     break;
        //case "redirect":
        case "demo-2d-line":
            //lineInit(e.data["data"]);
            break;
        case "demo-2d-pnt":
            pntUpdate(e.data["data"]);
            break;
        case "drawArranged":
            drawArranged(e.data["data"]);
            break;
        case "room_kill":
            room_killed();
            break;
        case "flash":
            flash(e.data["data"]);
            break;
        case "checked":
            console.log("sett");
            location.href = 'http://' + document.domain + ':' + location.port + '/checked/' + dev_id;
            break;
        case "ntpDelta":
            if (ntpCount == 0) {
                ntpDelta /= 10;
                flash("Time sync: " + ntpDelta);
                ntping = true;
                clocking();
            } else {
                if (ntpCount > 0) {
                    ntpDelta += e.data["data"];
                    flash("NTPing: " + ntpDelta);
                    ntpCount -= 1;
                    ntpStart();
                }
                else {
                    ntpCount = 0;
                }
            }
            break;
    };
};
// self.addEventListener("update", function(e) {
//     document.getElementById("textarea").innerHTML = "#Room: " + room_id + "\nDev Number: " + e.data.count;
// });

// self.addEventListener("demo-2d-line", function(e) {
//     lineInit
// });

// self.addEventListener("update", function(e) {

// });

// self.addEventListener("update", function(e) {

// });

//send msg using socket
function sendMsg(e) {
    socket_worker.postMessage({
        emit:true,
        m:e.m,
        data:e.data
    });
};

//line upload
// function 

//resetline
function resetLines() {
    socket_worker.postMessage({
        emit: true,
        m:"reset_lines"
    });
};

//2d demo init
function demo2dInit() {
    socket_worker.postMessage({
        emit: true,
        m: "2d-demo"
    });
};

//send pnt data
function sendPnt(data) {
    socket_worker.postMessage({
        emit:true,
        m: '2d-demo-pnt',
        data:data
    });
}

// ntp
function ntpStart() {
    socket_worker.postMessage({
        ntp:true
    });
}