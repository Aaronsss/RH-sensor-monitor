# RH-sensor-monitor
This plugin for RotorHazard lets you set up a warning and an alarm on any sensor that is installed within RotorHazard

# How to setup
Place the sensor_monitor folder within the RotorHazard plugins folder Rotorhazard/src/server/plugins

Start / restart the server and go the the server log (Settings -> System > Server Log)

Within the server log you will see something like this:
'''
2023-11-04 23:25:23.601: plugins.sensor_monitor [INFO] Sensor monitor available groups and sensor
2023-11-04 23:25:23.601: plugins.sensor_monitor [INFO] -> Group name: Battery
2023-11-04 23:25:23.602: plugins.sensor_monitor [INFO] --> Sensor name: _voltage 22.592
2023-11-04 23:25:23.602: plugins.sensor_monitor [INFO] --> Sensor name: _current 386.98170731707313
2023-11-04 23:25:23.602: plugins.sensor_monitor [INFO] --> Sensor name: _power 9327.134146341463
2023-11-04 23:25:23.602: plugins.sensor_monitor [INFO] -> Group name: Core
2023-11-04 23:25:23.602: plugins.sensor_monitor [INFO] --> Sensor name: _temp 41.318
2023-11-04 23:25:23.602: plugins.sensor_monitor [INFO] Battery cells detected: 6
'''

You will need to note down the group name and the sensor name of the sensor you want to setup a warning on e.g. to monitor the 22.592 value you would choose Battery and _voltage

Next go to the Settings -> Sensor Monitor options and fill out the information, the options are as follows:
1. Sensor group - the group name of the sensor you want to monitor
2. Sensor name - the sensor name of the sensor you want to monitor
3. Enabled - enables or disabled warnings and notifications
4. Use cell voltage - Selecting this divides the sensor value by the calculated LiPo cell voltage at boot up
5. Warn level - the level at which a server message is sent
6. Alarm level - the level at which a server pop up and audible announcement happens

An example setup can be seen below:
![example setup](./img/example_setup.png)
