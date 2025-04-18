# RH-sensor-monitor
This plugin for [RotorHazard](https://github.com/RotorHazard/RotorHazard) lets you set up a warning on any sensors that is installed within RotorHazard

# How to Install
There are 3 ways you can install this plugin
1. Though RotorHazards community plugin manager on RotorHazard 4.3.0 or greater:  
   This can be found on your timer which must be connected to the internet by going to settings -> plugins -> Browse Community Plugins (online only) -> Utilities then install the Sensor Monitor plugin
   
2. Run the following command in the SSH terminal to install the sensor monitor 
  ```
  cd ~
  wget https://github.com/Aaronsss/RH-sensor-monitor/archive/refs/heads/main.zip
  unzip ./main.zip
  rm -R ~/RotorHazard/src/server/plugins/sensor_monitor
  mv ~/RH-sensor-monitor-main/custom_plugins/sensor_monitor/ ~/RotorHazard/src/server/plugins/
  rm -R ./RH-sensor-monitor-main/
  rm ./main.zip
  sudo systemctl restart rotorhazard.service
  ```
3. Manually:   
  If you wish to install manually, place the custom_plugins/sensor_monitor folder within the RotorHazard plugins folder Rotorhazard/src/server/plugins then start / restart the server  

# How to setup

> [!IMPORTANT]
> You must setup an Event Action correctly for this plugin to do anything.  

> [!IMPORTANT]
> The sensor is only checked when the race event happens, so a timer that is sitting there not being used will not check the battery voltage for example  

Go to Settings -> Event Actions tab and add click Add Action
1. Sensor - the group and name of the sensor you want to monitor
2. Warning Type - Select between messages, warning pop ups or voice call outs (or a combination of those things)
3. Compare Type - Select between less than or greater than. You can also use the calculated battery cell voltage if you wish
4. Sensor Warning Level - The threshold value to use to check with

An example setup to check battery voltage at the end of the race can be seen below:
![example setup](./img/example_setup.png)
