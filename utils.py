import RPi.GPIO as GPIO
import time
import drivers
import requests

IOTA_URL = "https://explorer-api.iota.org/search/mainnet/iota1qqc9mzff65d8d44y7gp0s4jrt7rdygua2kqmh242apcwhdcw0236sxh6esw"
PAYMENT_URL = "http://localhost:8000/payment"

def get_balance():
    response = requests.get(IOTA_URL).json()
    print(response)

    if response['address']['balance'] == None:
        print("Error: Fetch fail! No balance!")
        return -1

    return response.balance

def pusher():
    CONTROL_PIN = 11
    PWM_FREQ = 50

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN, GPIO.OUT)

    pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
    pwm.start(12)

    degrees = [12.0, 2.0, 12.0]
    try:
        # while True:
        #     time.sleep(0.01)
        #     button_state = GPIO.input(BUTTON_PIN)
        #     if button_state != previous_button_state:
        #         previous_button_state = button_state
        #         if button_state == GPIO.HIGH:
        #             print("Pressed")
        for i in range(1):
            for deg in degrees:
                pwm.ChangeDutyCycle(deg)
                time.sleep(1)
    except KeyboardInterrupt:
        pwm.ChangeDutyCycle(0)
        pwm.stop()
        GPIO.cleanup()
        print("End")

def lcd(message = "Pay 5Mi to buy"):
    # Load the driver and set it to "display"
    # If you use something from the driver library use the "display." prefix first
    display = drivers.Lcd()

    # Main body of code
    try:
        print("Writing to display")
        # Remember that your sentences can only be 16 characters long!
        if message != "Pay 5Mi to buy!":
            display.lcd_display_string("Processing...", 1)
        else:
            display.lcd_display_string("IOTA Machine", 1)
        display.lcd_display_string(message, 2)
    except KeyboardInterrupt:
        # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        print("Cleaning up!")
        #display.lcd_clear()

def detect_button():
    BUTTON_PIN = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    previous_button_state = GPIO.input(BUTTON_PIN)
    while True:
        time.sleep(0.01)
        button_state = GPIO.input(BUTTON_PIN)
        if button_state != previous_button_state:
            previous_button_state = button_state
            if button_state == GPIO.HIGH:
                print("Pressed")
                response = requests.post(PAYMENT_URL)
                print(response)
