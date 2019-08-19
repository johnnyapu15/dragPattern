from flask import Flask, render_template, request, session
import flask_socketio as si
from pythons.dragnnect_exp import *
from pythons.fileio import *
from datetime import datetime
from pythons.check import * 

app = Flask(__name__) 
app.secret_key = 'the random string'
socketio = si.SocketIO(app, manage_session=False)

room = dict()

hints = ['E', 'V', 'E']

@app.route('/')
def index():
    return render_template('index.html')


# 1. Create room
@app.route('/roomInit', methods=["POST"])
def roomInit():
    print(request.form)
    session['id'] = str(request.form['id'])
    session['room_id'] = str(request.form['room_id'])
    session['dev_info'] = str(request.form['dev_info'])
    if not(session['room_id'] in room.keys()):
        room[session['room_id']] = dict()
        room[session['room_id']]['devices'] = dict()
        room[session['room_id']]['sequence'] = 0
        room[session['room_id']]['lines'] = []
    room[session['room_id']]['sequence'] += 1
    session['device_id'] = str(room[session['room_id']]['sequence'])
    session['dev_id'] = str(room[session['room_id']]['sequence'])
    room[session['room_id']]['devices'][session['device_id']] = DeviceArrangement(session['device_id'])
    return render_template('canvas.html', session=session)

# 2. Estimate arrangements & Check pattern
@app.route('/draw')
def estimation():
    print("good.")

@app.route('/checked/<dev_id>')
def checkSite(dev_id):
    print(dev_id)
    return render_template('checked.html', hint = hints[int(dev_id) - 1])



#################################################
# SocketIO functions ############################

#################################################

@socketio.on('init')
def initSocketIO():
    si.join_room(session['room_id'])
    print("Initiating socketIO...")
    si.emit('update', {'count':room[session['room_id']]['sequence']}, room = session['room_id'])

@socketio.on('ntp_start')
def ntp_0():
    print('ntp...0')
    t0 = int(datetime.utcnow().timestamp() * 1000)
    si.emit('ntp_0')
    room[session['room_id']]['devices'][session['device_id']].ntpTimes = t0


@socketio.on('ntp_1')
def ntp_1(t1):
    print('ntp...1')
    t2 = int(datetime.utcnow().timestamp() * 1000)
    t0 = room[session['room_id']]['devices'][session['device_id']].ntpTimes
    delay = ((t1 - t0) + (t2 - t1)) / 2
    delta = t1 - t0 - delay
    si.emit('ntp_delta', delta)
    room[session['room_id']]['devices'][session['device_id']].ntpDelay = delay
    print("Delta for " + str(session['device_id']) +": " + str(delta))

@socketio.on('reset_lines')
def reset_lines():
    room_id = session['room_id']
    for key, dev in room[room_id]['devices'].items():
        dev.setDeviceSize(0, 0)
    #room_lines[room_id] = []
    room[room_id]['lines'] = []
    print(str(room_id) + ": reset lines...")

@socketio.on('kill_room')
def kill_room():
    si.emit("room_kill", room=session['room_id'])
    id = session['room_id']
    del room[id]['devices']
    #del room_lines[session['room_id']]
    del room[id]['lines']
    del room[id]['sequence']
    del room[id]
    print("room killed.")

@socketio.on('device_update')
def dev_update2(data):
    print(session['device_id'])
    print(room)
    room_id = session['room_id']
    count = room[room_id]['sequence']
    dev_id = str(session['device_id'])
    pnts = data['11pnts']
    l0 = LineData(dev_id)
    l0.set(pnts, data['start_time'])
    room[room_id]['devices'][dev_id].setDeviceSize(data['width'], data['height'])
    room[room_id]['devices'][dev_id].device_name = session['dev_info']
    room[room_id]['lines'].append(l0)
    ret = dict()
    if 2 * count - 2 <= len(room[room_id]['lines']):
        room[room_id]['lines'] = room[room_id]['lines'][0:(2*count-2)]
        # Init
        for key, dev in room[room_id]['devices'].items():
            dev.init()
        LD = devLineToData(
            [
                room[room_id]['expNum'],
                room_id
            ], 
            room[room_id]['devices'], room[room_id]['lines']
        )
        saveLine(LD)
        for i, l in enumerate(LD):
            l['first']['lines'] = np.array(l['first']['lines'])
            l['second']['lines'] = np.array(l['second']['lines'])
        # Calculate
        for i, l in enumerate(LD):
            # print(l)
            i0 = str(l['first']['dev_index'])
            i1 = str(l['second']['dev_index'])
            output = heuristic_basic(l)
            room[room_id]['devices'][i0].link(
                room[room_id]['devices'][i1],
                output
            )
            print("Output:")
            print(output)
        for key, dev in room[room_id]['devices'].items():
            ret[str(dev.device_id)] = \
                [dev.get2dPoints(), dev.alpha, dev.rot[1]]
        # print("drawing...")
        # print(LD)
        print("ret: ")
        print(ret)
        storePattern(ret, room[room_id]['expNum'])
        print(">>>>>Check:")
        chec = check(ret)
        if chec[0] < 0:
            print(chec[1])
            si.emit('flash', "Wrong pattern!" , room=session['room_id']) 
        else:
            print("CHECKED!")
            si.emit('checked', room=session['room_id']) 
        
        # si.emit('draw', ret, room=room_id)
        # print('drawed')
        # Reset
        for key, dev in room[room_id]['devices'].items():
            dev.setDeviceSize(0, 0)
        room[room_id]['lines'] = []
    elif 2 * count - 2 > len(room[room_id]['lines']):
        # Listening,,,
        return
    else:
        # TODO: draw or reset
        for key, dev in room[room_id]['devices'].items():
            dev.setDeviceSize(0, 0)
        room[room_id]['lines'] = []
        return

@socketio.on('sendingExpNum')
def setExpNum(data):
    print("exp: " + str(data))
    room[session["room_id"]]["expNum"] = data
    si.emit('flash', "Experiment number is " + str(room[session["room_id"]]["expNum"]))
#################################################
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')