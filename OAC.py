import RPi.GPIO as GPIO
import time
import pigpio

# Define GPIO Pins (as per your new code)
TRIG = 23     # Ultrasonic Sensor TRIG Pin
ECHO = 24     # Ultrasonic Sensor ECHO Pin
SERVO = 17    # Servo Motor Control Pin

# Motor Driver Pins (L298N - as per your new code)
ENA = 4
IN1 = 5
IN2 = 6
IN3 = 13
IN4 = 19
ENB = 9

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT) # Only setup the direction control pins

# Motor PWM Control (Initialize but don't start yet, control in movement functions)
GPIO.setup([ENA, ENB], GPIO.OUT)
GPIO.output(ENA, True) # Enable A
GPIO.output(ENB, True) # Enable B
motorA_pwm = GPIO.PWM(ENA, 100)  # PWM at 100Hz
motorB_pwm = GPIO.PWM(ENB, 100)
motorA_pwm.start(0)   # Start with 0% duty cycle (stopped)
motorB_pwm.start(0)

# Start pigpio for servo
pi = pigpio.pi()
if not pi.connected:
    exit()

# Function to set servo angle using pigpio
def set_angle(angle):
    pulse_width = 500 + (angle * 2000 / 180)  # Convert angle to pulse width (500-2500us)
    pi.set_servo_pulsewidth(SERVO, pulse_width)
    time.sleep(0.5)

# Function to get distance from ultrasonic sensor
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10µs pulse
    GPIO.output(TRIG, False)

    start_time, stop_time = time.time(), time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2  # Convert time to distance in cm
    return round(distance, 2)

# Motor movement functions (now controlling PWM speed as well)
def move_forward(speed=50): # Speed 0-100
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    motorA_pwm.ChangeDutyCycle(speed)
    motorB_pwm.ChangeDutyCycle(speed)

def move_backward(speed=50):
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    motorA_pwm.ChangeDutyCycle(speed)
    motorB_pwm.ChangeDutyCycle(speed)

def turn_left(speed=50):
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    motorA_pwm.ChangeDutyCycle(speed)
    motorB_pwm.ChangeDutyCycle(speed)

def turn_right(speed=50):
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    motorA_pwm.ChangeDutyCycle(speed)
    motorB_pwm.ChangeDutyCycle(speed)

def stop_motors():
    motorA_pwm.ChangeDutyCycle(0)
    motorB_pwm.ChangeDutyCycle(0)
    GPIO.output([IN1, IN2, IN3, IN4], False)

# Main function to scan and move
def obstacle_avoidance():
    try:
        while True:
            set_angle(90)  # Center position
            distance = get_distance()
            print(f"Front Distance: {distance} cm")

            if distance < 15:  # Obstacle detected
                print("Obstacle detected! Stopping and scanning...")
                stop_motors()
                time.sleep(0.5)

                # Scan left
                set_angle(150)
                left_distance = get_distance()
                print(f"Left Distance: {left_distance} cm")

                # Scan right
                set_angle(30)
                right_distance = get_distance()
                print(f"Right Distance: {right_distance} cm")

                # Choose the best direction
                if left_distance > right_distance:
                    print("Turning Left")
                    turn_left()
                    time.sleep(1)
                else:
                    print("Turning Right")
                    turn_right()
                    time.sleep(1)

                stop_motors()
                time.sleep(0.5) # Small pause after turning
            else:
                move_forward()

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stop_motors()
        pi.set_servo_pulsewidth(SERVO, 0)
        pi.stop()
        GPIO.cleanup()

# Run the robot
obstacle_avoidance()