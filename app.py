from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
import time
import random

app = Flask(__name__)

# Initialize Camera
camera = cv2.VideoCapture(0)

# Robot Status
robot_status = {
    "movement": "Stopped",
    "color_detected": "None",
    "voice_response": ""
}

# =========================
# MOTOR CONTROL FUNCTIONS
# =========================

def move_forward():
    robot_status["movement"] = "Moving Forward"
    print("Robot Moving Forward")

def move_backward():
    robot_status["movement"] = "Moving Backward"
    print("Robot Moving Backward")

def turn_left():
    robot_status["movement"] = "Turning Left"
    print("Robot Turning Left")

def turn_right():
    robot_status["movement"] = "Turning Right"
    print("Robot Turning Right")

def stop_robot():
    robot_status["movement"] = "Stopped"
    print("Robot Stopped")

# =========================
# VIDEO STREAMING
# =========================

def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            break
        else:
            # Convert frame into jpeg
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# =========================
# COLOR DETECTION
# =========================

def detect_color():
    colors = ["Red", "Green", "Blue", "Yellow"]
    detected = random.choice(colors)
    robot_status["color_detected"] = detected
    return detected

# =========================
# VOICE RESPONSE SYSTEM
# =========================

def voice_command(command):
    responses = {
        "hello": "Hello, I am your Smart Surveillance Robot.",
        "status": "All systems are working properly.",
        "move": "Robot is ready to move.",
        "camera": "Camera streaming is active.",
        "stop": "Robot stopped successfully."
    }

    reply = responses.get(command.lower(), "Command not recognized.")
    robot_status["voice_response"] = reply

    return reply

# =========================
# ROUTES
# =========================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move', methods=['POST'])
def move():

    direction = request.form.get('direction')

    if direction == "forward":
        move_forward()

    elif direction == "backward":
        move_backward()

    elif direction == "left":
        turn_left()

    elif direction == "right":
        turn_right()

    elif direction == "stop":
        stop_robot()

    return jsonify({
        "status": "success",
        "movement": robot_status["movement"]
    })

@app.route('/detect_color')
def color_detection():

    color = detect_color()

    return jsonify({
        "detected_color": color
    })

@app.route('/voice_command', methods=['POST'])
def handle_voice_command():

    command = request.form.get('command')

    response = voice_command(command)

    return jsonify({
        "response": response
    })

@app.route('/status')
def status():

    return jsonify(robot_status)

# =========================
# MAIN FUNCTION
# =========================

if __name__ == '__main__':

    print("Starting Smart Surveillance Robot Server...")

    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False,
        threaded=True
    )

    camera.release()
