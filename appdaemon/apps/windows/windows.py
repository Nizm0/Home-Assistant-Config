import appdaemon.plugins.hass.hassapi as hass

from datetime import datetime, timedelta

class WindowsActions(hass.Hass):

  def initialize(self):
    self.listen_state(self.light_on, "binary_sensor.kitchen_left_window_sensor", new = "on")
    self.listen_state(self.light_off, "binary_sensor.kitchen_left_window_sensor", new = "off")

  def open(self, entity, attribute, old, new, kwargs):
    self.turn_on("light.hue_color_lamp_2")
    self.run_in(self.light_off, 60)

  def light_on(self, entity, attribute, old, new, kwargs):
    self.turn_on("light.hue_color_lamp_2")

  def light_off(self, entity, attribute, old, new, kwargs):
    self.turn_off("light.hue_color_lamp_2")