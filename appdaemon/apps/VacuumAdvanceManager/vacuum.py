import appdaemon.plugins.hass.hassapi as hass
import datetime
import json
# from datetime import datetime
from collections import namedtuple
from base import Base
import globals
# from globals import Actions

class VacuumAdvanceManager(Base):

  def initialize(self):
    self.run_by_app = False
    self.counter = 0

    self.log(f'Fresh start of vacuum Appdaemon app', log="vacuum")

    self.title = "Roborock"
    self.tag = self.args.get("tag", "home-vacuum-automation")
    self.vacuum_entity = self.args.get("vacuum_entity")
    self.vacuum_time_entity = self.args.get("vacuum_time_entity", "input_datetime.vacuum_day_time")
    self.occupancy_entity = self.args.get("occupancy", "group.family")
    self.cleaned_area_entity = self.args.get("cleaned_area", 0)
    self.ready_to_vacuum_entity = self.args.get("ready_to_vacuum", "input_boolean.ready_to_vacuum")
    self.ready_for_emptying_entity = self.args.get("ready_for_emptying_entity", "input_boolean.ready_for_emptying")
    self.waiting_for_emptying_entity = self.args.get("waiting_for_emptying_entity", "input_boolean.waiting_for_emptying")
    self.going_to_be_emptyied_entity = self.args.get("going_to_be_emptyied_entity", "input_boolean.going_to_be_emptyied")
    self.waiting_return_home_entity = self.args.get("waiting_return_home_entity", "input_boolean.waiting_return_home")
    self.ready_to_emptying_vacuum_entity = self.args.get("ready_to_emptying_vacuum_entity", "input_boolean.ready_to_emptying_vacuum")
    
    self.home_preset_select = self.args.get("home_preset_select", "input_select.home_preset")
    self.notifiers = self.args.get("notifiers", [])
    self.vacuum_daily = None
    self.vacuum_timer_handler = None
    
    self.vacuum = self.get_state(self.vacuum_entity, attribute="all")

    self.set_run_daily(self, self.vacuum_time_entity, '', self.get_state(self.vacuum_time_entity), '')
    # self.listen_state(self.cleaned_area_changed, self.cleaned_area_entity)
    self.listen_state(self.change_run_daily, self.vacuum_time_entity)
    self.listen_state(self.vacuum_state_handle, self.vacuum_entity)
    self.listen_event(self.action_event_clicked, "html5_notification.clicked", tag=self.tag)
    if self.args["switch"] is not None:
      self.listen_event(self.event_received, "deconz_event")

  @property
  def ready_to_vacuum(self):
    self.__ready_to_vacuum = self.__convert_on_off_to_boolean(self.get_state(self.ready_to_vacuum_entity))
    self.log(f"read self.ready_to_vacuum {self.__ready_to_vacuum}", log="vacuum")
    return self.__ready_to_vacuum

  @ready_to_vacuum.setter
  def ready_to_vacuum(self, value):
    self.__ready_to_vacuum = value
    self.__turn_on_off_input_boolean(value, self.ready_to_vacuum_entity)
    self.log(f"write self.ready_to_vacuum {self.__ready_to_vacuum}", log="vacuum")

  @property
  def ready_for_emptying(self):
    self.__ready_for_emptying = self.__convert_on_off_to_boolean(self.get_state(self.ready_for_emptying_entity))
    self.log(f"read self.ready_for_emptying {self.__ready_for_emptying}", log="vacuum")
    return self.__ready_for_emptying

  @ready_for_emptying.setter
  def ready_for_emptying(self, value):
    self.__ready_for_emptying = value
    self.__turn_on_off_input_boolean(value, self.ready_for_emptying_entity)
    self.log(f"write self.ready_for_emptying {self.__ready_for_emptying}", log="vacuum")

  @property
  def waiting_for_emptying(self):
    self.__waiting_for_emptying = self.__convert_on_off_to_boolean(self.get_state(self.waiting_for_emptying_entity))
    self.log(f"read self.waiting_for_emptying {self.__waiting_for_emptying}", log="vacuum")
    return self.__waiting_for_emptying

  @waiting_for_emptying.setter
  def waiting_for_emptying(self, value):
    self.__waiting_for_emptying = value
    self.__turn_on_off_input_boolean(value, self.waiting_for_emptying_entity)
    self.log(f"write self.waiting_for_emptying {self.__waiting_for_emptying}", log="vacuum")

  @property
  def going_to_be_emptyied(self):
    self.__going_to_be_emptyied = self.__convert_on_off_to_boolean(self.get_state(self.going_to_be_emptyied_entity))
    self.log(f"read self.going_to_be_emptyied {self.__going_to_be_emptyied}", log="vacuum")
    return self.__going_to_be_emptyied

  @going_to_be_emptyied.setter
  def going_to_be_emptyied(self, value):
    self.__going_to_be_emptyied = value
    self.__turn_on_off_input_boolean(value, self.going_to_be_emptyied_entity)
    self.log(f"write self.going_to_be_emptyied {self.__going_to_be_emptyied}", log="vacuum")

  @property
  def waiting_return_home(self):
    self.__waiting_return_home = self.__convert_on_off_to_boolean(self.get_state(self.waiting_return_home_entity))
    self.log(f"read self.waiting_return_home {self.__waiting_return_home}", log="vacuum")
    return self.__waiting_return_home

  @waiting_return_home.setter
  def waiting_return_home(self, value):
    self.__waiting_return_home = value
    self.__turn_on_off_input_boolean(value, self.waiting_return_home_entity)
    self.log(f"write self.waiting_return_home {self.__waiting_return_home}", log="vacuum")

  @property
  def ready_to_emptying_vacuum(self):
    self.__ready_to_emptying_vacuum = self.self.__convert_on_off_to_boolean(self.get_state(self.ready_to_emptying_vacuum_entity))
    self.log(f"read self.ready_to_emptying_vacuum {self.__ready_to_emptying_vacuum}", log="vacuum")
    return self.__ready_to_emptying_vacuum

  @ready_to_emptying_vacuum.setter
  def ready_to_emptying_vacuum(self, value):
    self.__ready_to_emptying_vacuum = value
    self.__turn_on_off_input_boolean(value, self.ready_to_emptying_vacuum_entity)
    self.log(f"write self.ready_to_emptying_vacuum {self.__ready_to_emptying_vacuum}", log="vacuum")

  @property
  def cleaned_area(self):
    self.__cleaned_area = int(float(self.get_state(self.cleaned_area_entity)))
    self.log(f"read self.cleaned_area {self.__cleaned_area}", log="vacuum")
    return self.__cleaned_area

  @cleaned_area.setter
  def cleaned_area(self, value):
    self.__cleaned_area = value
    self.set_value(self.cleaned_area_entity, value=value)
    self.log(f"write self.cleaned_area {self.__cleaned_area}", log="vacuum")

  def __convert_on_off_to_boolean(self, value):
    if value == "on":
      return True
    else:
      return False

  def __turn_on_off_input_boolean(self, value, entity):
    if value:
      self.turn_on(entity)
    else:
      self.turn_off(entity)

  def send_vacuum_for_emptying(self, entity, attribute, old, new, kwargs):
    emptying_location = self.args["emptying_location"]
    self.log(f"send_vacuum_for_emptying - self.going_to_be_emptyied: {self.going_to_be_emptyied}", log="vacuum")
    self.ready_for_emptying = False
    self.going_to_be_emptyied = True
    self.vacuum_action("vacuum/send_command", entity_id=self.vacuum_entity, command="app_goto_target", params=emptying_location)

  def vacuum_emptied(self):
    self.log('Vacuum emptied, returning to dock')
    self.waiting_for_emptying = False
    self.cleaned_area = 0
    # self.dock_vacuum()

  def set_run_daily(self, entity, attribute, old, new, kwargs):
    self.input_time = datetime.time.fromisoformat(new)
    self.vacuum_daily = self.run_daily(self.run_daily_callback, self.input_time)
    self.counter = self.counter + 1
    self.log(f"Reinitialize run daily for {self.counter} time with {self.input_time}", log="vacuum")

  def change_run_daily(self, entity, attribute, old, new, kwargs):
    self.cancel_vacuum_timer(self.vacuum_daily)
    self.log(f"Cancel previous timer at {old}", log="vacuum")
    self.set_run_daily(entity, attribute, old, new, kwargs)

  def run_daily_callback(self, kwargs):
    self.log("Run daily vacuum", log="vacuum")
    self.vacuum = self.get_state(self.vacuum_entity, attribute="all")
    # ready = self.get_state(self.ready_to_vacuum_entity)
    occupancy = self.get_state(self.occupancy_entity)
    home_preset = self.get_state(self.home_preset_select)
    clean_start = datetime.datetime.strptime(self.vacuum['attributes']['clean_start'], '%Y-%m-%dT%H:%M:%S').date()
    today = clean_start == datetime.date.today()
    message = ""
    if self.vacuum["state"] not in ["cleaning", "error", "returning"]:
      if not self.ready_to_vacuum:
        message = "Flor is not ready to cleanup"
        if not today:
          message = message + "and no one vacuums it"
        message = message + ". Did you forget about me?"
        self.notify_on_change(self.title, message, actions=[Actions["start_vacuum"], Actions["cancel"]])
        self.log("Flor is not ready, wainting for response.", log="vacuum")
      elif occupancy == 'not_home' and home_preset == 'Empty':
        message = "Started daily Cleanup"
        self.notify_on_change(self.title, message, actions=[Actions["return_vacuum"]])
        self.start_vacuum()
        self.log("Vacuum started", log="vacuum")
      else:
        message = "Flor is ready to cleanup, but I can see that someone is in home. I will start vacuum in 5 min."
        self.notify_on_change(self.title, message, actions=[Actions["pospone"], Actions["cancel_postpone"]])
        self.vacuum_timer_handler = self.run_in(self.start_vacuum_event_handler, 300)
        self.log("Vacuum will start in 5 min.", log="vacuum")
    else:
      self.log(f"Nothing has hapened, vacuum {self.vacuum['attributes']['friendly_name']} is now {self.vacuum['state']}", log="vacuum")

  def vacuum_action(self, service, **kwargs):
    self.log(f"{service} for {kwargs}", log="vacuum")
    self.call_service(service, **kwargs)

  def start_vacuum(self):
    self.run_by_app = True
    self.vacuum_action("vacuum/start", entity_id=self.vacuum_entity)
    self.cancel_vacuum_timer(self.vacuum_timer_handler)
  def stop_vacuum(self):
    self.vacuum_action("vacuum/stop", entity_id=self.vacuum_entity)
  def pause_vacuum(self):
    self.vacuum_action("vacuum/pause", entity_id=self.vacuum_entity)
  def dock_vacuum(self):
    self.vacuum_action("vacuum/return_to_base", entity_id=self.vacuum_entity)
  def pause_vacuum_for(self, seconds):
    self.pause_vacuum()
    self.run_in(self.start_vacuum_event_handler, seconds)
  def go_to(self, pos):
    self.vacuum_action("vacuum/send_command", entity_id=self.vacuum_entity, command="app_goto_target", params=pos)

  def start_vacuum_event_handler(self, kwargs):
    self.start_vacuum()
  def dock_vacuum_event_handler(self, kwargs):
    self.dock_vacuum()

  def cancel_vacuum_timer(self, vacuum_timer):
    if vacuum_timer is not None:
      self.cancel_timer(vacuum_timer)

  def postpone_vacuum_timer(self, sec):
    if self.vacuum_timer_handler is not None:
      self.cancel_timer(self.vacuum_timer_handler)
    self.vacuum_timer_handler = self.run_in(self.start_vacuum_event_handler, sec)
    start = self.time() + "01:00:00"
    self.notify_on_change(title=self.title, message=f"Vacuuming postponed to {start}", actions=[Actions["start_vacuum"], Actions["return_vacuum"]])

  def notify_on_change(self, title, message, actions):
    # try:
    data = self.prepare_data_for_notify(actions=actions, tag=self.tag)
    for sender in self.notifiers:
      self.call_service(sender, title=title, message=message, data=data)
      self.log(f"Message \"{message}\" sent to {sender} with data={data}", log="vacuum")
    self.notify_by_tts_service(message)
    # except:
    #   self.log(f"Some data are missing sender={self.notifiers} title={title} message={message} actions={actions}", log="vacuum")
    #   return

  def notify_by_tts_service(self, message):
    service = self.args["tts_service"]
    devices = self.args["tts_devices"]
    occupancy = self.get_state(self.occupancy_entity)
    if service is not None and occupancy == 'home':
      for sender in devices:
        self.call_service(service, entity_id=sender, message=message)

  def prepare_data_for_notify(self, actions, tag, ttl=0, importance="default", chanel="vacuum", group="vacuum"):
    data = {
      "vibrationPattern": "200, 100, 200, 100, 200, 100, 200",
      "ttl": ttl,
      "importance": importance,
      "channel": chanel,
      "group": group,
      "actions": actions,
      "icon": "/local/images/icons/robot-vacuum.png"
      # "tag": tag
    }# self.log(data, log="vacuum")
    data["tag"] = tag
    return data

  def dismiss_by_tag(self, tag):
    self.call_service("html5/dismiss", data={"tag": tag})
  
  def _json_object_hook(self, d): return namedtuple('X', d.keys())(*d.values())
  def json2obj(self, data): return json.loads(data, object_hook=self._json_object_hook)

  def event_received(self, event_name, data, kwargs):
    if data != {}:
      event_data = data["event"]
      event_id = data["id"]
      event_received = datetime.datetime.now()
      self.log(f"Deconz event received from {event_id}. Event was: {event_data}", log="vacuum")
      self.set_state("sensor.deconz_event", state = event_id, attributes = {"event_data": event_data, "event_received": str(event_received)})
      if event_id in self.args['switch']:
        self.event_button(event_name, data, kwargs)
      else:
        self.log(f'Usuported device {event_id}', log="vacuum")
    else:
      self.log('Data is empty', log="vacuum")

  def vacuum_state_handle(self, entity, attribute, old, new, kwargs):
    self.vacuum = self.get_state(self.vacuum_entity, attribute="all")
    # self.log(f"VACUUM ENTITY AS OBJECT {self.vacuum}", log="vacuum")
    message = ""
    if (old != new):
      self.log(f"New vacuum state: {new} and attribute: {attribute}", log="vacuum")
      if new == "error":
        self.log(f"Error detected attribute for {entity}, the user has been informed", log="vacuum")
        self.notify_on_change(title=self.title, message="Vacuum encounter an problem", actions=[])
      elif new == "cleaning":
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        # if self.cleaned_area > int(float(self.args["area_before_emptying"])) and not self.going_to_be_emptyied:
        if not self.going_to_be_emptyied and self.ready_for_emptying:
          self.log(f"Vacuum is full and need to be emptied", log="vacuum")
          message = f"Vacuum cleaned area is {self.cleaned_area}, and probably is full of beans!!"
          self.notify_on_change(title=self.title, message=message, actions=[Actions["return_vacuum"], Actions["just_one_more"]])
          self.stop_vacuum()
          # self.ready_for_emptying = True
          # self.notify_by_tts(message)
        elif not self.run_by_app and old == "docked" and not self.going_to_be_emptyied:
          self.log(f"Vacuum started cleaning by unknown sourse, self.run_by_app: {self.run_by_app}", log="vacuum")
          message = f"Vacuum is now {new}, is it intended?"
          self.notify_on_change(title=self.title, message=message, actions=[Actions["stop_vacuum"], Actions["cancel"]])
          # self.notify_by_tts(message)
        elif self.going_to_be_emptyied:
          self.log(f"Vacuum is going to be emptyied", log="vacuum")
          message = f"Vacuum is going to be emptyied"
          self.notify_on_change(title=self.title, message=message, actions=[])
        else:
          self.log(f"Vacuum just started cleaning, no action required", log="vacuum")
      elif new == "returning":
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        actions = []
        if old == "cleaning":
          cleaned_area = self.vacuum["attributes"]["cleaned_area"]
          cleaning_time = self.vacuum["attributes"]["cleaning_time"]
          self.log(f"Vacuum cleaned area from last emptying: {self.cleaned_area} and type {type(self.cleaned_area)}\n and in the current time: {cleaned_area} and type {type(cleaned_area)}", log="vacuum")
          self.cleaned_area = self.cleaned_area + cleaned_area
          message = f"Vacuum has finished his work, cleaned {cleaned_area} m\u00b2 in {cleaning_time} min."
          if self.cleaned_area > int(float(self.args["area_before_emptying"])):
            message = message + f"You have nod emptied me that long, I'm almost full."
            actions = [Actions["stop_vacuum"], Actions["send_for_emptying"]]
            self.log(f"Vacuum require cleaning", log="vacuum")
            self.ready_for_emptying = True
          self.notify_on_change(title=self.title, message=message, actions=actions)
          self.ready_to_vacuum = False
        elif old == "idle":
          if self.waiting_for_emptying:
            self.log("Vacuum is now clear, returning home", log="vacuum")
            message = f"Vacuum is now clear, returning home."
            self.notify_on_change(title=self.title, message=message, actions=actions)
            self.vacuum_emptied()
          else:
            self.log("Vacuum returning home", log="vacuum")
            message = f"Vacuum returning home."
            self.notify_on_change(title=self.title, message=message, actions=actions)
        else:
          self.log(f"Hej!!!!!!!!! What just happened\n{self.vacuum}", log="vacuum")
      elif new == "docked":
        self.log(f"Vacuum is docked, user informed", log="vacuum")
        self.run_by_app = False
        self.cancel_vacuum_timer(self.vacuum_timer_handler)
        # if self.waiting_for_emptying:
        #   self.waiting_for_emptying = False
        #   self.set_value(self.cleaned_area_entity, value=0)
        # message == message + " and docked."
        # self.notify_on_change(title=self.title, message=message, actions=[])
      elif new == "idle":
        if self.going_to_be_emptyied:
          self.going_to_be_emptyied = False
          self.waiting_for_emptying = True
          self.log(f"Vacuum waiting to be emptyied!!", log="vacuum")
          message = f"Vacuum waiting to be emptyied!!"
          actions = [Actions["return_vacuum"]]
          self.notify_on_change(title=self.title, message=message, actions=actions)
        else:
          if not self.waiting_for_emptying:
            self.log(f"Vacuum is idle, will send it to dock in 300s", log="vacuum")
            self.vacuum_timer_handler = self.run_in(self.dock_vacuum_event_handler, 300)
      elif new == "paused":
        self.log(f"Vacuum new state: {new} and attribute {attribute}", log="vacuum")
        self.notify_on_change(title=self.title, message="The vacuum cleaner has been suspended", actions=[Actions["start_vacuum"], Actions["return_vacuum"]])
      else:
        self.log(f"Vacuum new state: {new} and attribute {attribute}", log="vacuum")
    else:
      self.log(f"New and old state are the same {new}", log="vacuum")

  def action_event_clicked(self, event_name, data, kwargs):
    event_action = data["action"]
    event_tag = data["tag"]
    self.log(f"Push notification clicked {event_action} with {data}", log="vacuum")
    if event_action == "start_vacuum":
      self.dismiss_by_tag(event_tag)
      self.start_vacuum()
    elif event_action == "just_one_more":
      self.dismiss_by_tag(event_tag)
      self.ready_for_emptying = False
      self.start_vacuum()
    elif event_action == "stop_vacuum":
      self.dismiss_by_tag(event_tag)
      self.stop_vacuum()
    elif event_action == "return_vacuum":
      self.dismiss_by_tag(event_tag)
      self.dock_vacuum()
    elif event_action == "send_for_emptying":
      self.dismiss_by_tag(event_tag)
      self.send_vacuum_for_emptying(None, None, None, None, kwargs)
    elif event_action == "cancel":
      self.dismiss_by_tag(event_tag)
    elif event_action == "pospone":
      self.dismiss_by_tag(event_tag)
      self.postpone_vacuum_timer(3600)
    elif event_action == "cancel_postpone":
      self.dismiss_by_tag(event_tag)
      self.cancel_vacuum_timer(self.vacuum_timer_handler)
      self.notify_on_change(title=self.title, message=f"Cancel pospone cleaning.", actions=[])
    elif event_action == "send_wen_in_home":
      self.dismiss_by_tag(event_tag)
    else:
      self.log(f"Unsupported action {event_action} with {data}", log="vacuum")
      pass

  def event_button(self, event_name, data, kwargs):
    event_data = data["event"]
    button = data['id']
    event_received = datetime.datetime.now()
    self.vacuum = self.get_state(self.vacuum_entity, attribute="all")
    self.log(f'Button {button} down, date {event_received}', log="vacuum")
    if button == self.args["switch"]:
      if event_data == 1002: #released
        self.log(f'Button {button} release, I\'m ready to cleanup')
        self.ready_to_vacuum = True
        self.log(f'Button {button} long click down, date {event_received}', log="vacuum")
      elif event_data == 1003: #long release
        self.log(f"self.waiting_for_emptying {self.waiting_for_emptying}", log="vacuum")
        if not self.waiting_for_emptying:
          self.log(f'Button {button} long click release.\n Vacuum waiting for emptying.', log="vacuum")
          self.send_vacuum_for_emptying(None, None, None, None, kwargs)
        elif self.waiting_for_emptying and self.vacuum["state"] in ["idle"]:
          self.log(f'Button {button} long click release, date {event_received}.\n Vacuum emptied, returning to base.', log="vacuum")
          self.return_to_base()
        else:
          self.log(f'Button {button} long click release, date {event_received}.\n unknown exact state.', log="vacuum")
      elif event_data == 1004: #double click
        if self.vacuum["state"] in ["cleaning"]:
          self.log(f'Button {button} double click, stoping cleanup immediately', log="vacuum")
          self.stop_vacuum()
        elif self.vacuum["state"] in ["docked", "idle", "paused"]:
          self.log(f'Button {button} double click, starting cleanup immediately', log="vacuum")
          self.start_vacuum()
        else:
          self.log(f'Button {button} double click, unsupported vacuum state: {self.vacuum}', log="vacuum")
      elif event_data > 1004 and event_data <= 1010: #multi click
        self.log(f'Button {button} multi click, panic button!! Stop and returning to dock', log="vacuum")
        if self.vacuum["state"] not in ["error", "idle", "paused"]:
          self.stop_vacuum()
        elif self.vacuum["state"] in ["idle", "paused"]:
          self.dock_vacuum()
      else:
        self.log(f'Button event {event_data} not supported, date {event_received}', log="vacuum")


Actions = {
    'start_vacuum': {
        "action": "start_vacuum",
        # "icon": "",
        "title": "Start Vacuum"
    },
    'stop_vacuum': {
        "action": "stop_vacuum",
        # "icon": "",
        "title": "Stop Vacuum"
    },
    'return_vacuum': {
        "action": "return_vacuum",
        # "icon": "",
        "title": "Return Vacuum"
    },
    'send_for_emptying': {
        "action": "send_for_emptying",
        # "icon": "",
        "title": "Send for emptying"
    },
    'just_one_more': {
        "action": "just_one_more",
        # "icon": "",
        "title": "Just one more time"
    },
    'pospone': {
        "action": "pospone",
        "title": "Pospone to 1h"
    },
    'cancel': {
        "action": "cancel",
        "title": "Cancel"
    },
    'cancel_postpone': {
        "action": "cancel_postpone",
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