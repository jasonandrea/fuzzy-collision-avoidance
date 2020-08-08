# Import tkinter module for GUI
from tkinter import *

# Fuzzifier, range of variables
# Notation: "start:max value:end"
distRange = {
    "CLOSE": [0, 0, 30],
    "INTERMEDIATE": [20, 40, 60],
    "LONG": [50, 100, 100]}
speedRange = {
    "SLOW": [0, 0, 40],
    "MEDIUM": [30, 70, 110],
    "FAST": [100, 140, 140]}

# Defuzzifier, range of variables
# Notation: "start:max value:end"
brakeRange = {
    "SOFT": [0, 0, 40],
    "MEDIUM": [30, 50, 70],
    "HARD": [60, 100, 100]}


def calcDegreeTrapezoidR(x, a, b):
    """
    Calculate the membership degree of trapezoid R-function
    :param x: the value from the user
    :param a: lower limit
    :param b: upper limit
    :return: membership degree
    """
    if x > b:
        return 0
    elif x >= a and x <= b:
        return float(b - x) / (b - a)
    else:
        return 1


def calcDegreeTrapezoidL(x, a, b):
    """
    Calculate the membership degree of trapezoid L-function
    :param x: the value from the user
    :param a: lower limit
    :param b: upper limit
    :return: membership degree of x
    """
    if x < a:
        return 0
    elif x >= a and x <= b:
        return float(x - a) / (b - a)
    else:
        return 1


def calcDegreeTriangular(x, a, b, m):
    """
    Calculate the membership degree of triangular function
    :param x: the value from the user
    :param a: lower limit
    :param b: upper limit
    :param m: the peak, where a < m < b
    :return: membership degree of x
    """
    if x <= a or x >= b:
        return 0
    elif x > a and x <= m:
        return float(x - a) / (m - a)
    else:
        return float(b - x) / (b - m)


def fuzzify(distance, speed):
    """
    Fuzzification of input from the parameter
    :param distance: input distance to be fuzzified
    :param speed: input speed to be fuzzified
    :return: the result of fuzzification process
    """
    distDegrees = [-1, -1, -1]  # [SHORT, INTERMEDIATE, LONG]
    speedDegrees = [-1, -1, -1]  # [SLOW, MEDIUM, FAST]

    # Get degrees of distance
    if distance < distRange["INTERMEDIATE"][0]:
        distDegrees[0] = calcDegreeTrapezoidR(distance, distRange["CLOSE"][0], distRange["CLOSE"][2])
    elif distance <= distRange["CLOSE"][2]:
        distDegrees[0] = calcDegreeTrapezoidR(distance, distRange["CLOSE"][0], distRange["CLOSE"][2])
        distDegrees[1] = calcDegreeTriangular(distance, distRange["INTERMEDIATE"][0], distRange["INTERMEDIATE"][2],
                                              distRange["INTERMEDIATE"][1])
    elif distance < distRange["LONG"][0]:
        distDegrees[1] = calcDegreeTriangular(distance, distRange["INTERMEDIATE"][0], distRange["INTERMEDIATE"][2],
                                              distRange["INTERMEDIATE"][1])
    elif distance <= distRange["INTERMEDIATE"][2]:
        distDegrees[1] = calcDegreeTriangular(distance, distRange["INTERMEDIATE"][0], distRange["INTERMEDIATE"][2],
                                              distRange["INTERMEDIATE"][1])
        distDegrees[2] = calcDegreeTrapezoidL(distance, distRange["LONG"][0], distRange["LONG"][2])
    else:
        distDegrees[2] = calcDegreeTrapezoidL(distance, distRange["LONG"][0], distRange["LONG"][2])

    # Get degrees of speed
    if speed < speedRange["MEDIUM"][0]:
        speedDegrees[0] = calcDegreeTrapezoidR(speed, speedRange["SLOW"][0], speedRange["SLOW"][2])
    elif speed <= speedRange["SLOW"][2]:
        speedDegrees[0] = calcDegreeTrapezoidR(speed, speedRange["SLOW"][0], speedRange["SLOW"][2])
        speedDegrees[1] = calcDegreeTriangular(speed, speedRange["MEDIUM"][0], speedRange["MEDIUM"][2],
                                               speedRange["MEDIUM"][1])
    elif speed < speedRange["FAST"][0]:
        speedDegrees[1] = calcDegreeTriangular(speed, speedRange["MEDIUM"][0], speedRange["MEDIUM"][2],
                                               speedRange["MEDIUM"][1])
    elif speed <= speedRange["MEDIUM"][2]:
        speedDegrees[1] = calcDegreeTriangular(speed, speedRange["MEDIUM"][0], speedRange["MEDIUM"][2],
                                               speedRange["MEDIUM"][1])
        speedDegrees[2] = calcDegreeTrapezoidL(speed, speedRange["FAST"][0], speedRange["FAST"][2])
    else:
        speedDegrees[2] = calcDegreeTrapezoidL(speed, speedRange["FAST"][0], speedRange["FAST"][2])

    # Return both distance and speed degrees
    return distDegrees, speedDegrees


