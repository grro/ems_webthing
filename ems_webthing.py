import sys
import logging
import tornado.ioloop
from webthing import (MultipleThings, Property, Thing, Value, WebThingServer)
from ems import Boiler



class BoilerThing(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, boiler: Boiler):
        Thing.__init__(
            self,
            'urn:dev:ops:boilerSensor-1',
            'Boiler',
            ['MultiLevelSensor'],
            "boiler sensor"
        )

        self.boiler = boiler
        self.boiler.set_listener(self.on_value_changed)
        self.ioloop = tornado.ioloop.IOLoop.current()

        self.current_flow_temperature = Value(self.boiler.current_flow_temperature)
        self.add_property(
            Property(self,
                     'current_flow_temperature',
                     self.current_flow_temperature,
                     metadata={
                         'title': 'current_flow_temperature',
                         'type': 'number',
                         'description': 'The current flow temperature',
                         'readOnly': True,
                     }))

        self.selected_flow_temperature = Value(self.boiler.selected_flow_temperature, self.boiler.set_selected_flow_temperature)
        self.add_property(
            Property(self,
                     'selected_flow_temperature',
                     self.selected_flow_temperature,
                     metadata={
                         'title': 'selected_flow_temperature',
                         'type': 'number',
                         'description': 'The selected flow temperature',
                         'readOnly': False,
                     }))

        self.heating_active = Value(self.boiler.heating_active)
        self.add_property(
            Property(self,
                     'heating_active',
                     self.heating_active,
                     metadata={
                         'title': 'heating_active',
                         'type': 'boolean',
                         'description': 'True, if the heating is currently active',
                         'readOnly': True,
                     }))


        self.selected_flow_temperature = Value(self.boiler.selected_flow_temperature, self.boiler.set_selected_flow_temperature)
        self.add_property(
            Property(self,
                     'selected_flow_temperature',
                     self.selected_flow_temperature,
                     metadata={
                         'title': 'selected_flow_temperature',
                         'type': 'number',
                         'description': 'The selected flow temperature',
                         'readOnly': False,
                     }))

        self.dhw_selected_temp = Value(self.boiler.dhw_selected_temp, self.boiler.set_dhw_selected_temp)
        self.add_property(
            Property(self,
                     'dhw_selected_temp',
                     self.dhw_selected_temp,
                     metadata={
                         'title': 'dhw_selected_temp',
                         'type': 'number',
                         'description': 'The selected domestic hot water',
                         'readOnly': False,
                     }))

        self.dhw_set_temp = Value(self.boiler.dhw_set_temp)
        self.add_property(
            Property(self,
                     'dhw_set_temp',
                     self.dhw_set_temp,
                     metadata={
                         'title': 'dhw_set_temp',
                         'type': 'number',
                         'description': 'The set domestic hot water',
                         'readOnly': True,
                     }))

        self.dhw_active = Value(self.boiler.dhw_active)
        self.add_property(
            Property(self,
                     'dhw_active',
                     self.dhw_active,
                     metadata={
                         'title': 'dhw_active',
                         'type': 'boolean',
                         'description': 'True, if the domestic hot water is currently active',
                         'readOnly': True,
                     }))

        self.dhw_activated = Value(self.boiler.dhw_activated, self.boiler.set_dhw_activated)
        self.add_property(
            Property(self,
                     'dhw_activated',
                     self.dhw_activated,
                     metadata={
                         'title': 'dhw_activated',
                         'type': 'boolean',
                         'description': 'True, if the domestic hot water is actived',
                         'readOnly': False,
                     }))

    def on_value_changed(self):
        self.ioloop.add_callback(self.__on_value_changed)

    def __on_value_changed(self):
        self.selected_flow_temperature.notify_of_external_update(self.boiler.selected_flow_temperature)
        self.current_flow_temperature.notify_of_external_update(self.boiler.current_flow_temperature)
        self.heating_active.notify_of_external_update(self.boiler.heating_active)
        self.dhw_set_temp.notify_of_external_update(self.boiler.dhw_set_temp)
        self.dhw_selected_temp.notify_of_external_update(self.boiler.dhw_selected_temp)
        self.dhw_activated.notify_of_external_update(self.boiler.dhw_activated)
        self.dhw_active.notify_of_external_update(self.boiler.dhw_active)


def run_server(port: int, ems_uri: str):
    ems_uri = ems_uri.strip()
    if not ems_uri.endswith("/"):
        ems_uri = ems_uri + '/'

    boiler = BoilerThing(Boiler(ems_uri + "api/boiler"))
    server = WebThingServer(MultipleThings([boiler], 'ems_devices'), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server http://localhost:' + str(port) + " (ems=" + ems_uri + ")")
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    try:
        logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        logging.getLogger('tornado.access').setLevel(logging.ERROR)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
        run_server(int(sys.argv[1]), sys.argv[2])
    except Exception as e:
        logging.error(str(e))
        raise e
