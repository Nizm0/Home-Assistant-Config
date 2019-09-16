import appdaemon.plugins.hass.hassapi as hass
import datetime
from datetime import datetime

class DeconzHelper(hass.Hass):

  def initialize(self) -> None:
    self.listen_event(self.event_received, "deconz_event")
    for sensor in self.args["motions"]:
      # self._check_entity(entity=sensor, namespace=sensor.split('.')[0])
      # self.listen_state(self.motion_listener, sensor)
      self.log(f"State listener set for {sensor}")
    # if 'event' in self.args:
    #     self.listen_event(self.handle_event, self.args['event'])

  def event_received(self, event_name, data, kwargs):
    if data != {}:
      event_data = data["event"]
      event_id = data["id"]
      event_received = datetime.now()
      self.log("fDeconz event received from {event_id}. Event was: {event_data}")
      # self.set_state("sensor.deconz_event", state = event_id, attributes = {"event_data": event_data, "event_received": str(event_received)})
      if data["id"] in self.args['switch']:
        self.event_button(event_name, data, kwargs)
      elif data["id"] in self.args['cube']:
        self.event_qube(event_name, data, kwargs)
      else:
        self.log('Unknown device')
    else:
      self.log('Data is empty')

  def motion_listener(self, entity, attribute, old, new, kwargs):
    if new == "on":
      self.log(f"Motion detected in {self.friendly_name(entity)} and attributets {attribute}")

  def event_button(self, event_name, data, kwargs):
    event_data = data["event"]
    button = data['id']
    event_received = datetime.now()
    self.log(event_data)
    if event_data == 1000: #down
      self.log(f'Button {button} down, date {event_received}')
    elif event_data == 1002: #releas
      self.log(f'Button {button} release, date {event_received}')
    elif event_data == 1001: #long down
      self.log(f'Button {button} long click down, date {event_received}')
    elif event_data == 1003: #long release
      self.log(f'Button {button} long click release, date {event_received}')
    elif event_data == 1004: #double click
      self.log(f'Button {button} double click, date {event_received}')
    elif event_data > 1004 and event_data < 1010: #multi click
      self.log(f'Button {button} multi click, date {event_received}')
    else:
      self.log(f'Button event {event_data} not suported, date {event_received}')

  def event_qube(self, event_name, data, kwargs):
    event_data = data["event"]
    cube = data["id"]
    event_received = datetime.now()
    # if data['id'] == self.args['id']:
    self.log(event_data)
    if event_data in [1000, 2000, 3000, 4000, 5000, 6000]:
      self.log(f'Qube {cube} slide, date {event_received}')
      # self.set_state("sensor.aqara_cube", state = 'slide', attributes = {"event_data": event_data, "event_received": str(event_received)})
    elif event_data in [1001, 2002, 3003, 4004, 5005, 6006]:
      self.log(f'Qube {cube} double tap, date {event_received}')
      # self.set_state("sensor.aqara_cube", state = 'double tap', attributes = {"event_data": event_data, "event_received": str(event_received)})
    elif event_data in [1006, 2005, 3004, 4003, 5002, 6001]:
      self.log(f'Qube {cube} flip180, date {event_received}')
      # self.set_state("sensor.aqara_cube", state = 'flip180', attributes = {"event_data": event_data, "event_received": str(event_received)})
    elif event_data in [1002, 1003, 1004, 1005, 2001, 2003, 2004, 2006, 3001, 3002, 3005, 3006, 4001, 4002, 4005, 4006, 5001, 5003, 5004, 5006, 6002, 6003, 6004, 6005]:
      self.log(f'Qube {cube} flip90, date {event_received}')
      # self.set_state("sensor.aqara_cube", state = 'flip90', attributes = {"event_data": event_data, "event_received": str(event_received)})
    elif event_data == 7007:
      self.log(f'Qube {cube} shake, date {event_received}')
      # self.set_state("sensor.aqara_cube", state = 'shake', attributes = {"event_data": event_data, "event_received": str(event_received)})
    elif event_data == 7008:
      self.log(f'Qube {cube} fall, date {event_received}')
      # self.set_state("sensor.aqara_cube", state = 'fall', attributes = {"event_data": event_data, "event_received": str(event_received)})                              
    elif event_data == 7000:
      self.log(f'Qube {cube} wake, date {event_received}')
      # self.set_state("sensor.aqara_cube", state = 'wake', attributes = {"event_data": event_data, "event_received": str(event_received)})
    elif len(str(event_data)) != 4 or str(event_data)[1:3] != '00':
      if event_data > 0:
        self.log(f'Qube {cube} rotate cw, date {event_received}')
        # self.set_state("sensor.aqara_cube", state = 'rotate cw', attributes = {"event_data": event_data, "event_received": str(event_received)})
      elif event_data < 0:
        self.log(f'Qube {cube} rotate ccw, date {event_received}')
        # self.set_state("sensor.aqara_cube", state = 'rotate ccw', attributes = {"event_data": event_data, "event_received": str(event_received)})
    else:
      self.log(f'Qube event {event_data} not suported, date {event_received}')