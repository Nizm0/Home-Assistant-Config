import appdaemon.plugins.hass.hassapi as hass

from datetime import datetime, timedelta

class Events(hass.Hass):

# html5_notification.clicked
  def initialize(self):
    self.listen_event(self.generic_event, "html5_notification.clicked", action = "open_door")

  def generic_event(self, event_name, data, kwargs):
    event_action = data["action"]
    event_target = data["target"]
    event_received = datetime.now()
    self.log("You have pushed {}. From device: {}".format(event_action, event_target))
    self.turn_on("light.bedroom_main_light")
    self.run_in(self.light_off, 10)

  def light_on(self, entity, attribute, old, new, kwargs):
    self.turn_on("light.bedroom_main_light")

  def light_off(self, entity, attribute, old, new, kwargs):
    self.turn_off("light.bedroom_main_light")

  # def chose_action(self, action, i):
  #   switcher={
  #     "open_door":light_on
  #   }
  #   func = switcher.get(action, lambda :"Invalid")
  #   return func()