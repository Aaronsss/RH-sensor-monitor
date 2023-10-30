'''Sensor Monitor'''

import logging
logger = logging.getLogger(__name__)
from eventmanager import Evt
from EventActions import ActionEffect
from RHUI import UIField, UIFieldType, UIFieldSelectOption

from Results import RacePointsMethod


class sensor_monitor():
    def __init__(self, rhapi):
        self._rhapi = rhapi

    def send_message_warn(self, sensor, value):
        self._rhapi.ui.message_notify(sensor + "is below the warning level of" + str(value))

    def send_message_alert(self, sensor, value):
        self._rhapi.ui.message_speak(sensor + "is below the alarm level of" + str(value))
        self._rhapi.ui.message_alert(sensor + "is below the alarm level of" + str(value))

    def check_sensors(self, args):
        #self.send_message_alert("test sensor", 3.72)
        for x in self._rhapi.sensors.sensors_dict:
            print(x)

    
    def register_handlers(self, args):
        print("handlers registered")
        # args['register_fn'](
        #         RacePointsMethod(
        #             "Position",
        #             points_by_position,
        #             None,
        #             [
        #                 UIField('points_list', "Points (CSV)", UIFieldType.TEXT, placeholder="10,6,3,1"),
        #             ]
        #         )
        #     )

def initialize(rhapi):
    sensor_mon = sensor_monitor(rhapi)
    rhapi.events.on(Evt.ACTIONS_INITIALIZE, sensor_mon.register_handlers)
    rhapi.events.on(Evt.LAPS_CLEAR, sensor_mon.check_sensors)

    rhapi.ui.register_panel('sensor_monitor', 'Sensor Monitor', 'settings', order=0)

    rhapi.fields.register_option(UIField('sensor_mon_name', 'Sensor name', UIFieldType.TEXT), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_warn', 'Warning enabled', UIFieldType.CHECKBOX, 1), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_warn_level', 'Warning level', UIFieldType.BASIC_INT), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_alarm', 'Alarm enabled', UIFieldType.CHECKBOX, 1), 'sensor_monitor')
    rhapi.fields.register_option(UIField('sensor_mon_alarm_level', 'Alarm level', UIFieldType.BASIC_INT), 'sensor_monitor')
  