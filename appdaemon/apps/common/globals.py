from enum import Enum

# Global variables

ios_isa = 'push_to_chrome_nizm0_oneplus3'
notify_michal = "notify/push_to_chrome_nizm0_oneplus3"

michal = "person.michal"
gosia = "person.gosia"

alarm = "alarm_control_panel.house"


notification_mode = {}
notification_mode["start_quiet_weekday"] = "23:00:00"
notification_mode["start_quiet_weekend"] = "23:59:00"
notification_mode["stop_quiet_weekday"] = "07:00:00"
notification_mode["stop_quiet_weekend"] = "09:00:00"


presence_state = {}
# Change this if you want to change the display name
presence_state["home"] = "Home"
presence_state["just_arrived"] = "Just arrived"
presence_state["just_left"] = "Just left"
presence_state["away"] = "Away"
presence_state["extended_away"] = "Extended away"


PEOPLE = {
    'Michal': {
        'device_tracker': 'person.michal',
        'proximity': 'proximity.home_michal',
        'notifier': 'push_to_chrome_nizm0_oneplus3'
    },
    'Gosia': {
        'device_tracker': 'person.gosia',
        'proximity': 'proximity.home_gosia',
        'notifier': 'push_to_chrome_nizm0_oneplus3'
    }
}


# class GlobalEvents(Enum):
#     # Events
#     # fired when house mode chages, i.e. day, evening, night, morning
#     EV_HOUSE_MODE_CHANGED = 'EV_HOUSE_MODE_CHANGED'
#     # any motion detected in a room
#     EV_MOTION_DETECTED = 'EV_MOTION_DETECTED'
#     EV_MOTION_OFF = 'EV_MOTION_OFF'
#     # fires when alarm on a google home device
#     EV_ALARM_CLOCK_ALARM = 'EV_ALARM_CLOCK_ALARM'

#     # Commands
#     # play a program with a specific program id (see sr.se api for details)
#     CMD_SR_PLAY_PROGRAM = 'CMD_SR_PLAY_PROGRAM'
#     # send notification
#     CMD_NOTIFY = 'CMD_NOTIFY'
#     # send notification with greeting
#     CMD_NOTIFY_GREET = 'CMD_NOTIFY_GREET'
#     # turn on ambient lights
#     CMD_AMBIENT_LIGHTS_ON = 'CMD_AMBIENT_LIGHTS_ON'
#     # turn off ambient lights
#     CMD_AMBIENT_LIGHTS_OFF = 'CMD_AMBIENT_LIGTS_OFF'


class HouseModes(Enum):
    morning = 'Morning'
    day = 'Day'
    evening = 'Evening'
    night = 'Night'