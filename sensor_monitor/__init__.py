'''Sensor Monitor'''

import logging
logger = logging.getLogger(__name__)
from dataclasses import dataclass, asdict 
from eventmanager import Evt
from EventActions import ActionEffect
from RHUI import UIField, UIFieldType, UIFieldSelectOption

@dataclass
class SensorInfo():
    group: str
    name: str
    txt: str

class sensor_monitor():
    cellCount = 100
    sensor_list = []

    def __init__(self, rhapi):
        self._rhapi = rhapi

    def send_message(self, sensor, value, updown, message_types):
        if message_types == 0 or message_types == 3:
            self._rhapi.ui.message_notify(sensor + " is " + updown + " the warning level and is currently: " + str(value))
        if message_types == 1 or message_types == 4:   
            self._rhapi.ui.message_alert(sensor + " is " + updown + " the alarm level and is currently: " + str(value))
        if message_types >= 2:
            self._rhapi.ui.message_speak("Alert " + sensor.replace("_", " ") + " is currently " + str(value))

    def calculate_cells(self, args, volts):
        if volts > 6 and volts <= 30:
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
        else:
            logger.info("[Sensor Monitor] Battery cells not calculated as voltage outside of 6-30V range")

    def check_sensors(self, action, args):
        sensor_info = self.sensor_list[int(action['sensors'])]
        try:
            Sensor_data = round(float(getattr(self._rhapi.sensors.sensor_obj(sensor_info.group), sensor_info.name)), 2)  
            if action['compare_type'] == '2' or action['compare_type'] == '3': # Use cell count 
                if self.cellCount == 100:
                    self.calculate_cells(args, Sensor_data)
                Sensor_data = round(Sensor_data / self.cellCount, 2)
            if action['compare_type'] == '0' or action['compare_type'] == '2': # less than 
                if Sensor_data < float(action['warn_value']):
                    self.send_message(sensor_info.txt, str(Sensor_data), "below", int(action['warn_type']))
            elif action['compare_type'] == '1' or action['compare_type'] == '3': # greater than 
                if Sensor_data > float(action['warn_value']):
                    self.send_message(sensor_info.txt, str(Sensor_data), "above", int(action['warn_type']))
        except:
            logger.info("[Sensor Monitor] " + sensor_info.txt + " not recognised!")

    def discover_sensors(self, args):
        self.sensor_list.clear()
        for x in self._rhapi.sensors.sensor_names:
            for y in vars(self._rhapi.sensors.sensor_obj(x)):
                if y.find("_") == 0:
                    self.sensor_list.append(SensorInfo(str(x), str(y), (str(x) + str(y))))
    
    def register_handlers(self, args):
        self.discover_sensors(args)
        sensor_options = []
        if not self.sensor_list:
            sensor_options.append(UIFieldSelectOption(0, "--- No Sensors Detected! ---"))
        for i, x in enumerate(self.sensor_list):
            sensor_options.append(UIFieldSelectOption(i, x.txt))
        if 'register_fn' in args:
            for effect in [
                ActionEffect(
                    'Sensor Monitor',
                    self.check_sensors,
                    [
                        UIField('sensors', "Sensor", UIFieldType.SELECT, options=sensor_options, value=0),
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