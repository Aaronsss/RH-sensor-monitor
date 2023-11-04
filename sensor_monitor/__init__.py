'''Sensor Monitor'''

import logging
logger = logging.getLogger(__name__)
from eventmanager import Evt
from EventActions import ActionEffect
from RHUI import UIField, UIFieldType, UIFieldSelectOption

class sensor_monitor():
    cellCount = 6

    def __init__(self, rhapi):
        self._rhapi = rhapi

    def send_message_warn(self, group, sensor, value):
        self._rhapi.ui.message_notify(group + " " + sensor[1:] + " is below the warning level and is currently: " + str(value))

    def send_message_alert(self, group, sensor, value):
        self._rhapi.ui.message_speak(group + " " + sensor[1:] + " is currently " + str(value))
        self._rhapi.ui.message_alert(group + " " + sensor[1:] + " is below the alarm level and is currently: " + str(value))
    
    def calculate_cells(self, args):
        try:
            sensor_mon_group = self._rhapi.db.option("sensor_mon_group", "")
            sensor_mon_name = self._rhapi.db.option("sensor_mon_name", "")
            volts = float(getattr(self._rhapi.sensors.sensor_obj(sensor_mon_group), sensor_mon_name))
        except:
            volts = 0

        if volts > 21:
            self.cellCount = 6
        elif volts >= 17:
            self.cellCount = 5
        elif volts >= 12.8:
            self.cellCount = 4
        elif volts >= 9.2:
            self.cellCount = 3
        else:
            self.cellCount = 2
        print("Battery cells detected:", self.cellCount)

    def check_sensors(self, args):
        sensor_mon_enabled = bool(self._rhapi.db.option("sensor_mon_enabled", ""))

        if sensor_mon_enabled:
            sensor_mon_group = self._rhapi.db.option("sensor_mon_group", "")
            sensor_mon_name = self._rhapi.db.option("sensor_mon_name", "")
            sensor_mon_warn_level = float(self._rhapi.db.option("sensor_mon_warn_level", 0))
            sensor_mon_alarm_level = float(self._rhapi.db.option("sensor_mon_alarm_level", 0))

            print(sensor_mon_group, " ", sensor_mon_name, " ", sensor_mon_enabled, " ", str(sensor_mon_warn_level), " ", str(sensor_mon_alarm_level))
            print("cell count:", self.cellCount)

            try:
                Sensor_data = float(getattr(self._rhapi.sensors.sensor_obj(sensor_mon_group), sensor_mon_name))            
                if Sensor_data < sensor_mon_alarm_level:
                    self.send_message_alert(sensor_mon_group, sensor_mon_name, Sensor_data)
                elif Sensor_data < sensor_mon_warn_level:
                    self.send_message_warn(sensor_mon_group, sensor_mon_name, Sensor_data)
            except:
                print("unable to find sensor data")

    def discover_sensors(self, args):
        print("Sensor monitor available groups and sensor")
        for x in self._rhapi.sensors.sensor_names:
            print('-> Group name:', x)
            for y in vars(self._rhapi.sensors.sensor_obj(x)):
                if y.find("_") == 0:
                    print("--> Sensor name:", y, getattr(self._rhapi.sensors.sensor_obj(x), y))
                    #print('  ', getattr(self._rhapi.sensors.sensor_obj(x), y))
        self.calculate_cells(args)
    
    def register_handlers(self, args):
        print("handlers registered")

def initialize(rhapi):
    sensor_mon = sensor_monitor(rhapi)
    rhapi.events.on(Evt.ACTIONS_INITIALIZE, sensor_mon.register_handlers)
    rhapi.events.on(Evt.STARTUP, sensor_mon.discover_sensors)
    rhapi.events.on(Evt.RACE_STOP, sensor_mon.check_sensors)    

    rhapi.ui.register_panel('sensor_monitor', 'Sensor Monitor', 'settings', order=0)
    rhapi.fields.register_option(UIField('sensor_mon_group', 'Sensor group', UIFieldType.TEXT), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_name', 'Sensor name', UIFieldType.TEXT), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_enabled', 'Enabled', UIFieldType.CHECKBOX, 1), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_cell_calc', 'Calculate Battery Cells', UIFieldType.CHECKBOX, 1), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_warn_level', 'Warn level', UIFieldType.TEXT), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_alarm_level', 'Alarm level', UIFieldType.TEXT), 'sensor_monitor')

#    rhapi.fields.register_option(UIField('sensor_mon_name', "Sensor name", UIFieldType.SELECT, options=[UIFieldSelectOption(0, "No action"), UIFieldSelectOption(1, "Connect to OBS if not already connected")], value=0), 'sensor_monitor')

        #self.send_message_alert("test sensor", 3.72)

        # x = self._rhapi.sensors.sensor_obj('Battery')
        # print('# vars', vars(x))
        # print('# Voltage', getattr(x, '_voltage'))
        # print('# Current', getattr(x, '_current'))
        # print('# Power', getattr(x, '_power'))


            
        #print('# vars', vars(y))
        # print('# Temp', getattr(y, '_temp'))

        # for x in self._rhapi.sensors.sensor_names:
        #     print(x)
        #     for y in vars(self._rhapi.sensors.sensor_obj(x)):
        #         if y.find("_") == 0:
        #             print(" ", y)
        #             print('  ', getattr(self._rhapi.sensors.sensor_obj(x), y))
        #print('# vars', dir(y))
        #print('# Temp', getattr(y, '_temp'))
  