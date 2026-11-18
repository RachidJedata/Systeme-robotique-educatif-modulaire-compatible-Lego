
import time
import board
import digitalio
import microcontroller
import os
import matrice

print("MASTER CONTROLLER")



# ==========================================
# BUTTON CONFIGURATION
# ==========================================

def setup_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    return button


previous = setup_button(microcontroller.pin.PA03)
next_btn = setup_button(microcontroller.pin.PB07)
run_btn = setup_button(microcontroller.pin.PA04)


def wait_release(button):
    while not button.value:
        time.sleep(0.01)
    time.sleep(0.05)


# ==========================================
# SHARED MEMORY
# ==========================================

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


# ==========================================
# PROGRAM DISCOVERY
# ==========================================

def discover_programs():

    programs = [
        file[:-3]
        for file in os.listdir("/")
        if file.endswith(".py")
        and file not in ("code.py", "matrice.py")
    ]

    programs.sort()

    return programs


# ==========================================
# MATRIX MENU DISPLAY
# ==========================================

def show_menu():

    matrice.afficher_numero(selected + 1)


# ==========================================
# SLAVE APPLICATION EXECUTION
# ==========================================

def launch_application(program_name):

    print("\n[MASTER] Loading:", program_name)

    filename = "/" + program_name + ".py"

    try:

        with open(filename, "r") as f:
            program_code = f.read()

        context["exit_requested"] = False

        shared_memory["selected_program"] = program_name
        shared_memory["application_running"] = True
        shared_memory["message"] = "Starting"

        app_env = {
            "__name__": "__main__",
            "context": context,
            "shared": shared_memory
        }

        exec(program_code, app_env)

        setup = app_env.get("setup")
        app_loop = app_env.get("loop")
        cleanup = app_env.get("cleanup")

        if not callable(app_loop):
            raise Exception("Application must define loop(context)")

        if callable(setup):
            setup(context)

        print("[MASTER] Application running")

        shared_memory["message"] = "Running"

        # MASTER-SLAVE LOOP
        while not context["exit_requested"]:

            app_loop(context)

            if not run_btn.value:

                print("[MASTER] Stop requested")

                context["exit_requested"] = True
                wait_release(run_btn)

            time.sleep(0.001)

        if callable(cleanup):
            cleanup(context)

    except Exception as e:

        print("[MASTER] Application error:", e)

    finally:

        shared_memory["application_running"] = False
        shared_memory["message"] = "Stopped"

        print("[MASTER] Application stopped")


# ==========================================
# INITIALIZATION
# ==========================================

matrice.initialiser_matrice()

programs = discover_programs()

if not programs:

    matrice.afficher_smiley()
    print("No applications found!")

    while True:
        time.sleep(1)


selected = 0


# ==========================================
# STARTUP ANIMATION
# ==========================================

# Display smiley at startup
matrice.afficher_smiley()
time.sleep(2)

# Display initial menu
show_menu()


# ==========================================
# MAIN MASTER LOOP
# ==========================================

while True:

    # PREVIOUS BUTTON
    if not previous.value:

        selected = (selected - 1) % len(programs)

        show_menu()

        print("[MENU] Selected:", programs[selected])

        wait_release(previous)


    # NEXT BUTTON
    if not next_btn.value:

        selected = (selected + 1) % len(programs)

        show_menu()

        print("[MENU] Selected:", programs[selected])

        wait_release(next_btn)


    # RUN BUTTON
    if not run_btn.value:

        wait_release(run_btn)

        launch_application(programs[selected])

        print("\n[MASTER] Returning to menu")

        # Reset shared variables
        shared_memory["selected_program"] = None
        shared_memory["application_running"] = False
        context["exit_requested"] = False

        # Redisplay selected application
        show_menu()


    time.sleep(0.02)
