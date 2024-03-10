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

    def send_message(self, group, sensor, value, updown, message_types):
        if message_types == 0 or message_types == 3:
            self._rhapi.ui.message_notify(group + " " + sensor[1:] + " is " + updown + " the warning level and is currently: " + str(value))
        if message_types == 1 or message_types == 4:   
            self._rhapi.ui.message_alert(group + " " + sensor[1:] + " is " + updown + " the alarm level and is currently: " + str(value))
        if message_types >= 2:
            self._rhapi.ui.message_speak(group + " " + sensor[1:] + " is currently " + str(value))

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

    def check_sensors(self, action, args):
        try:
            Sensor_data = round(float(getattr(self._rhapi.sensors.sensor_obj(action['group']), action['name'])), 2)  
            
            if action['compare_type'] == '2' or action['compare_type'] == '3':
                Sensor_data = round(Sensor_data / self.cellCount, 2)
            if action['compare_type'] == '0' or action['compare_type'] == '2':
                if Sensor_data < action['warn_value']:
                    self.send_message_alert(action['group'], action['name'], Sensor_data, "below", int(action['warn_type']))
            elif action['compare_type'] == '1' or action['compare_type'] == '3':
                if Sensor_data > action['warn_value']:
                    self.send_message_alert(action['group'], action['name'], Sensor_data, "above", int(action['warn_type']))
        except:
            logger.info("group: " + action['group'] + " sensor: " + action['name'] + " not recognised!")

    def discover_sensors(self, args):
        logger.info("Sensor monitor available groups and sensor")
        for x in self._rhapi.sensors.sensor_names:
            logger.info('-> Group name: '+ str(x))
            for y in vars(self._rhapi.sensors.sensor_obj(x)):
                if y.find("_") == 0:
                    logger.info("--> Sensor name: " + str(y) + " " + str(getattr(self._rhapi.sensors.sensor_obj(x), y)))
        self.calculate_cells(args)
    
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
                        UIField('warn_type', "Type of Warning", UIFieldType.SELECT, options=[
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