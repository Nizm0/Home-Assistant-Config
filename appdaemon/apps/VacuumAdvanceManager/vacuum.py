import appdaemon.plugins.hass.hassapi as hass
import datetime
import json
import traceback
# from datetime import datetime
from collections import namedtuple
from base import Base
import globals
import voluptuous as vol
# from globals import Actions

# General

CONF_MODULE = 'module'
CONF_CLASS = 'class'
CONF_VACUUM = 'vacuum_entity'
CONF_TAG = 'tag'
CONF_TITLE = 'title'
CONF_VACUUM_TIME = 'vacuum_time_entity'
CONF_GOING_TO_BE_EMPTYIED = 'going_to_be_emptyied_entity'
CONF_READY_TO_VACUUM = 'ready_to_vacuum'
# CONF_VACUUM_NEEDS_EMPTYING_ENTITY = 'vacuum_needs_emptying_entity'
CONF_READY_FOR_EMPTYING_ENTITY = 'ready_for_emptying_entity'
# CONF_READY_TO_EMPTYING_VACUUM = 'ready_to_emptying_vacuum_entity'
CONF_WAITING_FOR_EMPTYING = 'waiting_for_emptying_entity'
CONF_WAITING_RETURN_HOME = 'waiting_return_home_entity'
CONF_CLEANED_AREA = 'cleaned_area'
CONF_OCCUPANCY = 'occupancy'
CONF_HOME_PRESET_SELECT = 'home_preset_select'
CONF_NOTIFIERS = 'notifiers'
CONF_TTS_SERVICE = 'tts_service'
CONF_TTS_DEVICES = 'tts_devices'
CONF_EMPTYING_LOCATION = 'emptying_location'
CONF_AREA_BEFORE_EMPTYING = 'area_before_emptying'
CONF_EVENTS_CONFIG = 'events_config'
CONF_SWITCH = 'switch'
CONF_SWITCH_LIST = 'switch_list'
CONF_ENTITY_LIST = 'entity_list'
CONF_LOG_LEVEL = 'log_level'
CONF_LOG_FILE = 'log_file'
CONF_X = 'x'
CONF_Y = 'y'

# Default values

DEFAULT_TITLE = 'Roborock'
DEFAULT_OCCUPANCY_ENTITY = 'group.family'
DEFAULT_CLEANED_AREA_ENTITY = 'input_number.vacuum_cleaned_area'
DEFAULT_VACUUM_TIME_ENTITY = 'input_datetime.vacuum_day_time'
DEFAULT_GOING_TO_BE_EMPTYIED_ENTITY = 'input_boolean.going_to_be_emptyied'
DEFAULT_HOME_PRESET_SELECT_ENTITY = 'input_select.home_preset'
DEFAULT_READY_TO_VACUUM_ENTITY = 'input_boolean.ready_to_vacuum'
# DEFAULT_VACUUM_NEEDS_EMPTYING_ENTITY = 'input_boolean.vacuum_needs_emptying'
DEFAULT_READY_FOR_EMPTYING_ENTITY = 'input_boolean.ready_for_emptying'
# DEFAULT_READY_TO_EMPTYING_VACUUM_ENTITY = 'input_boolean.ready_to_emptying_vacuum'
DEFAULT_WAITING_FOR_EMPTYING_ENTITY = 'input_boolean.waiting_for_emptying'
DEFAULT_WAITING_RETURN_HOME_ENTITY = 'input_boolean.waiting_return_home'

DEFAULT_MESSAGE_ICON = "/local/images/icons/robot-vacuum.png"

# Switch Option

CONF_NAME = 'name'
CONF_EVENT_TYPE = 'event_type'
CONF_DATA_ID_NAME = 'data_id_name'
CONF_EVENT_DATA = 'event_data'
CONF_EVENT_DATA_NAME = 'event_data_name'
CONF_ID = 'id'
CONF_STATE = 'state'
CONF_STATE_DATA= 'state_data'

CONF_READY_TO_VACUUM = 'ready_to_vacuum'
CONF_START_STOP_VACUUM = 'start_stop_vacuum'
CONF_CLEAN_VACUUM = 'clean_vacuum'
CONF_EMERGENCY_STOP = 'emergency_stop'
CONF_TEST_MESSAGE = 'send_test_message'

CONF_ACTION = 'action'
CONF_EVENT = 'event'
CONF_ENTITY = 'entity'
# input_select

CONF_EMPTY = 'Empty'

# PEOPLE_TRACKER_ENTITY_ID = 'sensor.people_tracker'
DEFAULT_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'

