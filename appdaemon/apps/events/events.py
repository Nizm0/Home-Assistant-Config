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
    self.log(f"Push notification closed: {event_tag}, {data}")

  def chose_action_event_received(self, event_name, data, kwargs):
    event_tag = data["tag"]
    self.log(f"Push notification received: {event_tag}, {data}")

  def chose_action_event_clicked(self, event_name, data, kwargs):
    event_action = data["action"]
    event_tag = data["tag"]
    # self.log("Push notification clicked (action) {event_action}")
    if event_action == "open_door":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.light_on(self)
      self.run_in(self.light_off, 10)
    elif event_action == "open":
      self.log(f"Push notification clicked {event_action}, {data}")
    elif event_action == "start_vacuum":
      self.log(f"Push notification clicked {event_action}, {data}")
      VacuumActions.start_vacuum(self, kwargs)
    elif event_action == "stop_vacuum":
      self.log(f"Push notification clicked {event_action}, {data}")
      VacuumActions.stop_vacuum(self, kwargs)
    elif event_action == "return_vacuum":
      self.log(f"Push notification clicked {event_action}, {data}")
      VacuumActions.dock_vacuum(self, kwargs)
    elif event_action == "cancel":
      self.log(f"Push notification clicked {event_action}, {data}")
      VacuumActions.cancel_vacuum_timer()
      self.dismiss_by_tag(event_tag)
    elif event_action == "pospone":
      self.log(f"Push notification clicked {event_action}, {data}")
      VacuumActions.postpone_vacuum_timer(3600)
    # switcher={
    #   "open_door":light_on
    # }
    # func = switcher.get(action, lambda :"Invalid")
    # return func()

  def dismiss_by_tag(self, tag):
    self.call_service("notify.html5_dismiss", data={"tag": tag})