"""
Plugin that uses libnotify to display mqtt subscriptoins

config:
    urgency      low, normal or critical
    icon         absolute path to the icon
"""
import os
import pynotify

ICON = os.path.dirname(os.path.realpath(__file__))+'/icon.png'
pynotify.init("MQTTClient")

def prep(msg=None, config=None):
    return_dict = {}
    return_dict['config'] = config
    if msg is not None:
        return_dict = {'title': msg.topic, 'message': msg.payload, 'icon': ICON }
    return return_dict
    

def run(**kwargs):
    notification = pynotify.Notification(kwargs['title'], kwargs['message'], kwargs['icon'])
    notification.set_urgency(pynotify.URGENCY_CRITICAL)
    notification.show()