# logs

LOG_ERROR = 'ERROR'
LOG_DEBUG = 'DEBUG'
LOG_INFO = 'INFO'
LOG_FILE = 'default'

# Attributes
ATTRIBUTE_FRIENDLY_NAME = 'friendly_name'
ATTRIBUTE_WHO = 'who'
ATTRIBUTE_DEVICE_CLASS = 'device_class'

STATE = 'state'
ATTRIBUTES = 'attributes'

INTRUDER = 'intruder'

TIMER_STATE = 'timer_state'
TIMER_OBJECT = 'timer_object'

DOMAIN ='domain'
SERVICE = 'service'

# Schemas

SWITCH_EVENT_ACTION_SCHEMA = {
  vol.Required(CONF_ACTION): vol.Any(CONF_READY_TO_VACUUM, CONF_START_STOP_VACUUM, CONF_CLEAN_VACUUM, CONF_EMERGENCY_STOP, CONF_TEST_MESSAGE),
  vol.Required(CONF_EVENT): str
}

SWITCH_ENTITY_ACTION_SCHEMA = {
  vol.Required(CONF_ACTION): vol.Any(CONF_READY_TO_VACUUM, CONF_START_STOP_VACUUM, CONF_CLEAN_VACUUM, CONF_EMERGENCY_STOP, CONF_TEST_MESSAGE),
  vol.Required(CONF_STATE): str
}

EVENT_SCHEMA = {
  vol.Required(CONF_NAME): str,
  vol.Required(CONF_EVENT_TYPE): str,
  vol.Required(CONF_DATA_ID_NAME): str,
  vol.Required(CONF_EVENT_DATA_NAME): str,
  vol.Required(CONF_EVENT_DATA): [SWITCH_EVENT_ACTION_SCHEMA]
}

ENTITY_SCHEMA = {
  vol.Required(CONF_ID): str,
  vol.Required(CONF_STATE_DATA): [SWITCH_ENTITY_ACTION_SCHEMA]
}

EVENTS_CONFIG_SCHEMA = {
  vol.Optional(CONF_SWITCH_LIST): [EVENT_SCHEMA],
  vol.Optional(CONF_ENTITY_LIST): [ENTITY_SCHEMA]
}

LOCATION_SCHEMA = {
  vol.Required(CONF_X): int,
  vol.Required(CONF_Y): int
}

APP_SCHEMA = vol.Schema({
  vol.Required(CONF_MODULE): str,
  vol.Required(CONF_CLASS): str,
  vol.Required(CONF_VACUUM): str,
  vol.Required(CONF_TAG): str,
  vol.Optional(CONF_TITLE, default=DEFAULT_TITLE): str,
  vol.Optional(CONF_VACUUM_TIME, default=DEFAULT_VACUUM_TIME_ENTITY): str,
  vol.Optional(CONF_READY_TO_VACUUM, default=DEFAULT_READY_TO_VACUUM_ENTITY): str,
  vol.Optional(CONF_HOME_PRESET_SELECT, default=DEFAULT_HOME_PRESET_SELECT_ENTITY): str,
  vol.Optional(CONF_WAITING_FOR_EMPTYING, default=DEFAULT_WAITING_FOR_EMPTYING_ENTITY): str,
  vol.Optional(CONF_GOING_TO_BE_EMPTYIED, default=DEFAULT_GOING_TO_BE_EMPTYIED_ENTITY): str,
  vol.Optional(CONF_WAITING_RETURN_HOME, default=DEFAULT_WAITING_RETURN_HOME_ENTITY): str,
  vol.Optional(CONF_READY_FOR_EMPTYING_ENTITY, default=DEFAULT_READY_FOR_EMPTYING_ENTITY): str,
  # vol.Optional(CONF_VACUUM_NEEDS_EMPTYING_ENTITY, default=DEFAULT_VACUUM_NEEDS_EMPTYING_ENTITY): str,
  vol.Optional(CONF_CLEANED_AREA, default=DEFAULT_CLEANED_AREA_ENTITY): str,
  vol.Optional(CONF_OCCUPANCY, default=DEFAULT_OCCUPANCY_ENTITY): str,
  vol.Optional(CONF_NOTIFIERS): [str],
  vol.Optional(CONF_TTS_SERVICE): str,
  vol.Optional(CONF_TTS_DEVICES): [str],
  vol.Optional(CONF_EMPTYING_LOCATION): LOCATION_SCHEMA,
  vol.Optional(CONF_AREA_BEFORE_EMPTYING, default=100): int,
  vol.Optional(CONF_EVENTS_CONFIG): EVENTS_CONFIG_SCHEMA,
  # vol.Optional(CONF_SWITCH): SWITCH_SCHEMA,
  # vol.Required(CONF_PEOPLE_TRACKER, default=PEOPLE_TRACKER_ENTITY_ID): str,
  # vol.Optional(CONF_NOTIFY): NOTIFY_SCHEMA,
  vol.Optional(CONF_LOG_LEVEL, default=LOG_DEBUG): vol.Any(LOG_INFO, LOG_DEBUG),
  vol.Optional(CONF_LOG_FILE, default=LOG_FILE): str
  })

