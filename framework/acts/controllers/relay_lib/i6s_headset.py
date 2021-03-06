#!/usr/bin/env python3
#
#   Copyright 2017 - The Android Open Source Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import enum

from acts.controllers.relay_lib.errors import RelayConfigError
from acts.controllers.relay_lib.generic_relay_device import GenericRelayDevice
from acts.controllers.relay_lib.helpers import validate_key

PAIRING_MODE_WAIT_TIME = 3
WAIT_TIME = 0.1
MISSING_RELAY_MSG = 'Relay config for i6s Headset "%s" missing relay "%s".'


class Buttons(enum.Enum):
    POWER = "Power"
    NEXT = 'Next'
    PREVIOUS = "Previous"
    PLAY_PAUSE = 'Play_pause'
    PAIR = "Pair"
    VOLUME_UP = "Volume_up"
    VOLUME_DOWN = "Volume_down"


class I6sHeadset(GenericRelayDevice):

    def __init__(self, config, relay_rig):
        GenericRelayDevice.__init__(self, config, relay_rig)
        self.mac_address = validate_key('mac_address', config, str,
                                        'I6sHeadset')
        for button in Buttons:
            self.ensure_config_contains_relay(button.value)

    def setup(self):
        GenericRelayDevice.setup(self)

    def clean_up(self):
        """Turns off headset."""
        self.relays[Buttons.Pair.value].set_no_for(PAIRING_MODE_WAIT_TIME)

    def ensure_config_contains_relay(self, relay_name):
        """
        Throws an error if the relay does not exist.

        Args:
            relay_name:relay_name to be checked.
        """
        if relay_name not in self.relays:
            raise RelayConfigError(MISSING_RELAY_MSG % (self.name, relay_name))

    def enter_pairing_mode(self):
        """Sets relay in paring mode."""
        self.relays[Buttons.PAIR.value].set_no_for(PAIRING_MODE_WAIT_TIME)

    def power_on(self):
        """Power on relay."""
        self.relays[Buttons.POWER.value].set_no_for(WAIT_TIME)

    def press_play_pause(self):
        """
        Sets relay to
            Play state : if there is no A2DP_streaming.
            Pause state : if there is A2DP_streaming.
        """
        self.relays[Buttons.PLAY_PAUSE.value].set_no_for(WAIT_TIME)

    def press_next(self):
        """Skips to next song from relay_device."""
        self.relays[Buttons.NEXT.value].set_no_for(WAIT_TIME)

    def press_previous(self):
        """Skips to previous song from relay_device."""
        self.relays[Buttons.PREVIOUS.value].set_no_for(WAIT_TIME)

    def press_volume_up(self):
        """Increases volume from relay_device."""
        self.relays[Buttons.VOLUME_UP.value].set_no_for(WAIT_TIME)

    def press_volume_down(self):
        """Decreases volume from relay_device."""
        self.relays[Buttons.VOLUME_DOWN.value].set_no_for(WAIT_TIME)

    def press_initiate_call(self):
        """Initiate call from relay device."""
        for i in range(0, 2):
            self.relays[Buttons.POWER.value].set_no_for(WAIT_TIME)
        return True

    def press_accept_call(self):
        """Accepts call from relay device."""
        self.relays[Buttons.POWER.value].set_no_for(WAIT_TIME)
        return True
