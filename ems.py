import requests
import logging
from time import sleep
from threading import Thread



class Boiler:

    def __init__(self, uri: str):
        self.uri = uri
        self.selected_flow_temperature = -1
        self.current_flow_temperature = -1
        self.heating_active = False
        self.dhw_selected_temp = -1        # domestic hot water
        self.dhw_set_temp = -1
        self.dhw_storage_temp = -1
        self.dhw_active = False
        self.dhw_activated = False
        Thread(target=self.__run_loop, daemon=True).start()

    def set_listener(self, listener):
        self.__listener = listener

    def __notify_listener(self):
        self.__listener()

    def __run_loop(self):
        while True:
            try:
                self.__fetch_data()
            except Exception as e:
                logging.warning(str(e))
            sleep(3)

    def __fetch_data(self):
        resp = requests.get(self.uri)
        data = resp.json()
        self.selected_flow_temperature = data['selflowtemp']
        self.current_flow_temperature = data['curflowtemp']
        self.heating_active = data['heatingactive']
        self.dhw_selected_temp = data['dhw']['settemp']
        self.dhw_set_temp = data['dhw']['seltemp']
        self.dhw_storage_temp = data['dhw']['storagetemp2']
        self.dhw_active = data['dhw']['active']
        self.dhw_activated = data['dhw']['activated']
        self.__notify_listener()


    def set_selected_flow_temperature(self, temp: float):
        # todo
        self.__notify_listener()


    def set_dhw_selected_temp(self, temp: float):
        # todo
        self.__notify_listener()

    def set_dhw_activated(self, on: bool):
        # todo
        self.__notify_listener()

'''
http://192.168.1.82/api/boiler


https://docs.emsesp.org/Commands/

https://docs.emsesp.org/tips-and-tricks/#controlling-the

'''