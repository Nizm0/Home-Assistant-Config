import appdaemon.plugins.hass.hassapi as hass
import datetime
import json
from base import Base
import globals
from globals import Actions

class VacuumActions(Base):


  def initialize(self):
    self.tag = "home-vacuum-automation"
    self.counter = 0
    self.vacuum_timer_handle = None
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
        self.cancel_timer()
        self.log(f"Vacuum new state: {new}")
        message = f"Vacuum is now {new}, is it intended?"
        self.notify_on_start(title, message)
      elif new == "docked":
        self.cancel_timer()
        self.log("Vacuum new state: {}".format(new))
      elif new == "idle":
        self.log("Vacuum new state: {}".format(new))
        self.vacuum_timer_handle = self.run_in(self.dock_vacuum, 300)
      elif new == "pause":
        self.log("Vacuum new state: {}".format(new))
      elif new == "returning":
        self.cancel_timer()
        self.log("Vacuum new state: {}".format(new))
      else:
        self.log("Vacuum new state: {}".format(new))

  def run_daily_callback(self, kwargs):
    self.log("Run daily vacuum")
    ready = self.get_state("input_boolean.ready_to_vacuum")
    ocupancy = self.get_state("group.all_devices")
    home_preset = self.get_state("input_select.home_preset")
    title = "Roborock"
    message = ""
    # data =  self.prepare_data_for_notify(self, action, self.tag)
    # notify = ["notify/push_to_chrome_nizm0_oneplus3"]

    if self.get_state("vacuum.rockrobo") not in ["cleaning", "error", "returning"]:
      if ready != "on":
        message = "Flor is not ready to cleanup? Did you forget about that?"
        # actions = {"start_vacuum", "cancel"}
        # # actions.append(Actions["start_vacuum"])
        # # actions.append(Actions["cancel"])
        # self.log("Print Actions")
        # self.log(actions)
        data = {
          "vibrate": "200, 100, 200, 100, 200, 100, 200",
          # "importance": "hight",
          "renotify": "true",
          # "timestamp": time,
          "priority": "high",
          "actions": [{
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
          # data = self.prepare_data_for_notify(actions, self.tag)
          self.call_service(sender, title = title, message = message, data = data)
          self.log("Message {} sended to {}".format(title, sender))
        # self.notify(name="notify.push_to_chrome_nizm0_oneplus3", title = "Hello", message = "Hello World from appDeamon", data=data)
      elif ocupancy == 'not_home' and home_preset == 'Empty':
        self.start_vacuum()
        self.log("Vacuum started")
      else:
        message = "Flor is ready to cleanup, but I can see someone is in home. I will start vacuum in 5 min."
        data = {
          "vibrate": "200, 100, 200, 100, 200, 100, 200",
          "renotify": "true",
          "priority": "high",
          "actions": [{
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
          self.log("Message {} sended to {}".format(title, sender))
        self.vacuum_timer_handle = self.run_in(self.start_vacuum, 300)


  def start_vacuum(self):
    self.log("vacuum/start for {}".format("vacuum.rockrobo"))
    self.call_service("vacuum/start", entity_id="vacuum.rockrobo")
  def stop_vacuum(self):
    self.log("vacuum/stop for {}".format("vacuum.rockrobo"))
    self.call_service("vacuum/stop", entity_id="vacuum.rockrobo")
  def pause_vacuum(self):
    self.log("vacuum/stop for {}".format("vacuum.rockrobo"))
    self.call_service("vacuum/pause", entity_id="vacuum.rockrobo")
  def dock_vacuum(self, kwargs):
    self.log("vacuum/dock for {}".format("vacuum.rockrobo"))
    self.call_service("vacuum/return_to_base", entity_id="vacuum.rockrobo")
  def cancel_timer(self, kwargs):
    if self.vacuum_timer_handle is not None:
      self.cancel_timer(self.vacuum_timer_handle)

  def pause_vacuum_for(self, seconds):
    self.log("vacuum/pause for {}".format(seconds))
    self.run_in(self.pause_vacuum, 1)
    self.run_in(self.start_vacuum, seconds)

  def notify_on_start(self, title, message):
    data = {
      "vibrate": "200, 100, 200, 100, 200, 100, 200",
      # "importance": "hight",
      "renotify": "true",
      # "timestamp": time,
      "priority": "high",
      "actions": [{
                  "action": "stop_vacuum",
                  "icon": "/static/icons/favicon-192x192.png",
                  "title": "Stop Vacuum"
                },
                {
                  "action": "cancel",
                  "title": "Cancel"
                }],
      "tag": "home-vacuum-automation"
    }
    for sender in self.notify:
      self.call_service(sender, title = title, message = message, data = data)

  def prepare_data_for_notify(self, actions, tag):
    data = {
      "vibrate": "200, 100, 200, 100, 200, 100, 200",
      # "importance": "hight",
      "renotify": "true",
      # "timestamp": time,
      "priority": "high",
      "actions": Actions[actions[1]],
      # "tag": tag
    }
    # data.append(actions)
    data.append(tag)
    self.log("Print data")
    self.log(data)
    return data