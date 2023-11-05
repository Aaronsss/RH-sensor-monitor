'''Sensor Monitor'''

import logging
logger = logging.getLogger(__name__)
from eventmanager import Evt
from RHUI import UIField, UIFieldType

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
        logger.info("Battery cells detected: " + str(self.cellCount))

    def check_sensors(self, args):
        sensor_mon_enabled = self._rhapi.db.option("sensor_mon_enabled", "")

        if sensor_mon_enabled == '1':
            sensor_mon_group = self._rhapi.db.option("sensor_mon_group", "")
            sensor_mon_name = self._rhapi.db.option("sensor_mon_name", "")
            sensor_mon_warn_level = float(self._rhapi.db.option("sensor_mon_warn_level", 0))
            sensor_mon_alarm_level = float(self._rhapi.db.option("sensor_mon_alarm_level", 0))
            sensor_mon_cell_calc = self._rhapi.db.option("sensor_mon_cell_calc", "")

            try:
                Sensor_data = round(float(getattr(self._rhapi.sensors.sensor_obj(sensor_mon_group), sensor_mon_name)), 2)  
                
                if sensor_mon_cell_calc == '1':
                    Sensor_data = round(Sensor_data / self.cellCount, 2)

                if Sensor_data < sensor_mon_alarm_level:
                    self.send_message_alert(sensor_mon_group, sensor_mon_name, Sensor_data)
                elif Sensor_data < sensor_mon_warn_level:
                    self.send_message_warn(sensor_mon_group, sensor_mon_name, Sensor_data)
            except:
                logger.info("group: " + sensor_mon_group + " sensor: " + sensor_mon_name + " not recognised!")

    def discover_sensors(self, args):
        logger.info("Sensor monitor available groups and sensor")
        for x in self._rhapi.sensors.sensor_names:
            logger.info('-> Group name: '+ str(x))
            for y in vars(self._rhapi.sensors.sensor_obj(x)):
                if y.find("_") == 0:
                    logger.info("--> Sensor name: " + str(y) + " " + str(getattr(self._rhapi.sensors.sensor_obj(x), y)))
        self.calculate_cells(args)
    
    def register_handlers(self, args):
        print("handlers registered")

def initialize(rhapi):
    sensor_mon = sensor_monitor(rhapi)
    rhapi.events.on(Evt.ACTIONS_INITIALIZE, sensor_mon.register_handlers)
    rhapi.events.on(Evt.STARTUP, sensor_mon.discover_sensors)
    rhapi.events.on(Evt.LAPS_CLEAR, sensor_mon.check_sensors)    

    rhapi.ui.register_panel('sensor_monitor', 'Sensor Monitor', 'settings', order=0)
    rhapi.fields.register_option(UIField('sensor_mon_group', 'Sensor group', UIFieldType.TEXT), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_name', 'Sensor name', UIFieldType.TEXT), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_enabled', 'Enabled', UIFieldType.CHECKBOX), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_cell_calc', 'Use cell voltage', UIFieldType.CHECKBOX), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_warn_level', 'Warn level', UIFieldType.TEXT), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_alarm_level', 'Alarm level', UIFieldType.TEXT), 'sensor_monitor')