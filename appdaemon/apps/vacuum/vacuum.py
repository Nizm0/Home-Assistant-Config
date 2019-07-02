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
    self.change_time(self, "input_datetime.vacuum_day_time", '', self.get_state("input_datetime.vacuum_day_time"), '')
    self.listen_state(self.change_time, "input_datetime.vacuum_day_time")

  def change_time(self, entity, attribute, old, new, kwargs):
    input_time = datetime.time.fromisoformat(new)
    self.run_daily(self.run_daily_callback, input_time)
    self.counter = self.counter + 1
    self.log("Reinitialize run daily for {} time with {}".format(self.counter ,input_time))

  # Our callback function will be called by the scheduler every day
  def run_daily_callback(self, kwargs):
    self.log("Run daily vacuum")
    ready = self.get_state("input_boolean.ready_to_vacuum")
    title = "Roborock"
    message = "Flor is not ready to cleanup? Did you forget about that?"
    notify = ["notify/push_to_chrome_nizm0_oneplus3"]
    data =  {
              "vibrate": "200, 100, 200, 100, 200, 100, 200",
              # "importance": "hight",
              "renotify": "true",
              # "timestamp": time,
              # "priority": 0,
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
    if ready != "on":
      for sender in notify:
        self.call_service(sender, title = title, message = message, data = data)
        self.log("Message {} sended to {}".format(title, sender))
      # self.notify(name="notify.push_to_chrome_nizm0_oneplus3", title = "Hello", message = "Hello World from appDeamon", data=data)

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