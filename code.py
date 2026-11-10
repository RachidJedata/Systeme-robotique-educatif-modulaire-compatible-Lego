
import time
import board
import digitalio
import microcontroller
import os


print("MASTER CONTROLLER")





def setup_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    return button


previous = setup_button(microcontroller.pin.PA03)
next_btn = setup_button(microcontroller.pin.PA04)
run_btn = setup_button(microcontroller.pin.PB07)


def wait_release(button):
    while not button.value:
        time.sleep(0.01)
    time.sleep(0.05)


# Shared RAM between MASTER and SLAVE applications

shared_memory = {
    "counter": 0,
    "selected_program": None,
    "application_running": False,
    "led_state": False,
    "message": "Ready"
}




context = {
    "shared": shared_memory,
    "exit_requested": False
}



def discover_programs():

    programs = [
        file[:-3]
        for file in os.listdir("/")
        if file.endswith(".py")
        and file != "code.py"
    ]

    programs.sort()

    return programs


# ==========================================
# SLAVE APPLICATION EXECUTION
# ==========================================

def launch_application(program_name):

    print("\n[MASTER] Loading:", program_name)

    filename = "/" + program_name + ".py"

    try:

        # Read application source
        with open(filename, "r") as f:
            program_code = f.read()

        # Reset application context
        context["exit_requested"] = False

        shared_memory["selected_program"] = program_name
        shared_memory["application_running"] = True
        shared_memory["message"] = "Starting"

        # Create isolated application namespace
        app_env = {
            "__name__": "__main__",
            "context": context,
            "shared": shared_memory
        }

        # Load application
        exec(program_code, app_env)

        # Get application functions
        setup = app_env.get("setup")
        app_loop = app_env.get("loop")
        cleanup = app_env.get("cleanup")

        if not callable(app_loop):
            raise Exception("Application must define loop(context)")

        # Initialize slave
        if callable(setup):
            setup(context)

        print("[MASTER] Application running")

        shared_memory["message"] = "Running"

        # MASTER-SLAVE LOOP
        while not context["exit_requested"]:

            # Execute one application cycle
            app_loop(context)

            # MASTER monitors RUN button
            if not run_btn.value:

                print("[MASTER] Stop requested")

                context["exit_requested"] = True
                wait_release(run_btn)

            time.sleep(0.001)

        # Stop slave application
        if callable(cleanup):
            cleanup(context)

    except Exception as e:

        print("[MASTER] Application error:", e)

    finally:

        shared_memory["application_running"] = False
        shared_memory["message"] = "Stopped"

        print("[MASTER] Application stopped")


# ==========================================
# MASTER MENU
# ==========================================

programs = discover_programs()

if not programs:

    print("No applications found!")

    while True:
        time.sleep(1)


selected = 0

print("\nAvailable applications:")

for i, program in enumerate(programs):
    print(i, "-", program)


# ==========================================
# MAIN MASTER LOOP
# ==========================================

while True:

    print(
        "\rSelected:",
        programs[selected],
        "       ",
        end=""
    )

    # PREVIOUS
    if not previous.value:

        selected = (selected - 1) % len(programs)

        print("\nSelected:", programs[selected])

        wait_release(previous)

    # NEXT
    if not next_btn.value:

        selected = (selected + 1) % len(programs)

        print("\nSelected:", programs[selected])

        wait_release(next_btn)

    # RUN
    if not run_btn.value:

        wait_release(run_btn)

        launch_application(programs[selected])

        print("\nReturning to MASTER menu")

        # Refresh shared variables
        shared_memory["selected_program"] = None
        context["exit_requested"] = False

    time.sleep(0.02)
