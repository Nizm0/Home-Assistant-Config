import appdaemon.plugins.hass.hassapi as hass
from vacuum import VacuumActions
from base import Base

from datetime import datetime, timedelta

class Events(Base):

# html5_notification.clicked
  def initialize(self):
    self.listen_event(self.chose_action_event_closed, "html5_notification.closed") #, action = "open_door"
    self.listen_event(self.chose_action_event_received, "html5_notification.received") #, action = "open_door"
    self.listen_event(self.chose_action_event_clicked, "html5_notification.clicked") #, action = "open_door"
    # self.log("Push notification clicked {}".format(event_action))

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

  def chose_action_event_closed(self, event_name, data, kwargs):
    event_tag = data["tag"]
    self.log("Push notification closed: {}".format(event_tag))

  def chose_action_event_received(self, event_name, data, kwargs):
    event_tag = data["tag"]
    self.log("Push notification received: {}".format(event_tag))

  def chose_action_event_clicked(self, event_name, data, kwargs):
    event_action = data["action"]
    # self.log("Push notification clicked (action) {event_action}")
    if event_action == "open_door":
      self.log("Push notification clicked {}".format(event_action))
      self.light_on(self)
      self.run_in(self.light_off, 10)
    elif event_action == "open":
      self.log("Push notification clicked {}".format(event_action))
    elif event_action == "start_vacuum":
      self.log("Push notification clicked {}".format(event_action))
      VacuumActions.start_vacuum(self, kwargs)
    elif event_action == "stop_vacuum":
      self.log("Push notification clicked {}".format(event_action))
      VacuumActions.stop_vacuum(self, kwargs)
    elif event_action == "cancel":
      self.log("Push notification clicked {}".format(event_action))
      VacuumActions.cancel_timer(self)
    # switcher={
    #   "open_door":light_on
    # }
    # func = switcher.get(action, lambda :"Invalid")
    # return func()