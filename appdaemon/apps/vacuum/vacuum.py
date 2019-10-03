import appdaemon.plugins.hass.hassapi as hass
import datetime
import json
from collections import namedtuple
from base import Base
import globals
# from globals import Actions

class VacuumActions(Base):

  # title = "Roborock"
  # vacuum_entity = ""
  vacuum_timer_handler = None

  def initialize(self):
    self.title = "Roborock"
    self.tag = self.args["tag"]
    self.vacuum_entity = self.args["vacuum_entity"]
    self.vacuum_time_entity = self.args["vacuum_time_entity"]
    self.ready_to_vacuum = self.args["ready_to_vacuum"]
    self.ocupancy = self.args["ocupancy"]
    self.home_preset_select = self.args["home_preset_select"]
    self.notifiers = self.args["notifiers"]
    self.counter = 0
    self.vacuum_timer_handler = None
    self.ready_to_cleaning = False
    self.surface_cleaned_since_last_cleaning = 0 # TODO create sensor in HAS
    self.set_vacuum_timer(self, self.vacuum_time_entity, '', self.get_state(self.vacuum_time_entity), '')
    self.listen_state(self.change_vacuum_timer, self.vacuum_time_entity)
    self.listen_state(self.vacuum_state_handle, self.vacuum_entity)
    self.listen_event(self.action_event_clicked, "html5_notification.clicked", tag=self.tag)

  def set_vacuum_timer(self, entity, attribute, old, new, kwargs):
    self.input_time = datetime.time.fromisoformat(new)
    self.vacuum_daily = self.run_daily(self.run_daily_callback, self.input_time)
    self.counter = self.counter + 1
    self.log(f"Reinitialize run daily for {self.counter} time with {self.input_time}")

  def change_vacuum_timer(self, entity, attribute, old, new, kwargs):
    self.cancel_vacuum_timer(self.vacuum_timer_handler)
    self.log(f"Cancel previous timer at {old}")
    self.set_vacuum_timer(entity, attribute, old, new, kwargs)

  def run_daily_callback(self, kwargs):
    self.log("Run daily vacuum")
    ready = self.get_state(self.ready_to_vacuum)
    ocupancy = self.get_state(self.ocupancy)
    home_preset = self.get_state(self.home_preset_select)
    message = ""
    # dump_actions = json.dump(Actions)
    if self.get_state(self.vacuum_entity) not in ["cleaning", "error", "returning"]:
      actions = []#{Actions["start_vacuum"], Actions["cancel"]}
      if ready != "on":
        message = "Flor is not ready to cleanup? Did you forget about that?"
        self.notify_on_change(self.title, message, actions=[Actions["start_vacuum"], Actions["cancel"]])
        self.log("Flor is not ready, wainting for response.")
      elif ocupancy == 'not_home' and home_preset == 'Empty':
        self.start_vacuum()
        self.log("Vacuum started")
      else:
        message = "Flor is ready to cleanup, but I can see that someone is in home. I will start vacuum in 5 min."
        self.notify_on_change(self.title, message, actions=[Actions["pospone"], Actions["cancel"]])
        self.vacuum_timer_handler = self.run_in(self.start_vacuum, 300)
        self.log("Vacuum will start in 5 min.")

  def vacuum_state_handle(self, entity, attribute, old, new, kwargs):
    self.vacuum = self.get_state(self.vacuum_entity, attribute="all")
    # self.log(f"VACUUM ENTITY AS OBJECT {self.vacuum}")
    message = ""
    if (old != new):
      if new == "error":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.notify_on_change(title=self.title, message="Vacuum encouner an problem", actions=[])
      elif new == "cleaning":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        message = f"Vacuum is now {new}, is it intended?"
        self.notify_on_change(title=self.title, message=message, actions=[Actions["stop_vacuum"], Actions["cancel"]])
      elif new == "returning":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        if old == "cleaning":
          cleaned_area = self.vacuum["attributes"]["cleaned_area"]
          cleaning_time = self.vacuum["attributes"]["cleaning_time"]
          message = f"Vacuum has finished his work, cleaned {cleaned_area} m\u00b2 in {cleaning_time} min"
          self.notify_on_change(title=self.title, message=message, actions=[])
          self.turn_off(self.ready_to_vacuum)
          self.surface_cleaned_since_last_cleaning =+ cleaned_area
          if self.surface_cleaned_since_last_cleaning > 100:
            self.ready_to_cleaning = True
      elif new == "docked":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        # message == message + " and docked."
        # self.notify_on_change(title=self.title, message=message, actions=[])
      elif new == "idle":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.vacuum_timer_handler = self.run_in(self.dock_vacuum, 300)
      elif new == "paused":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.notify_on_change(title=self.title, message="The vacuum cleaner has been suspended", actions=[Actions["start_vacuum"], Actions["return_vacuum"]])
      else:
        self.log(f"Vacuum new state: {new} and attribute {attribute}")

  def action_event_clicked(self, event_name, data, kwargs):
    event_action = data["action"]
    event_tag = data["tag"]
    # self.log("Push notification clicked (action) {event_action}")
    if event_action == "start_vacuum":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      self.start_vacuum()
    elif event_action == "stop_vacuum":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      self.stop_vacuum()
    elif event_action == "return_vacuum":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      self.dock_vacuum()
    elif event_action == "send_to_clinup":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      clinup_location = self.args["clinup_location"]
      if clinup_location != None:
        self.go_to(clinup_location)
    elif event_action == "cancel":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      # self.cancel_vacuum_timer()
    elif event_action == "pospone":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      self.postpone_vacuum_timer(3600)

  def vacuum_action(self, service, **kwargs):
    self.log(f"{service} for {kwargs}")
    self.call_service(service, **kwargs)

  def start_vacuum(self):
    self.vacuum_action("vacuum/start", entity_id=self.vacuum_entity)
    self.cancel_vacuum_timer(self.vacuum_timer_handler)
  def stop_vacuum(self):
    self.vacuum_action("vacuum/stop", entity_id=self.vacuum_entity)
  def pause_vacuum(self, kwargs):
    self.vacuum_action("vacuum/pause", entity_id=self.vacuum_entity)
  def dock_vacuum(self, kwargs):
    self.vacuum_action("vacuum/return_to_base", entity_id=self.vacuum_entity)
  def pause_vacuum_for(self, seconds):
    self.pause_vacuum()
    self.run_in(self.start_vacuum, seconds)
  def go_to(self, pos):
    self.vacuum_action("vacuum/send_command", entity_id=self.vacuum_entity, command="app_goto_target", params=pos)

  def cancel_vacuum_timer(self, vacuum_timer):
    if vacuum_timer is not None:
      self.cancel_timer(vacuum_timer)

  def postpone_vacuum_timer(self, sec):
    if self.vacuum_timer_handler is not None:
      self.cancel_timer(self.vacuum_timer_handler)
    self.vacuum_timer_handler = self.run_in(self.start_vacuum, sec)
    start = self.time() + "01:00:00"
    self.notify_on_change(title=self.title, message=f"Vacuuming postponed to {start}", actions=[Actions["start_vacuum"], Actions["return_vacuum"]])

  def notify_on_change(self, title, message, actions):
    # try:
    data = self.prepare_data_for_notify(actions=actions, tag=self.tag)
    for sender in self.notifiers:
      self.call_service(sender, title=title, message=message, data=data)
      self.log(f"Message \"{message}\" sent to {sender} with data={data}")
    # except:
    #   self.log(f"Some data are mising sender={self.notifiers} title={title} message={message} actions={actions}")
    #   return

  def prepare_data_for_notify(self, actions, tag):
    data = {
      "vibrate": "200, 100, 200, 100, 200, 100, 200",
      # "importance": "hight",
      "renotify": "true",
      # "timestamp": time,
      "priority": "high",
      "actions": actions,
      "tag": tag
    }# self.log(data)
    return data

  def dismiss_by_tag(self, tag):
    self.call_service("notify/html5_dismiss", data={"tag": tag})
  
  def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
  def json2obj(self, data): return json.loads(data, object_hook=self._json_object_hook)


Actions = {
    'start_vacuum': {
        "action": "start_vacuum",
        # "icon": "/static/icons/favicon-192x192.png",
        "title": "Start Vacuum"
    },
    'stop_vacuum': {
        "action": "stop_vacuum",
        # "icon": "/static/icons/favicon-192x192.png",
        "title": "Stop Vacuum"
    },
    'return_vacuum': {
        "action": "return_vacuum",
        # "icon": "/static/icons/favicon-192x192.png",
        "title": "Return Vacuum"
    },
    'send_clinup': {
        "action": "send_to_clinup",
        # "icon": "/static/icons/favicon-192x192.png",
        "title": "Send to clinup"
    },
    'pospone': {
        "action": "pospone",
        "title": "Pospone fo 1h"
    },
    'cancel': {
        "action": "cancel",
        "title": "Cancel"
    }
}