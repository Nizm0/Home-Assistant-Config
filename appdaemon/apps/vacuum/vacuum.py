import appdaemon.plugins.hass.hassapi as hass
import datetime
from base import Base
import globals
from globals import HouseModes, PEOPLE
# from datetime import time, timedelta, tzinfo
# from datetime import time

class VacuumActions(Base):


  def initialize(self):
    # input_time = datetime.time.fromisoformat(self.get_state("input_datetime.vacuum_day_time"))
    # input_time = datetime.time(15, 00)
    # Schedule a daily callback that will call run_daily()
    self.counter = 0
    self.notify = ["notify/push_to_chrome_nizm0_oneplus3"]
    self.set_vacuum_timer(self, "input_datetime.vacuum_day_time", '', self.get_state("input_datetime.vacuum_day_time"), '')
    self.listen_state(self.change_vacuum_timer, "input_datetime.vacuum_day_time")
    self.listen_state(self.vacuum_state_handle, "vacuum.rockrobo")

  def set_vacuum_timer(self, entity, attribute, old, new, kwargs):
    self.input_time = datetime.time.fromisoformat(new)
    self.vacuum_daily = self.run_daily(self.run_daily_callback, self.input_time)
    self.counter = self.counter + 1
    self.log("Reinitialize run daily for {} time with {}".format(self.counter ,self.input_time))

  def change_vacuum_timer(self, entity, attribute, old, new, kwargs):
    self.cancel_timer(self.vacuum_daily)
    self.log("Cancel previous timer at {}".format(old))
    self.set_vacuum_timer(self, "input_datetime.vacuum_day_time", '', new, '')

  def vacuum_state_handle(self, entity, attribute, old, new, kwargs):
    if (old != new):
      title = "Roborock"
      if new == "error":
        self.log("Vacuum new state: {}".format(new))
      elif new == "cleaning":
        self.log("Vacuum new state: {}".format(new))
        message = "Vacuum has started and now is {} is it intended?".format(new)
        notify_on_start(self, title, self.notify, message)
      elif new == "docked":
        self.log("Vacuum new state: {}".format(new))
      elif new == "error":
        self.log("Vacuum new state: {}".format(new))
      elif new == "idle":
        self.log("Vacuum new state: {}".format(new))
      elif new == "pause":
        self.log("Vacuum new state: {}".format(new))
      elif new == "returning":
        self.log("Vacuum new state: {}".format(new))
      else:
        self.log("Vacuum new state: {}".format(new))

  # Our callback function will be called by the scheduler every day
  def run_daily_callback(self, kwargs):
    self.log("Run daily vacuum")
    ready = self.get_state("input_boolean.ready_to_vacuum")
    ocupancy = self.get_state("group.all_devices")
    home_preset = self.get_state("input_select.home_preset")
    title = "Roborock"
    message = ""
    # notify = ["notify/push_to_chrome_nizm0_oneplus3"]

    if self.get_state("vacuum.rockrobo") in ["docked", "idle", "pause"]:
      if ready != "on":
        message = "Flor is not ready to cleanup? Did you forget about that?"
        for sender in self.notify:
          self.call_service(sender, title = title, message = message, data = data)
          self.log("Message {} sended to {}".format(title, sender))
        # self.notify(name="notify.push_to_chrome_nizm0_oneplus3", title = "Hello", message = "Hello World from appDeamon", data=data)
      elif ocupancy == 'not_home' and home_preset == 'Empty':
        self.start_vacuum(self)
        self.log("Vacuum started")

  def start_vacuum(self):
    self.log("vacuum/start for {}".format("vacuum.rockrobo"))
    self.call_service("vacuum/start", entity_id="vacuum.rockrobo")
  def stop_vacuum(self):
    self.log("vacuum/stop for {}".format("vacuum.rockrobo"))
    self.call_service("vacuum/return_to_base", entity_id="vacuum.rockrobo")
  def pause_vacuum(self):
    self.log("vacuum/stop for {}".format("vacuum.rockrobo"))
    self.call_service("vacuum/return_to_base", entity_id="vacuum.rockrobo")

  def pause_vacuum_for(self, seconds):
    self.log("vacuum/pause for {}".format(seconds))
    self.run_in(self.pause_vacuum, 1)
    self.run_in(self.start_vacuum, seconds)

  def notify_on_start(self, sender, title, message):
    data =  {
          "vibrate": "200, 100, 200, 100, 200, 100, 200",
          # "importance": "hight",
          "renotify": "true",
          # "timestamp": time,
          "priority": "high",
          "actions": [
            {
              "action": "start_vacuum",
              "icon": "/static/icons/favicon-192x192.png",
              "title": "Start Vacuum"
            },
            {
              "action": "cancel",
              "title": "Cancel"
            }],
          "tag": "home-vacuum-automation"
        }
    for sender in self.notify:
      self.call_service(sender, title = title, message = message, data = data)