class VacuumAdvanceManager(Base):

  def initialize(self):
    
    args = APP_SCHEMA(self.args)
    
    self._level = args.get(CONF_LOG_LEVEL)
    self._log_file = args.get(CONF_LOG_FILE)
    self.run_by_app = False
    self.counter = 0

    self.log(f'Fresh start of vacuum Appdaemon app', log=self._log_file, level=self._level)
    self.log(args, log=self._log_file, level=self._level)

    self._title = args.get(CONF_TITLE)
    self._tag = args.get(CONF_TAG)
    self._vacuum_entity = args.get(CONF_VACUUM)
    self._vacuum_time_entity = args.get(CONF_VACUUM_TIME)
    self._occupancy_entity = args.get(CONF_OCCUPANCY)
    self._cleaned_area_entity = args.get(CONF_CLEANED_AREA)
    self._ready_to_vacuum_entity = args.get(CONF_READY_TO_VACUUM)
    self._ready_for_emptying_entity = args.get(CONF_READY_FOR_EMPTYING_ENTITY)
    # self._vacuum_neads_emptying = args.get(CONF_VACUUM_NEEDS_EMPTYING_ENTITY)
    self._waiting_for_emptying_entity = args.get(CONF_WAITING_FOR_EMPTYING)
    self._going_to_be_emptyied_entity = args.get(CONF_GOING_TO_BE_EMPTYIED)
    self._waiting_return_home_entity = args.get(CONF_WAITING_RETURN_HOME)
    # self._ready_to_emptying_vacuum_entity = args.get(CONF_READY_TO_EMPTYING_VACUUM)
    
    self._switches = []
    for switch in args.get(CONF_EVENTS_CONFIG).get(CONF_SWITCH_LIST, {}):
      self.log(f"One item from list switch {switch}", log=self._log_file, level=self._level)
      self._switches.append(Switch(switch))
      self.listen_event(self.event_received, switch.get(CONF_EVENT_TYPE))
    # for s in self._switches:
    #   self.log(f"switch list {s.name} with actions {s._actions}", log=self._log_file, level=self._level)

    self._entites = []
    for entity in args.get(CONF_EVENTS_CONFIG).get(CONF_ENTITY_LIST, {}):
      self.log(f"One item from list entity {entity}", log=self._log_file, level=self._level)
      self._entites.append(Entity(entity))
      self.listen_state(self.entity_state_changed, entity.get(CONF_ID))

    self._home_preset_select = args.get(CONF_HOME_PRESET_SELECT)
    self._notifiers = args.get(CONF_NOTIFIERS)
    self._vacuum_daily = None
    self._vacuum_timer_handler = None

    self._emptying_location = [args.get(CONF_EMPTYING_LOCATION).get(CONF_X), args.get(CONF_EMPTYING_LOCATION).get(CONF_Y)]
    self._area_before_emptying = args.get(CONF_AREA_BEFORE_EMPTYING)
    
    self._vacuum = self.get_state(self._vacuum_entity, attribute="all")

    self.set_run_daily(self, self._vacuum_time_entity, '', self.get_state(self._vacuum_time_entity), '')
    # self.listen_state(self.cleaned_area_changed, self._cleaned_area_entity)
    self.listen_state(self.change_run_daily, self._vacuum_time_entity)
    self.listen_state(self.vacuum_state_handle, self._vacuum_entity)
    self.listen_event(self.action_event_clicked, "html5_notification.clicked", tag=self._tag)
    self.listen_event(self.action_event_clicked, "mobile_app_notification_action", tag=self._tag)
    # if self._switch_name is not None:
    #   self.log(f'New even listener: {self._switch_name}, date {self._switch_event_name}', log=self._log_file, level=self._level)
    #   self.listen_event(self.event_received, self._switch_event_name)

  @property
  def ready_to_vacuum(self):
    self.__ready_to_vacuum = self.__convert_on_off_to_boolean(self.get_state(self._ready_to_vacuum_entity))
    self.log(f"read self.ready_to_vacuum {self.__ready_to_vacuum}", log=self._log_file, level=self._level)
    return self.__ready_to_vacuum

  @ready_to_vacuum.setter
  def ready_to_vacuum(self, value):
    self.__ready_to_vacuum = value
    self.__turn_on_off_input_boolean(value, self._ready_to_vacuum_entity)
    self.log(f"write self.ready_to_vacuum {self.__ready_to_vacuum}", log=self._log_file, level=self._level)

  @property
  def ready_for_emptying(self):
    self.__ready_for_emptying = self.__convert_on_off_to_boolean(self.get_state(self._ready_for_emptying_entity))
    self.log(f"read self.ready_for_emptying {self.__ready_for_emptying}", log=self._log_file, level=self._level)
    return self.__ready_for_emptying

  @ready_for_emptying.setter
  def ready_for_emptying(self, value):
    self.__ready_for_emptying = value
    self.__turn_on_off_input_boolean(value, self._ready_for_emptying_entity)
    self.log(f"write self.ready_for_emptying {self.__ready_for_emptying}", log=self._log_file, level=self._level)

  @property
  def waiting_for_emptying(self):
    self.__waiting_for_emptying = self.__convert_on_off_to_boolean(self.get_state(self._waiting_for_emptying_entity))
    self.log(f"read self.waiting_for_emptying {self.__waiting_for_emptying}", log=self._log_file, level=self._level)
    return self.__waiting_for_emptying

  @waiting_for_emptying.setter
  def waiting_for_emptying(self, value):
    self.__waiting_for_emptying = value
    self.__turn_on_off_input_boolean(value, self._waiting_for_emptying_entity)
    self.log(f"write self.waiting_for_emptying {self.__waiting_for_emptying}", log=self._log_file, level=self._level)

  @property
  def going_to_be_emptyied(self):
    self.__going_to_be_emptyied = self.__convert_on_off_to_boolean(self.get_state(self._going_to_be_emptyied_entity))
    self.log(f"read self.going_to_be_emptyied {self.__going_to_be_emptyied}", log=self._log_file, level=self._level)
    return self.__going_to_be_emptyied

  @going_to_be_emptyied.setter
  def going_to_be_emptyied(self, value):
    self.__going_to_be_emptyied = value
    self.__turn_on_off_input_boolean(value, self._going_to_be_emptyied_entity)
    self.log(f"write self.going_to_be_emptyied {self.__going_to_be_emptyied}", log=self._log_file, level=self._level)

  @property
  def waiting_return_home(self):
    self.__waiting_return_home = self.__convert_on_off_to_boolean(self.get_state(self._waiting_return_home_entity))
    self.log(f"read self.waiting_return_home {self.__waiting_return_home}", log=self._log_file, level=self._level)
    return self.__waiting_return_home

  @waiting_return_home.setter
  def waiting_return_home(self, value):
    self.__waiting_return_home = value
    self.__turn_on_off_input_boolean(value, self._waiting_return_home_entity)
    self.log(f"write self.waiting_return_home {self.__waiting_return_home}", log=self._log_file, level=self._level)

  # @property
  # def vacuum_neads_emptying(self):
  #   self.__vacuum_neads_emptying = self.self.__convert_on_off_to_boolean(self.get_state(self._vacuum_neads_emptying))
  #   self.log(f"read self.vacuum_neads_emptying {self.__vacuum_neads_emptying}", log=self._log_file, level=self._level)
  #   return self.__vacuum_neads_emptying

  # @vacuum_neads_emptying.setter
  # def vacuum_neads_emptying(self, value):
  #   self.__vacuum_neads_emptying = value
  #   self.__turn_on_off_input_boolean(value, self._vacuum_neads_emptying)
  #   self.log(f"write self.vacuum_neads_emptying {self.__vacuum_neads_emptying}", log=self._log_file, level=self._level)

  @property
  def cleaned_area(self):
    self.__cleaned_area = int(float(self.get_state(self._cleaned_area_entity)))
    self.log(f"read self.cleaned_area {self.__cleaned_area}", log=self._log_file, level=self._level)
    return self.__cleaned_area

  @cleaned_area.setter
  def cleaned_area(self, value):
    self.__cleaned_area = value
    self.set_value(self._cleaned_area_entity, value=value)
    self.log(f"write self.cleaned_area {self.__cleaned_area}", log=self._log_file, level=self._level)

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
    self.log(f"send_vacuum_for_emptying - self.going_to_be_emptyied: {self.going_to_be_emptyied}", log=self._log_file, level=self._level)
    self.ready_for_emptying = False
    self.going_to_be_emptyied = True
    self.vacuum_action("vacuum/send_command", entity_id=self._vacuum_entity, command="app_goto_target", params=self._emptying_location)

  def vacuum_emptied(self):
    self.log('Vacuum emptied, returning to dock')
    self.waiting_for_emptying = False
    self.cleaned_area = 0
    # self.dock_vacuum()

  def set_run_daily(self, entity, attribute, old, new, kwargs):
    self.input_time = datetime.time.fromisoformat(new)
    self._vacuum_daily = self.run_daily(self.run_daily_callback, self.input_time)
    self.counter = self.counter + 1
    self.log(f"Reinitialize run daily for {self.counter} time with {self.input_time}", log=self._log_file, level=self._level)

  def change_run_daily(self, entity, attribute, old, new, kwargs):
    self.cancel_vacuum_timer(self._vacuum_daily)
    self.log(f"Cancel previous timer at {old}", log=self._log_file, level=self._level)
    self.set_run_daily(entity, attribute, old, new, kwargs)

  def run_daily_callback(self, kwargs):
    self.log("Run daily vacuum", log=self._log_file, level=self._level)
    self._vacuum = self.get_state(self._vacuum_entity, attribute="all")
    # ready = self.get_state(self._ready_to_vacuum_entity)
    occupancy_state = self.get_state(self._occupancy_entity)
    home_preset = self.get_state(self._home_preset_select)
    clean_start = datetime.datetime.strptime(self._vacuum['attributes']['clean_start'], DEFAULT_TIMESTAMP_FORMAT).date()
    today = clean_start == datetime.date.today()
    message = ""
    if self._vacuum["state"] not in ["cleaning", "error", "returning"]:
      if not self.ready_to_vacuum:
        message = "Flor is not ready to cleanup"
        if not today:
          message = message + " and no one vacuums it"
        message = message + ". Did you forget about me?"
        self.notify_on_change(self._title, message, actions=[Actions["start_vacuum"], Actions["cancel"]])
        self.log("Flor is not ready, wainting for response.", log=self._log_file, level=self._level)
      elif self.ready_for_emptying:
        message = f"Hey, time for daily cleaning, but I'm full. Could you please clean me up?"
        self.notify_on_change(self._title, message, actions=[Actions["send_for_emptying"]])
        self.log(f"Vacuum is full, {self.cleaned_area}m\u00b2 cleaned from last emptying. User notified", log=self._log_file, level=self._level)
      elif occupancy_state == 'not_home' and home_preset == CONF_EMPTY:
        message = "Started daily Cleanup"
        self.notify_on_change(self._title, message, actions=[Actions["return_vacuum"]])
        self.start_vacuum()
        self.log("Vacuum started", log=self._log_file, level=self._level)
      else:
        message = "Flor is ready to cleanup, but I can see that someone is in home. I will start vacuum in 5 min."
        self.notify_on_change(self._title, message, actions=[Actions["start_vacuum"], Actions["pospone"], Actions["cancel_postpone"]])
        self._vacuum_timer_handler = self.run_in(self.start_vacuum_event_handler, 300)
        self.log("Vacuum will start in 5 min.", log=self._log_file, level=self._level)
    else:
      self.log(f"Nothing has hapened, vacuum {self._vacuum['attributes']['friendly_name']} is now {self._vacuum['state']}", log=self._log_file, level=self._level)

  def vacuum_action(self, service, **kwargs):
    self.log(f"{service} for {kwargs}", log=self._log_file, level=self._level)
    self.call_service(service, **kwargs)

  def start_vacuum(self):
    self.run_by_app = True
    self.vacuum_action("vacuum/start", entity_id=self._vacuum_entity)
    self.cancel_vacuum_timer(self._vacuum_timer_handler)
  def stop_vacuum(self):
    self.vacuum_action("vacuum/stop", entity_id=self._vacuum_entity)
  def pause_vacuum(self):
    self.vacuum_action("vacuum/pause", entity_id=self._vacuum_entity)
  def dock_vacuum(self):
    self.vacuum_action("vacuum/return_to_base", entity_id=self._vacuum_entity)
  def pause_vacuum_for(self, seconds):
    self.pause_vacuum()
    self.run_in(self.start_vacuum_event_handler, seconds)
  def go_to(self, pos):
    self.vacuum_action("vacuum/send_command", entity_id=self._vacuum_entity, command="app_goto_target", params=pos)

  def start_vacuum_event_handler(self, kwargs):
    self.start_vacuum()
  def dock_vacuum_event_handler(self, kwargs):
    self.dock_vacuum()

  def cancel_vacuum_timer(self, vacuum_timer):
    if vacuum_timer is not None:
      self.cancel_timer(vacuum_timer)

  def postpone_vacuum_timer(self, sec):
    if self._vacuum_timer_handler is not None:
      self.cancel_timer(self._vacuum_timer_handler)
    self._vacuum_timer_handler = self.run_in(self.start_vacuum_event_handler, sec)
    start = self.time() + "01:00:00"
    self.notify_on_change(title=self._title, message=f"Vacuuming postponed to {start}", actions=[Actions["start_vacuum"], Actions["return_vacuum"]])

  def notify_on_change(self, title, message, actions, deep=1):
    try:
      data = self.prepare_data_for_notify(actions=actions, tag=self._tag)
      for sender in self._notifiers:
        self.call_service(sender, title=title, message=message, data=data)
        self.log(f"Message \"{message}\" with title \"{title}\"sent to \"{sender}\" with data {data}", log=self._log_file, level=self._level)
      self.notify_by_tts_service(message)
    except TimeoutError:
      if deep <= 5:
        self.log(f"Notification error faild. Retry send for {deep}", log=self._log_file, level=self._level)
        self.notify_on_change(title, message, actions, deep+1)
      else:
        self.log(f"Notification error faild. tryed {deep} without success.", log=self._log_file, level=self._level)
      return
    except:
      self.log(f"Some data are missing sender={self._notifiers} title={title} message={message} actions={actions}", log=self._log_file, level=self._level)
      return

  def notify_by_tts_service(self, message):
    service = self.args.get("tts_service")
    devices = self.args.get("tts_devices")
    occupancy_state = self.get_state(self._occupancy_entity)
    if service is not None and occupancy_state == 'home':
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
      "icon": DEFAULT_MESSAGE_ICON
      # "tag": tag
    }# self.log(data, log=self._log_file, level=self._level)
    data["tag"] = tag
    return data

  def dismiss_by_tag(self, tag):
    self.call_service("html5/dismiss", data={"tag": tag})
  
  def _json_object_hook(self, d): return namedtuple('X', d.keys())(*d.values())
  def json2obj(self, data): return json.loads(data, object_hook=self._json_object_hook)

  def event_received(self, event_name, data, kwargs):
    self.log(f'Event name {event_name} and data {data}', log=self._log_file, level=self._level)
    for switch in self._switches:
      if event_name == switch.event_type and switch.name == data[switch.data_id_name]:
        self.log(f'{event_name} = {switch.event_type} Switch name {switch.name} = {data[switch.data_id_name]}', log=self._log_file, level=self._level)
        self.execute_button_action(str(switch.action(data)), kwargs)

  def entity_state_changed(self, entity, attribute, old, new, kwargs):
    self.log(f'Entity name {entity} state changed to {new}', log=self._log_file, level=self._level)
    for _entity in self._entites:
      if entity == _entity.id:
        self.log(f'Entity id {_entity.id} = {entity}', log=self._log_file, level=self._level)
        self.execute_button_action(_entity.action(new), kwargs)
    pass

  def execute_button_action(self, action, kwargs):
    method_name = ''
    event_time = datetime.datetime.now()
    try:
      # self.log(f'invoked data {data},\nevent: {switch.event_data_name}\nlist of keys {switch._actions.keys()}', log=self._log_file, level=self._level)
      method_name = 'button_action_' + action
      method = getattr(self, method_name, lambda: 'Invalid')
      self.log(f'invoked methot {method_name} at date {event_time}', log=self._log_file, level=self._level)
      return method(kwargs)
    except ValueError:
      pass
    except SyntaxError:
      pass
    except Exception as inst:
      self.log(f"Function {method_name} not exists,\nerror {inst}\n{traceback.format_exc()}", log=self._log_file, level=LOG_ERROR)

  def button_action_ready_to_vacuum(self, kwargs):
    self.log(f'I\'m ready to cleanup', log=self._log_file, level=self._level)
    self.ready_to_vacuum = True
  def button_action_clean_vacuum(self, kwargs):
    __vacuum_state = self._vacuum["state"]
    if not self.waiting_for_emptying:
      self.log(f'Vacuum waiting for emptying.', log=self._log_file, level=self._level)
      self.send_vacuum_for_emptying(None, None, None, None, kwargs)
    elif self.waiting_for_emptying and __vacuum_state in ["idle"]:
      self.log(f'Vacuum emptied, returning to base.', log=self._log_file, level=self._level)
      self.dock_vacuum()
    else:
      self.log(f'Unknown exact action state.', log=self._log_file, level=self._level)
  def button_action_start_stop_vacuum(self, kwargs):
    __vacuum_state = self._vacuum["state"]
    if __vacuum_state in ["cleaning"]:
      self.log(f'Stoping cleanup immediately', log=self._log_file, level=self._level)
      self.stop_vacuum()
    elif __vacuum_state in ["docked", "idle", "paused"]:
      self.log(f'Starting cleanup immediately', log=self._log_file, level=self._level)
      self.start_vacuum()
    else:
      self.log(f'Unsupported vacuum state: {self._vacuum}', log=self._log_file, level=self._level)
  def button_action_emergency_stop(self, kwargs):
    self.log(f'Panic button!! Stop or return to dock', log=self._log_file, level=self._level)
    __vacuum_state = self._vacuum["state"]
    if __vacuum_state not in ["error", "idle", "paused"]:
      self.stop_vacuum()
    elif __vacuum_state in ["idle", "paused"]:
      self.dock_vacuum()
    else:
      self.log(f'{__vacuum_state} User action is required', log=self._log_file, level=self._level)
  def button_action_send_test_message(self, kwargs):
    self.log(f'Test message command induced', log=self._log_file, level=self._level)
    self.notify_on_change(title=self._title, message=f"test message", actions=[])

  def vacuum_state_handle(self, entity, attribute, old, new, kwargs):
    self._vacuum = self.get_state(self._vacuum_entity, attribute="all")
    # self.log(f"VACUUM ENTITY AS OBJECT {self._vacuum}", log=self._log_file, level=self._level)
    message = ""
    if (old != new):
      self.log(f"New vacuum state: {new} and attribute: {attribute}", log=self._log_file, level=self._level)
      if new == "error":
        self.log(f"Error detected attribute for {entity}, the user has been informed", log=self._log_file, level=self._level)
        self.notify_on_change(title=self._title, message="Vacuum encounter an problem", actions=[])
      elif new == "cleaning":
        self.cancel_vacuum_timer(self._vacuum_timer_handler)
        if not self.going_to_be_emptyied and self.ready_for_emptying:
          self.log(f"Vacuum is full and need to be emptied", log=self._log_file, level=self._level)
          message = f"Vacuum cleaned area is {self.cleaned_area}, and probably is full of beans!!"
          self.notify_on_change(title=self._title, message=message, actions=[Actions["return_vacuum"], Actions["just_one_more"]])
          self.stop_vacuum()
          # self.ready_for_emptying = True
          # self.notify_by_tts(message)
        elif not self.run_by_app and old == "docked" and not self.going_to_be_emptyied:
          self.log(f"Vacuum started cleaning by unknown sourse, self.run_by_app: {self.run_by_app}", log=self._log_file, level=self._level)
          message = f"Vacuum is now {new}, is it intended?"
          self.notify_on_change(title=self._title, message=message, actions=[Actions["stop_vacuum"], Actions["cancel"]])
          # self.notify_by_tts(message)
        elif self.going_to_be_emptyied:
          self.log(f"Vacuum is going to be emptyied", log=self._log_file, level=self._level)
          message = f"Vacuum is going to be emptyied"
          self.notify_on_change(title=self._title, message=message, actions=[])
        else:
          self.log(f"Vacuum just started cleaning, no action required", log=self._log_file, level=self._level)
      elif new == "returning":
        self.cancel_vacuum_timer(self._vacuum_timer_handler)
        actions = []
        if old == "cleaning":
          cleaned_area = self._vacuum["attributes"]["cleaned_area"]
          cleaning_time = self._vacuum["attributes"]["cleaning_time"]
          self.log(f"Vacuum cleaned area from last emptying: {self.cleaned_area} and type {type(self.cleaned_area)}\n and in the current time: {cleaned_area} and type {type(cleaned_area)}", log=self._log_file, level=self._level)
          self.cleaned_area = self.cleaned_area + cleaned_area
          message = f"Vacuum has finished his work, cleaned {cleaned_area} m\u00b2 in {cleaning_time} min."
          if self.cleaned_area > self._area_before_emptying:
            message = message + f"You have nod emptied me that long, I'm almost full."
            actions = [Actions["stop_vacuum"], Actions["send_for_emptying"]]
            self.log(f"Vacuum require cleaning", log=self._log_file, level=self._level)
            self.ready_for_emptying = True
          self.notify_on_change(title=self._title, message=message, actions=actions)
          self.ready_to_vacuum = False
        elif old == "idle":
          if self.waiting_for_emptying:
            self.log("Vacuum is now clear, returning home", log=self._log_file, level=self._level)
            message = f"Vacuum is now clear, returning home."
            self.notify_on_change(title=self._title, message=message, actions=actions)
            self.vacuum_emptied()
          else:
            self.log("Vacuum returning home", log=self._log_file, level=self._level)
            message = f"Vacuum returning home."
            self.notify_on_change(title=self._title, message=message, actions=actions)
        else:
          self.log(f"Hej!!!!!!!!! What just happened\n{self._vacuum}", log=self._log_file, level=self._level)
      elif new == "docked":
        self.log(f"Vacuum is docked, user informed", log=self._log_file, level=self._level)
        self.run_by_app = False
        self.cancel_vacuum_timer(self._vacuum_timer_handler)
        # if self.waiting_for_emptying:
        #   self.waiting_for_emptying = False
        #   self.set_value(self._cleaned_area_entity, value=0)
        # message == message + " and docked."
        # self.notify_on_change(title=self._title, message=message, actions=[])
      elif new == "idle":
        if self.going_to_be_emptyied:
          self.going_to_be_emptyied = False
          self.waiting_for_emptying = True
          self.log(f"Vacuum waiting to be emptyied!!", log=self._log_file, level=self._level)
          message = f"Vacuum waiting to be emptyied!!"
          actions = [Actions["return_vacuum"]]
          self.notify_on_change(title=self._title, message=message, actions=actions)
        else:
          if not self.waiting_for_emptying:
            self.log(f"Vacuum is idle, will send it to dock in 300s", log=self._log_file, level=self._level)
            self._vacuum_timer_handler = self.run_in(self.dock_vacuum_event_handler, 300)
      elif new == "paused":
        self.log(f"Vacuum new state: {new} and attribute {attribute}", log=self._log_file, level=self._level)
        self.notify_on_change(title=self._title, message="The vacuum cleaner has been suspended", actions=[Actions["start_vacuum"], Actions["return_vacuum"]])
      else:
        self.log(f"Vacuum new state: {new} and attribute {attribute}", log=self._log_file, level=self._level)
    else:
      self.log(f"New and old state are the same {new}", log=self._log_file, level=self._level)

  def action_event_clicked(self, event_name, data, kwargs):
    event_action = data["action"]
    event_tag = data["tag"]
    self.log(f"Push notification clicked {event_action} with {data}", log=self._log_file, level=self._level)
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
      self.cancel_vacuum_timer(self._vacuum_timer_handler)
      self.notify_on_change(title=self._title, message=f"Cancel pospone cleaning.", actions=[])
    elif event_action == "send_wen_in_home":
      self.dismiss_by_tag(event_tag)
    else:
      self.log(f"Unsupported action {event_action} with {data}", log=self._log_file, level=self._level)
      pass

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

