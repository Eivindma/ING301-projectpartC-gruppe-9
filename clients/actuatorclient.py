import time
import requests

import logging
log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

import common

LIGHTBULB_CLIENT_SLEEP_TIME = 4

class ActuatorClient:
    """
    Actuator client representing the physical light bulb in the house
    using the cloud service to set is state
    """

    def __init__(self, did):
        self.did = did
        self.state = common.ActuatorState('off')

    def get_state(self) -> str:

        """
        This method sends a GET request to the cloud service to
        read/obtain the current state of the light bulb actuator.
        """

        logging.info(f"Actuator Client {self.did} retrieving state")
        actuator_state = None

        # TODO
        url = common.BASE_URL + f"actuator/{self.did}/state"
        response = requests.get(url)
        actuator_state = common.ActuatorState.from_json_str(response.text)
        return actuator_state.state


    def run(self):
        """
        This method runs in a loop reguarly sending a request to the cloud service
        to set the current state of the light bulb in accordance with the state
        in the cloud service
        """

        # TODO
        while True:
            state = self.get_state()
            if state:
                self.state.set_state(state)
                logging.info(f"Actuator {self.did} state: {self.state.state}")
            time.sleep(LIGHTBULB_CLIENT_SLEEP_TIME)
            
            
if __name__ == '__main__':

    actuator = ActuatorClient(common.LIGHT_BULB_ACTUATOR_DID)
    actuator.run()