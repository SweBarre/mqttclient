![icon_running](https://user-images.githubusercontent.com/254416/41272012-bdb5ace2-6e13-11e8-846b-4e509a6b3e48.png)
# MQTTClient
This is my simple client that I use to connect to my mqtt client at home to get notifications on events and publishing commands remote.


## Configuration
The configuration file for the application is located at *~/.mqttclient.yaml*. When you launch the client for the first time you get the option to copy the default_mqttclient.yaml as a base for your configuration. The configuration file is a standard [yaml file](http://yaml.org)
The configuration file has the following sections

### mqtt
this is where you configure the connection options for your MQTT server 
```yaml
mqtt:
  host: localhost
  port: 1883
  use_tls: true
  user: username
  password: secret
  timeout_reconnect: 60
  logger: mqttclient
  ca_file: /etc/ssl/ca-bundle.pem
  connect_on_launch: true
  subscriptions:
    - name: irssi
      subscribe: true
      topic: irssi
      plugins:
        - irssi
    - name: test
      subscribe: true
      topic: test
      plugins:
        - notify
```
The `connect_on_launch` specifies if mqttclient should connect to mqtt server automaticly when you launch the application or not. Under `subscription` you specify the topics you want the application to subscribe to and supports wildcards. 
For example, `myhome/floor1/temperature/#` would subscribe to all topics under _myhome/floor1/temperature_ while `myhome/+/lights/#` would subscribe to all topics under _lights_ on all _floors_.
the _plugins_ list specifies all plugins that should be executed when a topic is updated

### plugin
Here you can override the plugins default configuration, for example setting the priority on notifcation for the irssi plugin from de default Notify.Urgency.NORMAL to Notify.Urgency.CRITICAL
```yaml
plugin:
  irssi:
    urgency: critical
```
### publish
This section configures the publish menu when you right click on the application indicator
![right_click_menu](https://user-images.githubusercontent.com/254416/41272005-b3cb7090-6e13-11e8-8121-a49f230b82a9.png)
```yaml
publish:
  - name: test 1
    topic: test
    payload: hejsan svejsan
    retain: false
  - name: test 2
    topic: test2/testing
    payload: kalle kalas
    retain: false
  - name: sub meny name
    menu:
      - name: test 3
        topic: test
        payload: from submenu
        retain: false
```
### logging
Configures the application logging, one or several logging destinations can be configuring and it's using the [logging.config.dictConfig](https://docs.python.org/2/library/logging.config.html) function

## Plugin system
It's not much of a pluggin system, it's rough and ugly but anyways...
The __plugin__ should be put in the plugins subdirectory and the name of the directory will be the plugin name and the \_\_init\_\_.py in that directory will be called, eg `plugins/myplugin/__init__.py`
When the application is launched it goes through all subscriptions in the mqtt section of the configuration file and checks for all plugins specified there. If the plugin configured in the configuration file and is present in the filesystem the plugin will be loaded.

One method is mandatory in the plugin and that's the **prep** method
example for the notify plugin
```python
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
```

When a topic that the application is subscribing to is updated the mqttclient will go though the plugin list defined for that topic and call the prep method with msg as parameter.
msg.topic contains the topic thats been updated
msg.payload contains the value thats been updated
the prep should return a dictionary that will be used for the next step in the plugin, the method **run**

The *run* method is not mandatory, if the *prep* method is returning a _runner_ key that contains the name of a plugin then that plugins run method will be used.
the irssi plugin uses the notify run method

Here's a example of notify plugin beeing used:

![notify](https://user-images.githubusercontent.com/254416/41271999-ae43a20a-6e13-11e8-8407-eab1d999a2ee.png)

And here's a example of irssi plugin beeing used, using the notify runner


![irssi](https://user-images.githubusercontent.com/254416/41274984-b25891dc-6e1f-11e8-814b-d8e7a1890a15.png)
