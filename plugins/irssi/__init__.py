# this is a plugin to parse messages from
# https://github.com/dm8tbr/irssi-mqtt-notify/

import os

ICON = os.path.dirname(os.path.realpath(__file__))+'/icon.png'

def prep(msg=None):
    return_dict = {}
    return_dict['runner'] = 'notify'
    delimiter = None
    if msg is not None:
        if msg.payload[0] == "(":
            # PM is sent
            delimiter = ")"
        if msg.payload[0] == "[":
            # Hilight is sent
            delimiter = "]"

        if delimiter is None:
            # Unable to identify message type, do topif as title
            # and complete payload as message
            return_dict['title'] = msg.topic
            return_dict['message'] = msg.payload
        else:
            result = msg.payload.split(delimiter, 1)
            return_dict['title'] = result[0] + delimiter
            return_dict['message'] = result[1]
        return_dict['icon'] = ICON
    return return_dict
