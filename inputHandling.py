controller = None

def init(controller_):
    global controller
    controller = controller_

def loop():
    if controller.buttons.triangle:
        return True
    else:
        return False