def inference(distance, speed):
    """
    The inference engine.
    :return: Brake pressure degrees to be defuzzified
    """
    softDegrees = [0]
    mediumDegrees = [0]
    hardDegrees = [0]
    degreesResult = [0, 0, 0]

    # IF speed IS slow AND distance IS close THEN brake medium
    if speed[0] != -1 and distance[0] != -1:
        mediumDegrees.append(min(speed[0], distance[0]))

    # IF speed IS slow AND distance IS intermediate THEN brake soft
    if speed[0] != -1 and distance[1] != -1:
        softDegrees.append(min(speed[0], distance[1]))

    # IF speed IS slow AND distance IS far THEN brake soft
    if speed[0] != -1 and distance[2] != -1:
        softDegrees.append(min(speed[0], distance[2]))

    # IF speed IS medium AND distance IS close THEN brake hard
    if speed[1] != -1 and distance[0] != -1:
        hardDegrees.append(min(speed[1], distance[0]))

    # IF speed IS medium AND distance IS intermediate THEN brake medium
    if speed[1] != -1 and distance[1] != -1:
        mediumDegrees.append(min(speed[1], distance[1]))

    # IF speed IS medium AND distance IS far THEN brake soft
    if speed[1] != -1 and distance[2] != -1:
        softDegrees.append(min(speed[1], distance[2]))

    # IF speed IS fast AND distance IS close THEN brake hard
    if speed[2] != -1 and distance[0] != -1:
        hardDegrees.append(min(speed[2], distance[0]))

    # IF speed IS fast AND distance IS intermediate THEN brake hard
    if speed[2] != -1 and distance[1] != -1:
        hardDegrees.append(min(speed[2], distance[1]))

    # IF speed IS fast AND distance IS far THEN brake medium
    if speed[2] != -1 and distance[2] != -1:
        mediumDegrees.append(min(speed[2], distance[2]))

    degreesResult[0] = max(softDegrees)
    degreesResult[1] = max(mediumDegrees)
    degreesResult[2] = max(hardDegrees)

    return degreesResult


def defuzzify(brake):
    """
    Defuzzification of the result from the inference engine to make
    the output become user friendly, using Weighted Average method.
    :param brake: brake degrees from the inference engine
    :return: defuzzified value, user friendly
    """
    soft = brake[0] * (brakeRange["SOFT"][2] - ((brakeRange["SOFT"][2] - brakeRange["SOFT"][0]) * brake[0]))
    medium = brake[1] * (brakeRange["MEDIUM"][2] - ((brakeRange["MEDIUM"][2] - brakeRange["MEDIUM"][0]) * brake[1]))
    hard = brake[2] * (brakeRange["HARD"][2] - ((brakeRange["HARD"][2] - brakeRange["HARD"][0]) * brake[2]))

    brakePressure = (soft + medium + hard) / sum(brake)

    return '{:0.2f}%'.format(brakePressure)


def buttonCalculate():
    """
    Calculate the brake needed based on user input via textboxes,
    this function is called by pressing 'Calculate' button.

    Values from 2 textboxes will be gathered, fuzzified, sent into inference engine
    and defuzzified. Defuzzified value will be shown to the user.
    """
    # Get both distance and speed from textboxes
    try:
        distance = int(txtInputDistance.get())
        speed = int(txtInputSpeed.get())
        # Raise an ValueError if input is less than 0
        if distance < 0 or speed < 0:
            raise ValueError
    except ValueError:
        lblOutput.configure(text='INVALID INPUT')
        return

    # Fuzzification
    distDegrees, speedDegrees = fuzzify(distance, speed)

    # Inference engine
    brakeDegrees = inference(distDegrees, speedDegrees)

    # Defuzzification
    brakePressure = defuzzify(brakeDegrees)

    # Edit output label for the user to see
    lblOutput.configure(text=brakePressure)


window = Tk()
window.title('Fuzzy Collision Avoidance')
window.resizable(False, False)

# Labels
lblInputSpeed = Label(window, text='Vehicle Speed (km/h)', font=('Arial', 10))
lblInputDistance = Label(window, text='Distance to Object (m)', font=('Arial', 10))
lblOutput = Label(window, text='', font=('Arial', 10))

# Label placements
lblInputSpeed.grid(column=0, row=0)
lblInputDistance.grid(column=0, row=1)
lblOutput.grid(column=1, row=2)

# Text boxes
txtInputSpeed = Entry(window, width=17)
txtInputDistance = Entry(window, width=17)

# Textbox placements
txtInputSpeed.grid(column=1, row=0)
txtInputDistance.grid(column=1, row=1)

# Button
btnCalculate = Button(window, text='Calculate', command=buttonCalculate)

# Button placement
btnCalculate.grid(column=0, row=2)

window.mainloop()
