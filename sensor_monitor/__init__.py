'''Sensor Monitor'''

import logging
logger = logging.getLogger(__name__)
from eventmanager import Evt
from EventActions import ActionEffect
from RHUI import UIField, UIFieldType, UIFieldSelectOption

class sensor_monitor():
    cellCount = 100
    sensor_list = []

    def __init__(self, rhapi):
        self._rhapi = rhapi

    def send_message(self, group, sensor, value, updown, message_types):
        if message_types == 0 or message_types == 3:
            self._rhapi.ui.message_notify(group + " " + sensor[1:] + " is " + updown + " the warning level and is currently: " + str(value))
        if message_types == 1 or message_types == 4:   
            self._rhapi.ui.message_alert(group + " " + sensor[1:] + " is " + updown + " the alarm level and is currently: " + str(value))
        if message_types >= 2:
            self._rhapi.ui.message_speak(group + " " + sensor[1:] + " is currently " + str(value))

    def calculate_cells(self, args, group, name):
        try:
            volts = float(getattr(self._rhapi.sensors.sensor_obj(group), name))
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
            logger.info("[Sensor Monitor] Battery cells detected: " + str(self.cellCount))
        except:
            logger.info("[Sensor Monitor] Failed to detect the cell count of the sensor")

    def check_sensors(self, action, args):
        try:
            Sensor_data = round(float(getattr(self._rhapi.sensors.sensor_obj(action['group']), action['name'])), 2)  
        #Sensor_data = float(action['group'])
            if action['compare_type'] == '2' or action['compare_type'] == '3':
                if self.cellCount == 100:
                    self.calculate_cells(args, action['group'], action['name'])
                Sensor_data = round(Sensor_data / self.cellCount, 2)
            if action['compare_type'] == '0' or action['compare_type'] == '2':
                if Sensor_data < float(action['warn_value']):
                    self.send_message(action['group'], action['name'], str(Sensor_data), "below", int(action['warn_type']))
            elif action['compare_type'] == '1' or action['compare_type'] == '3':
                if Sensor_data > float(action['warn_value']):
                    self.send_message(action['group'], action['name'], str(Sensor_data), "above", int(action['warn_type']))
        except:
            logger.info("[Sensor Monitor] " + action['group'] + action['name'] + " not recognised!")

    def discover_sensors(self, args):
        self.sensor_list.clear()
        logger.info("[Sensor Monitor] Available groups and sensor")
        for x in self._rhapi.sensors.sensor_names:
            logger.info('[Sensor Monitor] -> Group name: '+ str(x))
            for y in vars(self._rhapi.sensors.sensor_obj(x)):
                if y.find("_") == 0:
                    logger.info("[Sensor Monitor] --> Sensor name: " + str(y) + " " + str(getattr(self._rhapi.sensors.sensor_obj(x), y)))
                    self.sensor_list.append((str(x) + str(y)))
        for x in self.sensor_list:
            print("[Sensor Monitor] " + x) 
    
    def register_handlers(self, args):
        self.discover_sensors(args)
        if 'register_fn' in args:
            for effect in [
                ActionEffect(
                    'Sensor Monitor',
                    self.check_sensors,
                    [
                        UIField('group', "Sensor Group", UIFieldType.TEXT),
                        UIField('name', "Sensor Name", UIFieldType.TEXT),
                        UIField('warn_type', "Warning Type", UIFieldType.SELECT, options=[
                            UIFieldSelectOption(0, "Message Only"),
                            UIFieldSelectOption(1, "Alert Only"),
                            UIFieldSelectOption(2, "Voice Call Out Only"),
                            UIFieldSelectOption(3, "Message and Voice Call Out"),
                            UIFieldSelectOption(4, "Alert and Voice Call Out"),
                        ], value=0),
                        UIField('compare_type', "Compare Type", UIFieldType.SELECT, options=[
                            UIFieldSelectOption(0, "Less than"),
                            UIFieldSelectOption(1, "Greater than"),
                            UIFieldSelectOption(2, "Less than per cell voltage"),
                            UIFieldSelectOption(3, "Greater than per cell voltage"),
                        ], value=0),
                        UIField('warn_value', "Sensor Warning Level", UIFieldType.TEXT),
                    ]
                )
            ]:
                args['register_fn'](effect)

def initialize(rhapi):
    sensor_mon = sensor_monitor(rhapi)
    rhapi.events.on(Evt.ACTIONS_INITIALIZE, sensor_mon.register_handlers)
    #rhapi.events.on(Evt.STARTUP, sensor_mon.discover_sensors)