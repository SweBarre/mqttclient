import os

ICON = os.path.dirname(os.path.realpath(__file__))+'/icon.png'

def prep(msg=None):
    return_dict = {}
    return_dict['runner'] = 'notify'
    if msg is not None:
        result = msg.payload.split("]", 1)
        return_dict['title'] = result[0] + "]"
        return_dict['message'] = result[1]
        return_dict['icon'] = ICON
    return return_dict
