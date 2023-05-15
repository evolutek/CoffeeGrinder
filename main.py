#!/usr/bin/python3
from time import sleep
import lib.gpios as GPIO
from flask import Flask, jsonify, render_template, request, redirect
import threading

MATCH_STATUS_INIT = "0"
MATCH_STATUS_STARTED = "1"
MATCH_STATUS_ENDED = "2"
app = Flask(__name__)
match = {'Balls': 0, 'Status': MATCH_STATUS_INIT}
match_lock = threading.Lock()

@app.route("/")
def interface():
    return render_template('index.html', balls=match['Balls'], status=match['Status'])


@app.route("/api/status", methods=['PUT'])
def update_status():
    data = request.json
    status = request.form.get('status')
    with match_lock:
        match['Status'] = status
        if status == MATCH_STATUS_STARTED or status == MATCH_STATUS_INIT:
            match['Balls'] = 0
            UpdateGraphics("UwU.png")
    return jsonify({'status': status, 'data': data})

@app.route("/api/status_post", methods=['POST'])
def update_status_post():
    status = request.form['status']
    with match_lock:
        match['Status'] = status
        if status == MATCH_STATUS_STARTED or status == MATCH_STATUS_INIT:
            match['Balls'] = 0
            UpdateGraphics("UwU.png")
    return redirect('/')


@app.route("/api/get_status")
def get_ball_count():
    with match_lock:
        status = match.copy()
    return jsonify(status)


def UpdateGraphics(filename):
    file = open("display/target", "w")
    file.write(filename)
    file.close()

def main_loop():
    screensaver_current = 1
    DETECT_UP = False
    while True:
        if match['Status'] == MATCH_STATUS_STARTED:
            if GPIO.get_pin(GPIO.PIN_SICK):
                if not DETECT_UP:
                    DETECT_UP = True
                    print("Detect up!")
                    sleep(0.5)
            else:
                if DETECT_UP:
                    DETECT_UP = False
                    if match['Balls'] < 10:
                        match['Balls'] += 1
                    UpdateGraphics(f"{match['Balls']}.png")
                    print(f"Ball passed! Detect set to down!\n total count: {match['Balls']}")
        elif match['Status'] == MATCH_STATUS_ENDED:
            if match['Balls'] < 1:
                UpdateGraphics("pedo5.png")
            #Custom idle display opions
            sleep(1)
        elif match['Status'] == MATCH_STATUS_INIT:
            UpdateGraphics(f"cm_ss_{screensaver_current}.png")
            screensaver_current += 1
            if screensaver_current > 12:
                screensaver_current = 1
            sleep(3)
        sleep(0.01)

if __name__ == "__main__":
    GPIO.init_pin(GPIO.PIN_SICK, output = False, pud_up = False)
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
    app.run(threaded=True, host='0.0.0.0')
    
