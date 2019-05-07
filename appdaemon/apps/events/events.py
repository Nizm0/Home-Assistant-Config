import appdaemon.plugins.hass.hassapi as hass

from datetime import datetime, timedelta

class Events(hass.Hass):

# html5_notification.clicked
  def initialize(self):
    self.listen_event(self.chose_action, "html5_notification.clicked", action = "open_door")

  # def generic_event(self, event_name, data, kwargs):
  #   event_action = data["action"]
  #   event_target = data["target"]
  #   event_received = datetime.now()
  #   self.log("You have pushed {}. From device: {}".format(event_action, event_target))
  #   self.turn_on("light.bedroom_main_light")
  #   self.run_in(self.light_off, 10)

  def light_on(self, kwargs):
    self.turn_on("light.bedroom_main_light")

  def light_off(self, kwargs):
    self.turn_off("light.bedroom_main_light")

  def chose_action(self, event_name, data, kwargs):
    event_action = data["action"]
    if event_action == "open_door":
      self.log("Push notification clicked {}".format(event_action))
      self.light_on(self)
      self.run_in(self.light_off, 10)
    elif event_action == "open":
      self.log("Push notification clicked {}".format(event_action))
    # switcher={
    #   "open_door":light_on
    # }
    # func = switcher.get(action, lambda :"Invalid")
    # return func()