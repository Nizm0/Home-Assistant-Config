import appdaemon.plugins.hass.hassapi as hass
import datetime
import json
# from datetime import datetime
from collections import namedtuple
from base import Base
import globals
# from globals import Actions

class VacuumActions(Base):

  # title = "Roborock"
  # vacuum_entity = ""
  # vacuum_timer_handler = None

  def initialize(self):
    self.title = "Roborock"
    self.tag = self.args["tag"]
    self.vacuum_entity = self.args["vacuum_entity"]
    self.vacuum_time_entity = self.args["vacuum_time_entity"]
    self.ready_to_vacuum_entity = self.args["ready_to_vacuum"]
    self.ocupancy_entity = self.args["ocupancy"]
    self.home_preset_select = self.args["home_preset_select"]
    self.notifiers = self.args["notifiers"]
    self.cleaned_area_entity = self.args["cleaned_area"]
    self.counter = 0
    self.vacuum_daily = None
    self.vacuum_timer_handler = None
    self.ready_for_emptying = False
    self.waiting_for_emptying = False
    self.waiting_return_home = False
    self.run_by_app = False
    self.cleaned_area = int(float(self.get_state(self.cleaned_area_entity)))

    self.set_run_daily(self, self.vacuum_time_entity, '', self.get_state(self.vacuum_time_entity), '')
    self.listen_state(self.cleaned_area_changed, self.cleaned_area_entity)
    self.listen_state(self.change_run_daily, self.vacuum_time_entity)
    self.listen_state(self.vacuum_state_handle, self.vacuum_entity)
    self.listen_event(self.action_event_clicked, "html5_notification.clicked", tag=self.tag)
    if self.args["switch"] is not None:
      self.listen_event(self.event_received, "deconz_event")

  def cleaned_area_changed(self, entity, attribute, old, new, kwargs):
    self.cleaned_area = int(float(new))
    if(self.cleaned_area > self.args["area_befor_emptying"]):
      self.ready_for_emptying = True

  def send_vacuum_for_emtying(self, entity, attribute, old, new, kwargs):
    emptying_location = self.args["emptying_location"]
    self.vacuum_action("vacuum/send_command", entity_id=self.vacuum_entity, command="app_goto_target", params=emptying_location)
    self.waiting_for_emptying = True
    # self.cancel_vacuum_timer(self.vacuum_timer_handler)

  def vacuum_emptied(self):
    self.log('Vacuum emptied, returnig to dock')
    self.waiting_for_emptying = False
    self.set_value(self.cleaned_area_entity, value=0)
    self.dock_vacuum(None)

  def set_run_daily(self, entity, attribute, old, new, kwargs):
    self.input_time = datetime.time.fromisoformat(new)
    # self.cancel_vacuum_timer(self.vacuum_daily)
    self.vacuum_daily = self.run_daily(self.run_daily_callback, self.input_time)
    self.counter = self.counter + 1
    self.log(f"Reinitialize run daily for {self.counter} time with {self.input_time}")

  def change_run_daily(self, entity, attribute, old, new, kwargs):
    self.cancel_vacuum_timer(self.vacuum_daily)
    self.log(f"Cancel previous timer at {old}")
    self.set_run_daily(entity, attribute, old, new, kwargs)

  def run_daily_callback(self, kwargs):
    self.log("Run daily vacuum")
    ready = self.get_state(self.ready_to_vacuum_entity)
    ocupancy = self.get_state(self.ocupancy_entity)
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
        message = "Started dayly Cleanup"
        self.notify_on_change(self.title, message, actions=[Actions["return_vacuum"]])
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
        if not self.run_by_app:
          message = f"Vacuum is now {new}, is it intended?"
          self.notify_on_change(title=self.title, message=message, actions=[Actions["stop_vacuum"], Actions["cancel"]])
      elif new == "returning":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        if old == "cleaning":
          cleaned_area = self.vacuum["attributes"]["cleaned_area"]
          cleaning_time = self.vacuum["attributes"]["cleaning_time"]
          # self.log(f"Cleaned_area = {cleaned_area} and type {type(cleaned_area)} and self.cleaned_area = {self.cleaned_area} and type {type(self.cleaned_area)} ")
          self.log(f"Vacuum cleaned area from last emptying: {self.cleaned_area} and type {type(self.cleaned_area)}\n and in thad time: {cleaned_area} and type {type(cleaned_area)}")
          self.cleaned_area = self.cleaned_area + cleaned_area
          self.set_value(self.cleaned_area_entity, value=self.cleaned_area)
          message = f"Vacuum has finished his work, cleaned {cleaned_area} m\u00b2 in {cleaning_time} min."
          actions = []
          if self.cleaned_area > int(float(self.args["area_befor_emptying"])):
            message = message + f" You have nod emptied me that long, I'm almost full."
            actions = [Actions["send_for_emptying"], Actions["send_wen_in_home"]]
            self.ready_for_emptying = True
          self.notify_on_change(title=self.title, message=message, actions=actions)
          self.turn_off(self.ready_to_vacuum_entity)
      elif new == "docked":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.run_by_app = False
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        # if self.waiting_for_emptying:
        #   self.waiting_for_emptying = False
        #   self.set_value(self.cleaned_area_entity, value=0)
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
      self.dock_vacuum(kwargs)
    elif event_action == "send_for_emptying":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      self.send_vacuum_for_emtying(None, None, None, None, kwargs)
      # clinup_location = self.args["clinup_location"]
      # if clinup_location != None:
      #   self.go_to(clinup_location)
    elif event_action == "cancel":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      # self.cancel_vacuum_timer()
    elif event_action == "pospone":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      self.postpone_vacuum_timer(3600)
    # elif event_action == "send_now":
    #   self.log(f"Push notification clicked {event_action}, {data}")
    #   self.dismiss_by_tag(event_tag)
    #   self.send_vacuum_for_emtying(None, None, None, None, kwargs)
      # self.postpone_vacuum_timer(3600)
    elif event_action == "send_wen_in_home":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      # self.postpone_vacuum_timer(3600)

  def vacuum_action(self, service, **kwargs):
    self.log(f"{service} for {kwargs}")
    self.call_service(service, **kwargs)

  def start_vacuum(self):
    self.run_by_app = True
    self.vacuum_action("vacuum/start", entity_id=self.vacuum_entity)
    self.cancel_vacuum_timer(self.vacuum_timer_handler)
  def stop_vacuum(self):
    self.vacuum_action("vacuum/stop", entity_id=self.vacuum_entity)
  def pause_vacuum(self):
    self.vacuum_action("vacuum/pause", entity_id=self.vacuum_entity)
  def dock_vacuum(self, kwargs):
    if not self.waiting_for_emptying:
      self.vacuum_action("vacuum/return_to_base", entity_id=self.vacuum_entity)
    else:
      self.vacuum_timer_handler = self.run_in(self.dock_vacuum, 600)
      self.waiting_for_emptying = False
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

  def event_received(self, event_name, data, kwargs):
    if data != {}:
      event_data = data["event"]
      event_id = data["id"]
      event_received = datetime.datetime.now()
      self.log("fDeconz event received from {event_id}. Event was: {event_data}")
      self.set_state("sensor.deconz_event", state = event_id, attributes = {"event_data": event_data, "event_received": str(event_received)})
      if event_id in self.args['switch']:
        self.event_button(event_name, data, kwargs)
      else:
        self.log(f'Usuported device {event_id}')
    else:
      self.log('Data is empty')

  def event_button(self, event_name, data, kwargs):
    event_data = data["event"]
    button = data['id']
    event_received = datetime.datetime.now()
    # self.log(event_data)
    # if event_data == 1000: #down
    self.log(f'Button {button} down, date {event_received}')
    if button == self.args["switch"]:
      if event_data == 1002: #releas
        self.log(f'Button {button} release, I\'m ready to cleanup')
        self.turn_on(self.ready_to_vacuum_entity)
      # elif event_data == 1001: #long down
        self.log(f'Button {button} long click down, date {event_received}')
      elif event_data == 1003: #long release
        if not self.waiting_for_emptying:
          self.send_vacuum_for_emtying(None, None, None, None, kwargs)
          self.log(f'Button {button} long click release.\n Vacuum waiting for emtying.')
        else:
          self.vacuum_emptied()
          self.log(f'Button {button} long click release, date {event_received}.\n Vacuum emptyed, returnig to base.')
      elif event_data == 1004: #double click
        self.log(f'Button {button} double click, starting cleanup immediately')
        vacuum_state = self.get_state(self.vacuum_entity)
        if vacuum_state in ["cleaning"]:
          self.dock_vacuum(kwargs)
        elif vacuum_state in ["docked", "idle", "paused"]:
          self.start_vacuum()
      elif event_data > 1004 and event_data < 1010: #multi click
        self.log(f'Button {button} multi click, panik butto!! Stop and returnikg to dock')
        if vacuum_state not in ["error"]:
          self.dock_vacuum(kwargs)
      else:
        self.log(f'Button event {event_data} not suported, date {event_received}')


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
    'send_for_emptying': {
        "action": "send_for_emptying",
        # "icon": "/static/icons/favicon-192x192.png",
        "title": "Send for emptying"
    },
    'pospone': {
        "action": "pospone",
        "title": "Pospone fo 1h"
    },
    'cancel': {
        "action": "cancel",
        "title": "Cancel"
    },
    # 'send_now': {
    #     "action": "send_now",
    #     "title": "Send now"
    # },
    'send_wen_in_home': {
        "action": "send_wen_in_home",
        "title": "Send when home"
    }
}