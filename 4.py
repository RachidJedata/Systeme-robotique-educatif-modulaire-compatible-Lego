
import time
import board
import digitalio
import microcontroller

led = None
last_toggle = 0
program = "Program 4"
timeOut = 4

def setup(context):

    global led, last_toggle

    led = digitalio.DigitalInOut(microcontroller.pin.PB03)
    led.direction = digitalio.Direction.OUTPUT

    last_toggle = time.monotonic()

    context["shared"]["counter"] = 0

    print("[SLAVE]"  + program)


def loop(context):

    global last_toggle

    now = time.monotonic()

    if now - last_toggle >= timeOut:

        led.value = not led.value

        context["shared"]["led_state"] = led.value
        context["shared"]["counter"] += 1

        last_toggle = now


def cleanup(context):

    led.value = False
    led.deinit()

    print("[SLAVE]" + + program)
