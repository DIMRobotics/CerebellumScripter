import zmq
import math
from struct import pack, unpack

context = zmq.Context()
socket = context.socket(zmq.REQ)

# Set "True" in your script to setup debugging output
DEBUG = True

# Robot configuration constants

# ODetect sensors indices
OD_FRONT = 1
OD_FLEFT = 2
OD_LEFT = 4
OD_REAR = 8
OD_RIGHT = 16
OD_FRIGHT = 32

OD_FULLFRONT = OD_FRONT | OD_FLEFT | OD_FRIGHT
OD_SIDES = OD_LEFT | OD_RIGHT
OD_ALL = 63

# Binary sensors indices
BSENSOR_SHMORGALKA = 1
BSENSOR_SELECTOR = 2

# Robot physical parameters
ROBOT_RADIUS = 146.5


def cdbg(module, string):
    if DEBUG:
        print ' [', module, '] ', string


def connect(zmq_address):
    socket.connect(zmq_address)
    cdbg("CONNECT", "Socket created")


def twist(left_speed, right_speed, distance):
    cdbg("TWIST", "Move: left speed " + str(left_speed) + ", right speed" +
         str(right_speed) + ", distance " + str(distance))

    data = pack("!ddd", left_speed, right_speed, distance)
    socket.send_multipart(["set", "twist", data])
    socket.recv_multipart()


def twist_busy():
    socket.send_multipart(["get", "twist_busy", ""])
    reply = socket.recv_multipart()
    if reply[0] == "b":
        return True
    else:
        return False


def twist_wait():
    cdbg("TWIST", "Waiting for robot stop")
    while twist_busy():
        pass
    cdbg("TWIST", "Robot stopped")


def twist_block(left_speed, right_speed, distance):
    twist(left_speed, right_speed, distance)
    twist_wait()


def twist_rotate(speed, angle):
    global ROBOT_RADIUS
    twist(speed, -speed, ROBOT_RADIUS * angle * math.pi / 180)


def twist_rotate_block(speed, angle):
    global ROBOT_RADIUS
    twist_block(speed, -speed, ROBOT_RADIUS * angle * math.pi / 180)


def dynamics(acceleration, brake):
    cdbg("TWIST", "Set dynamics: acceleration " + str(acceleration) +
         ", brake " + str(brake))
    data = pack("!dd", acceleration, brake)
    socket.send_multipart(["set", "dynamics", data])
    socket.recv_multipart()


def odetect_limit(directions, limit):
    cdbg("ODETECT", "Set limit for " + bin(directions) + ": " + str(limit))
    data = pack("!Ii", directions, limit)
    socket.send_multipart(["set", "odetect_limits", data])
    socket.recv_multipart()


def position_get():
    socket.send_multipart(["get", "position", ""])
    reply = socket.recv_multipart()
    data = unpack("!ddd", reply[1])
    return data


def servo(index, value):
    cdbg("SERVO", "Set servo " + str(index) + " to position " + str(value))
    data = pack("!id", index, value)
    socket.send_multipart(["set", "servo", data])
    socket.recv_multipart()


def sensor_get(index):
    socket.send_multipart(["get", "sensor", int(index)])
    reply = socket.recv_multipart()
    data = unpack("!i", reply[1])
    return data


def bsensor_get(index):
    socket.send_multipart(["get", "bsensor", pack("!I", index)])
    reply = socket.recv_multipart()
    data = unpack("!B", reply[0])
    if data[0]:
        return True
    else:
        return False


def led(state):
    if state > 0:
        state = 0xFF

    cdbg("LED", "Set LED to state" + str(state))
    data = pack("!B", state)
    socket.send_multipart(["set", "led", data])
    socket.recv_multipart()
