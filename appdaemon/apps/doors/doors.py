import appdaemon.plugins.hass.hassapi as hass
import re
from datetime import datetime, timedelta

class DoorsManager(hass.Hass):

  def initialize(self):
    self.timer_library = {}

    entities_to_monitor = []
    if 'binary_sensor' in self.args:
      entities_to_monitor.extend(self.args['binary_sensor'].split(','))
    elif 'sensors_to_monitor' in self.args:
      entities_to_monitor.extend(self.args['sensors_to_monitor'].split(','))

    for entity_type in entities_to_monitor:
      self._add_tracker(entity_name=entity_type)

    self.listen_event(self.add_tracker, 'monitor_add_tracker')

  def add_tracker(self, event_name, data, kwargs):

    try:
      entity_name = data['entity_name']
    except KeyError:
      self.error("You must supply a valid entity_name!")
      return

    if 'ttl' in data:
      ttl = data['ttl']
    else:
      ttl = None

    self._add_tracker(entity_name=entity_name, ttl=ttl)

  def _add_tracker(self, entity_name, ttl=None):
    """ Add a tracker for entity_id, optionally setting a ttl """
    
    try:
      self._check_entity(entity=entity_name, namespace=entity_name.split('.')[0])
      entities = [entity_name]
    except ValueError:
      try:
        re_entity = re.compile(".*({}).*".format(entity_name))
        entities = [entity for entity in self.get_state() if re_entity.match(entity)
                                                          if 'group' not in entity]
      except re.error:
        self.error("{} is not a valid entity name or RegEx string.".format(entity_name))
        return

    if not ttl:
      ttl = self.args['ttl']

    for entity in entities:
      self.listen_state(self.tracker, entity=entity, ttl=ttl)

  def tracker(self, entity, attribute, old, new, kwargs):

    try:
      self.cancel_timer(self.timer_library[entity])
    except KeyError:
      self.log('Tried to cancel a timer for {}, but none existed!'.format(entity), 
                  level='DEBUG')

    if new in ['on', 'open']:
      self.timer_library[entity] = self.run_in(self.notifier, 
                                    seconds=int(kwargs['ttl']),
                                    entity_name=entity,
                                    ttl=kwargs['ttl'],
                                    entity_state=new,
                                    delay=0)

  def notifier(self, kwargs):
    friendly_name = self.get_state(kwargs['entity_name'], attribute='friendly_name')
    last_seen = datetime.now() - timedelta(seconds=int(kwargs['ttl']))

    title = "Message from HASS".format(friendly_name)
    message = ("[{}] {} has been {} for more than {} seconds."
                .format(last_seen.strftime('%H:%M:%S'), friendly_name, 
                        kwargs['entity_state'], kwargs['ttl']))
    data = {
          "renotify": "true",
          "priority": "high",
          "tag": "home-door-notifications-appdaemon"
        }
    self.call_service('notify/push_to_chrome_nizm0_oneplus3', title=title, message=message, data=data)