from pynput import mouse, keyboard

def execute_on_user_activity(action):
    """Executes action when user activity is detected."""

    def action_no_args(*args):
        action()

    mouse_listener = mouse.Listener(
            on_move = action_no_args,
            on_click = action_no_args)
    mouse_listener.start()

    keyboard_listener = keyboard.Listener(on_press = action_no_args)
    keyboard_listener.start()