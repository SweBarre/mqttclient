"""
Plugin that uses libnotify to display mqtt subscriptoins

config:
    urgency      low, normal or critical
    icon         absolute path to the icon
"""
import os
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

ICON = os.path.dirname(os.path.realpath(__file__))+'/icon.png'
Notify.init("MQTTClient")

def _mydecode(var):
    """ returns str of var """
    if isinstance(var, str):
        return var
    if isinstance(var, bytes):
        return var.decode('utf-8')
    return str(var)

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
            'low': Notify.Urgency.LOW,
            'normal': Notify.Urgency.NORMAL,
            'critical': Notify.Urgency.CRITICAL
            }
    priority = 'normal'
    title = _mydecode(kwargs['title'])
    message = _mydecode(kwargs['message'])
    icon = iconpng = GdkPixbuf.Pixbuf.new_from_file(kwargs['icon'])
    notification = Notify.Notification.new(title, message)
    notification.set_icon_from_pixbuf(icon)
    notification.set_urgency(priorities.get(priority))
    notification.show()
