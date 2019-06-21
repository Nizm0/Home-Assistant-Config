import appdaemon.plugins.hass.hassapi as hass
import datetime
from base import Base
# from datetime import time, timedelta, tzinfo
# from datetime import time

class VacuumActions(Base):

  def initialize(self):
    input_time = datetime.time.fromisoformat(self.get_state("input_datetime.vacuum_day_time"))
    self.log(input_time)
    time = datetime.time(15, 00)
    # Schedule a daily callback that will call run_daily()
    self.run_daily(self.run_daily_callback, time)

  # Our callback function will be called by the scheduler every day
  def run_daily_callback(self, kwargs):
    ready = self.get_state("input_boolean.ready_to_vacuum")
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
      self.call_service("notify/push_to_chrome_nizm0_oneplus3", title = "Hello", message = "Hello World from appDeamon", data = data)
      # self.notify(name="notify.push_to_chrome_nizm0_oneplus3", title = "Hello", message = "Hello World from appDeamon", data=data)

  def start_vacuum(self):
    self.log("vacuum/start for {}".format("vacuum.rockrobo"))
    self.call_service("vacuum/start", entity_id="vacuum.rockrobo")