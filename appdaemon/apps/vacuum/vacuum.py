import appdaemon.plugins.hass.hassapi as hass
import datetime
import json
from base import Base
import globals
from globals import Actions

class VacuumActions(Base):

  def initialize(self):
    self.title = "Roborock"
    self.tag = self.args["tag"]
    self.vacuum_entity = self.args["vacuum_entity"]
    self.vacuum_time_entity = self.args["vacuum_time_entity"]
    self.ready_to_vacuum = self.args["ready_to_vacuum"]
    self.ocupancy = self.args["ocupancy"]
    self.home_preset_select = self.args["home_preset_select"]
    self.counter = 0
    self.vacuum_timer_handle = None
    self.notifiers = self.args["notifiers"]
    self.set_vacuum_timer(self, self.vacuum_time_entity, '', self.get_state(self.vacuum_time_entity), '')
    self.listen_state(self.change_vacuum_timer, self.vacuum_time_entity)
    self.listen_state(self.vacuum_state_handle, self.vacuum_entity)

  def set_vacuum_timer(self, entity, attribute, old, new, kwargs):
    self.input_time = datetime.time.fromisoformat(new)
    self.vacuum_daily = self.run_daily(self.run_daily_callback, self.input_time)
    self.counter = self.counter + 1
    self.log("Reinitialize run daily for {} time with {}".format(self.counter ,self.input_time))

  def change_vacuum_timer(self, entity, attribute, old, new, kwargs):
    self.cancel_vacuum_timer()
    self.log("Cancel previous timer at {}".format(old))
    self.set_vacuum_timer(self, entity, '', new, '')

  def vacuum_state_handle(self, entity, attribute, old, new, kwargs):
    if (old != new):
      if new == "error":
        self.log("Vacuum new state: {}".format(new))
        self.notify_on_change(title=self.title, message=f"Vacuum encouner an problem", actions=[])
      elif new == "cleaning":
        self.cancel_vacuum_timer()
        self.log(f"Vacuum new state: {new}")
        message = f"Vacuum is now {new}, is it intended?"
        self.notify_on_change(title=self.title, message=message, actions=["stop_vacuum", "cancel"])
      elif new == "docked":
        self.cancel_vacuum_timer()
        self.log("Vacuum new state: {}".format(new))
        self.notify_on_change(title=self.title, message=f"Vacuum has finished his work", actions=[])
      elif new == "idle":
        self.log("Vacuum new state: {}".format(new))
        self.vacuum_timer_handle = self.run_in(self.dock_vacuum, 300)
      elif new == "pause":
        self.log("Vacuum new state: {}".format(new))
      elif new == "returning":
        self.cancel_vacuum_timer()
        self.log("Vacuum new state: {}".format(new))
      else:
        self.log("Vacuum new state: {}".format(new))

  def run_daily_callback(self, kwargs):
    self.log("Run daily vacuum")
    ready = self.get_state(self.ready_to_vacuum)
    ocupancy = self.get_state(self.ocupancy)
    home_preset = self.get_state(self.home_preset_select)
    message = ""
    if self.get_state(self.vacuum_entity) not in ["cleaning", "error", "returning"]:
      actions = []#{Actions["start_vacuum"], Actions["cancel"]}
      if ready != "on":
        message = "Flor is not ready to cleanup? Did you forget about that?"
        self.notify_on_change(self.title, message, actions=["start_vacuum", "cancel"])
        # actions.append(Actions["start_vacuum"])
        # actions.append(Actions["cancel"])
        # self.log(f"Actions {actions}")
        # data = self.prepare_data_for_notify(actions, self.tag)
        # for sender in self.notifiers:
        #   self.call_service(sender, title=self.title, message = message, data = data)
        #   self.log(f"Message {self.title} sended to {sender}")
      elif ocupancy == 'not_home' and home_preset == 'Empty':
        self.start_vacuum(kwargs)
        self.log("Vacuum started")
      else:
        message = "Flor is ready to cleanup, but I can see someone is in home. I will start vacuum in 5 min."
        self.notify_on_change(self.title, message, actions=["pospone", "cancel"])
        # actions.append(Actions["start_vacuum"])
        # actions.append(Actions["cancel"])
        # data = self.prepare_data_for_notify(actions, self.tag)
        # for sender in self.notifiers:
        #   self.call_service(sender, title=self.title, message=message, data=data)
        #   self.log(f"Message {self.title} sended to {sender}")
        self.vacuum_timer_handle = self.run_in(self.start_vacuum, 300)

  def vacuum_action(self, service, vacuum, kwargs):
    self.log(f"{service} for {vacuum}")
    self.call_service(service, entity_id=vacuum)

  def start_vacuum(self, kwargs):
    self.vacuum_action("vacuum/start", self.vacuum_entity)
    # self.log("vacuum/start for {}".format("vacuum.rockrobo"))
    # self.call_service("vacuum/start", entity_id="vacuum.rockrobo")
    self.cancel_vacuum_timer()
  def stop_vacuum(self, kwargs):
    self.vacuum_action("vacuum/stop", self.vacuum_entity)
    # self.log("vacuum/stop for {}".format("vacuum.rockrobo"))
    # self.call_service("vacuum/stop", entity_id="vacuum.rockrobo")
  def pause_vacuum(self, kwargs):
    self.vacuum_action("vacuum/pause", self.vacuum_entity)
    # self.log("vacuum/stop for {}".format("vacuum.rockrobo"))
    # self.call_service("vacuum/pause", entity_id="vacuum.rockrobo")
  def dock_vacuum(self, kwargs):
    self.vacuum_action("vacuum/return_to_base", self.vacuum_entity)
    # self.log("vacuum/dock for {}".format("vacuum.rockrobo"))
    # self.call_service("vacuum/return_to_base", entity_id="vacuum.rockrobo")
    self.turn_off(self.ready_to_vacuum)
  def pause_vacuum_for(self, seconds):
    self.vacuum_action("vacuum/pause", self.vacuum_entity)
    self.run_in(self.start_vacuum, seconds)

  def cancel_vacuum_timer(self):
    if self.vacuum_timer_handle is not None:
      self.cancel_timer(self.vacuum_timer_handle)

  def postpone_vacuum_timer(self, sec):
    if self.vacuum_timer_handle is not None:
      self.cancel_timer(self.vacuum_timer_handle)
    self.vacuum_timer_handle = self.run_in(self.start_vacuum, sec)

  # def notify_on_error(self, title, message):
  #   data = self.prepare_data_for_notify(actions=[], tag=self.tag)
  #   self.notify_on_change(title=title, message=message, data=data)

  # def notify_on_dock(self, title, message):
  #   data = self.prepare_data_for_notify(actions=[], tag=self.tag)
  #   self.notify_on_change(title=title, message=message, data=data)

  # def notify_on_start(self, title, message):
  #   actions = []#[Actions["start_vacuum"], Actions["cancel"]]
  #   actions.append(Actions["stop_vacuum"])
  #   actions.append(Actions["cancel"])
  #   data = self.prepare_data_for_notify(actions=actions, tag=self.tag)
  #   for sender in self.notifiers:
  #     self.call_service(sender, title=title, message=message, data=data)

  def notify_on_change(self, title, message, actions):
    a = []
    try:
      for action in actions:
        a.append(Actons[action])
      data = self.prepare_data_for_notify(actions=actions, tag=self.tag)
      for sender in self.notifiers:
        self.call_service(sender, title=title, message=message, data=data)
    except:
      self.log(f"Some data are mising sender={sender} title={title} message={message} actions={actions}")
      return

  def prepare_data_for_notify(self, actions, tag):
    data = {
      "vibrate": "200, 100, 200, 100, 200, 100, 200",
      # "importance": "hight",
      "renotify": "true",
      # "timestamp": time,
      "priority": "high",
      "actions": actions,
      "tag": tag
    }
    self.log("Print data")
    self.log(data)
    return data