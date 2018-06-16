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
    icon = ICON
    if config is not None:
        if 'icon' in config:
            icon = config['icon']
    if msg is not None:
        return_dict['title'] = msg.topic
        return_dict['message'] = msg.payload
        return_dict['icon'] = icon
    return return_dict
    

def run(**kwargs):
    priorities = {
            'low': pynotify.URGENCY_LOW,
            'normal': pynotify.URGENCY_NORMAL,
            'critical': pynotify.URGENCY_CRITICAL
            }
    priority = 'normal'
    if kwargs['config'] is not None:
        if 'urgency' in kwargs['config']:
            priority = kwargs['config']['urgency']
    notification = pynotify.Notification(kwargs['title'], kwargs['message'], kwargs['icon'])
    notification.set_urgency(priorities.get(priority))
    notification.show()
