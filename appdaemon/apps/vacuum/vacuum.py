import appdaemon.plugins.hass.hassapi as hass
import datetime
import json
from base import Base
import globals
from globals import Actions

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
    self.counter = 0
    self.vacuum_timer_handler = None
    self.notifiers = self.args["notifiers"]
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
    self.set_vacuum_timer(self, entity, '', new, '')
    vacuum = self.get_state(self.vacuum_entity, attribute="all")
    self.log(f"Vacuum all atributes {vacuum}")

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
        self.log("Flor is not ready, wainting for response.")
      elif ocupancy == 'not_home' and home_preset == 'Empty':
        self.start_vacuum()
        self.log("Vacuum started")
      else:
        message = "Flor is ready to cleanup, but I can see that someone is in home. I will start vacuum in 5 min."
        self.notify_on_change(self.title, message, actions=["pospone", "cancel"])
        self.vacuum_timer_handler = self.run_in(self.start_vacuum, 300)
        self.log("Vacuum will start in 5 min.")

  def vacuum_state_handle(self, entity, attribute, old, new, kwargs):
    vacuum = self.get_state(self.vacuum_entity, attribute="all")
    if (old != new):
      if new == "error":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.notify_on_change(title=self.title, message="Vacuum encouner an problem", actions=[])
      elif new == "cleaning":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        message = f"Vacuum is now {new}, is it intended?"
        self.notify_on_change(title=self.title, message=message, actions=["stop_vacuum", "cancel"])
      elif new == "docked":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        # cleaned_area = attribute["cleaned_area"]
        # cleaning_time = attribute["cleaning_time"]
        message = f"Vacuum has finished his work, cleaned {vacuum.attributes.cleaned_area} m\2 in {vacuum.attributes.cleaning_time} min"
        self.notify_on_change(title=self.title, message=message, actions=[])
        self.turn_off(self.ready_to_vacuum)
      elif new == "idle":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.vacuum_timer_handler = self.run_in(self.dock_vacuum, 300)
      elif new == "paused":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.notify_on_change(title=self.title, message="The vacuum cleaner has been suspended", actions=["start_vacuum", "return_vacuum"])
      elif new == "returning":
        self.log(f"Vacuum new state: {new} and attribute {attribute}")
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
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
    elif event_action == "cancel":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      # self.cancel_vacuum_timer()
    elif event_action == "pospone":
      self.log(f"Push notification clicked {event_action}, {data}")
      self.dismiss_by_tag(event_tag)
      self.postpone_vacuum_timer(3600)

  def vacuum_action(self, service, vacuum):
    self.log(f"{service} for {vacuum}")
    self.call_service(service, entity_id=vacuum)

  def start_vacuum(self):
    self.vacuum_action("vacuum/start", vacuum_entity)
    # self.call_service("vacuum/start", entity_id="vacuum.rockrobo")
    self.cancel_vacuum_timer(self.vacuum_timer_handler)
  def stop_vacuum(self):
    self.vacuum_action("vacuum/stop", vacuum_entity)
    # self.call_service("vacuum/stop", entity_id="vacuum.rockrobo")
  def pause_vacuum(self, kwargs):
    self.vacuum_action("vacuum/pause", vacuum_entity)
    # self.call_service("vacuum/pause", entity_id="vacuum.rockrobo")
  def dock_vacuum(self, kwargs):
    self.vacuum_action("vacuum/return_to_base", vacuum_entity)
    # self.call_service("vacuum/return_to_base", entity_id="vacuum.rockrobo")
  def pause_vacuum_for(self, seconds):
    # self.vacuum_action("vacuum/pause", vacuum_entity)
    self.pause_vacuum()
    # self.call_service("vacuum/pause", entity_id="vacuum.rockrobo")
    self.run_in(self.start_vacuum, seconds)

  def cancel_vacuum_timer(self, vacuum_timer):
    if vacuum_timer is not None:
      self.cancel_timer(vacuum_timer)

  def postpone_vacuum_timer(self, sec):
    if self.vacuum_timer_handler is not None:
      self.cancel_timer(self.vacuum_timer_handler)
    self.vacuum_timer_handler = self.run_in(self.start_vacuum, sec)
    start = self.time() + "01:00:00"
    self.notify_on_change(self.title, f"Vacuuming postponed to {start}", ["start_vacuum", "return_vacuum"])

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
    a = []
    for action in actions:
      a.append(Actions[action])
    data = {
      "vibrate": "200, 100, 200, 100, 200, 100, 200",
      # "importance": "hight",
      "renotify": "true",
      # "timestamp": time,
      "priority": "high",
      "actions": a,
      "tag": tag
    }
    # self.log("Print data")
    # self.log(data)
    return data

  def dismiss_by_tag(self, tag):
    self.call_service("notify/html5_dismiss", data={"tag": tag})