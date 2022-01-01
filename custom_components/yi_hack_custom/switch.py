"""Yi Camera Custom Integration"""
import logging

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_IP_ADDRESS, CONF_FRIENDLY_NAME, CONF_USERNAME, CONF_PASSWORD
from homeassistant.components.switch import PLATFORM_SCHEMA

from datetime import timedelta

SCAN_INTERVAL = timedelta(minutes=2)

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP_ADDRESS): cv.string,
    vol.Required(CONF_FRIENDLY_NAME): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Yi Camera Custom Integration"""
    url = 'http://' + config[CONF_IP_ADDRESS] + ':8080'
    add_entities([YiCamera(url, config[CONF_FRIENDLY_NAME], config[CONF_USERNAME], config[CONF_PASSWORD])])


class YiCamera(SwitchEntity):
    """Representation of a Yi Home Camera"""

    def __init__(self, url, name, user, password):
        _LOGGER.debug('Initialising switch')
        self._url = url
        self._username = user
        self._password = password
        self._is_on = False
        self._icon = 'mdi:webcam'
        self._name = name
        self._attributes = {
            'ai_human_detection': False,
            'ir': False,
            'led': False,
            'rotate': False,
            'save_video_on_motion': False,
            'sentitivity': "low",
            'sound_detection': False,
            'sound_sensitivity': "80",
        }
        self.update()

    @property
    def name(self):
        """Name of the device."""
        return self._name

    @property
    def is_on(self):
        """Device State"""
        return self._is_on

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def turn_on(self, **kwargs) -> None:
        """Turn Plug On"""
        requests.get(self._url+'/cgi-bin/camera_settings.sh',
                     params={'switch_on': 'yes'}, auth=(self._username, self._password))

        self._is_on = True

    def turn_off(self, **kwargs):
        requests.get(self._url+'/cgi-bin/camera_settings.sh',
                     params={'switch_on': 'no'}, auth=(self._username, self._password))

        self._is_on = False

    def update(self):
        _LOGGER.debug('Updating Switch Attributes')
        r = requests.get(self._url+'/cgi-bin/get_configs.sh',
                         params={'conf': 'camera'}, auth=(self._username, self._password))

        data = r.json()

        self._is_on = data['SWITCH_ON'] == 'yes'
        self._attributes = {
            'ai_human_detection': data['AI_HUMAN_DETECTION'] == 'yes',
            'ir': data['IR'] == 'yes',
            'led': data['LED'] == 'yes',
            'rotate': data['ROTATE'] == 'yes',
            'save_video_on_motion': data['SAVE_VIDEO_ON_MOTION'] == 'yes',
            'sentitivity': data['SENSITIVITY'],
            'sound_detection': data['SOUND_DETECTION'] == 'yes',
            'sound_sensitivity': data['SOUND_SENSITIVITY'],
        }
