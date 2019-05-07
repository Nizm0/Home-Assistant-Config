import appdaemon.plugins.hass.hassapi as hass

from datetime import datetime, timedelta

class VacuumActions(hass.Hass):

  def initialize(self):
    self.listen_state(self.light_on, "binary_sensor.kitchen_left_window_sensor", new = "on")
    self.listen_state(self.light_off, "binary_sensor.kitchen_left_window_sensor", new = "off")

  def open(self, entity, attribute, old, new, kwargs):
    self.turn_on("light.bedroom_main_light")
    self.run_in(self.light_off, 60)

  def light_on(self, entity, attribute, old, new, kwargs):
    self.turn_on("light.bedroom_main_light")

  def light_off(self, entity, attribute, old, new, kwargs):
    self.turn_off("light.bedroom_main_light")