import os

ICON = os.path.dirname(os.path.realpath(__file__))+'/icon.png'

def init(config=None):
    pass

def prep(msg=None):
    return_dict = {}
    return_dict['runner']='notify'
    if msg is not None:
        return_dict['title'], return_dict['message'] = msg.payload.split(":", 1)
        return_dict['icon'] = ICON
    return return_dict