class Switch(object):
  def __init__(self, args):
    self.name = args[CONF_NAME]
    self.event_data_name = str(args[CONF_EVENT_DATA_NAME])
    self.event_type = args[CONF_EVENT_TYPE]
    self.data_id_name = args[CONF_DATA_ID_NAME]
    self._event_data_list = args[CONF_EVENT_DATA]
    self._actions = {}

    for e in self._event_data_list:
      self._actions[e[CONF_EVENT]] = e[CONF_ACTION]

  def action(self, data):
    if self.event_data_name in data.keys():
      action = str(data[self.event_data_name])
      if action in self._actions:
        return str(self._actions[action])
      else:
        raise ValueError(f'Not supported action: {action}')
    else:
      raise ValueError(f'Not suported event name: {self.event_data_name}')

class Entity(object):
  def __init__(self, args):
    self.id = args[CONF_ID]
    self._state_data_list = args[CONF_STATE_DATA]
    self._actions = {}

    for s in self._state_data_list:
      self._actions[s[CONF_STATE]] = s[CONF_ACTION]

  def action(self, state):
    # action = str(state)
    if state in self._actions:
      return str(self._actions[state])
    else:
      raise ValueError(f'Not supported action: {state}')

class SwitchEventData(object):
  def __init__(self, action, event):
    self.action = action
    self.event = event

class EntityStateData(object):
  def __init__(self, action, state):
    self.action = action
    self.state = state