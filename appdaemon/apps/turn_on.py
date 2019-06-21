import appdaemon.plugins.hass.hassapi as hass

## Turns on something when something else happens

class TurnOn(hass.Hass):

    def initialize(self):
    
        self.handle = None
    
    # Check some Params

    # Subscribe to sensors
        if "sensor" in self.args:
            for sensor in self.split_device_list(self.args["sensor"]):
                self.listen_state(self.action, sensor)
        else:
            self.log("No sensor specified, doing nothing")

    def action(self, entity, attribute, old, new, kwargs)
        if new == 'on'
            self.log("Turning on: {}".format(sensor))
            self.turn_on(self.args["action"])