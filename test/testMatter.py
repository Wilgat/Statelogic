import unittest
from unittest.mock import patch
from os.path import join, realpath
import sys

# Adjust the path to import StateLogic
sys.path.insert(0, realpath(join(__file__, "../../")))
from statelogic import StateLogic

class Matter(StateLogic):
    def __init__(self, author: str, app_name: str, major_version: str, minor_version: str, patch_version: str):
        super().__init__(self)
        self.author(author).appName(app_name).majorVersion(major_version).minorVersion( minor_version).patchVersion( patch_version)
        self.temperature = 110  # Initialize temperature

        # Define transitions for different states of matter
        self.transition("freeze", "LIQUID", "SOLID")   # Liquid to Solid
        self.transition("melts", "SOLID", "LIQUID")    # Solid to Liquid
        self.transition("evaporate", "LIQUID", "GAS")   # Liquid to Gas
        self.transition("condense", "GAS", "LIQUID")    # Gas to Liquid
        self.transition("sublimate", "SOLID", "GAS")    # Solid to Gas
        self.transition("deposition", "GAS", "SOLID")    # Gas to Solid

        # Set up event hooks for each event
        self.after("freeze", self.log_freeze)
        self.after("melts", self.log_melts)
        self.after("evaporate", self.log_evaporate)
        self.after("condense", self.log_condense)

        # Set up the before hook for the "condense" event
        self.before("condense", self.check_condense)
        self.on("condense", self.show_condense)
        self.on("condense", self.show_condense2)

    def safe_msg(self, msg, tag):
        pass

    def info_msg(self, msg, tag):
        pass

    def critical_msg(self, msg, tag):
        pass

    def log_freeze(self):
        self.safe_msg("The substance has frozen from liquid to solid.", "FROZEN")

    def log_melts(self):
        self.safe_msg("The substance has melted from solid to liquid.", "MELTED")

    def log_evaporate(self):
        self.safe_msg("The substance has evaporated from liquid to gas.", "EVAPORATED")

    def log_condense(self):
        self.info_msg("The substance has condensed from gas to liquid.", "CONDENSED")

    def show_condense(self):
        self.safe_msg(f"Another On {self.transitionName()}: {self.fromState()} -> {self.nextState()}", "CONDENSE")

    def show_condense2(self):
        self.safe_msg(f"(2) Another On {self.transitionName()}: {self.fromState()} -> {self.nextState()}", self.transitionName().upper())

    def check_condense(self) -> bool:
        if self.temperature < 120:
            self.safe_msg("Condense success", "CONDENSE SUCCESS")
            return True  # Allow the transition
        else:
            self.safe_msg("Condense failed: temperature too high.", "CONDENSE FAILED")
            return False  # Prevent the transition


class TestMatter(unittest.TestCase):
    def setUp(self):
        # Initialize a new instance of Matter before each test
        self.matter = Matter("Test Author", "Matter Test App", "1", "0", "0")

    def test_transition_liquid_to_solid_on_freeze(self):
        self.matter.state("LIQUID")
        self.matter.temperature = 100  # Set temperature for freezing
        self.matter.fire("freeze")
        self.assertEqual(self.matter.state(), "SOLID")

    def test_transition_solid_to_liquid_on_melts(self):
        self.matter.state("SOLID")
        self.matter.temperature = 80  # Set temperature for melting
        self.matter.fire("melts")
        self.assertEqual(self.matter.state(), "LIQUID")

    def test_transition_liquid_to_gas_on_evaporate(self):
        self.matter.state("LIQUID")
        self.matter.temperature = 110  # Set temperature for evaporation
        self.matter.fire("evaporate")
        self.assertEqual(self.matter.state(), "GAS")

    def test_transition_gas_to_liquid_on_condense_when_temperature_is_low(self):
        self.matter.state("GAS")
        self.matter.temperature = 100  # Set temperature for condensation
        self.matter.fire("condense")
        self.assertEqual(self.matter.state(), "LIQUID")

    def test_not_transition_gas_to_liquid_on_condense_when_temperature_is_high(self):
        self.matter.state("GAS")
        self.matter.temperature = 130  # Set temperature too high
        self.matter.fire("condense")
        self.assertEqual(self.matter.state(), "GAS")  # No change

    def test_transition_solid_to_gas_on_sublimate(self):
        self.matter.state("SOLID")
        self.matter.temperature = 150  # Set temperature for sublimation
        self.matter.fire("sublimate")
        self.assertEqual(self.matter.state(), "GAS")

    def test_transition_gas_to_solid_on_deposition(self):
        self.matter.state("GAS")
        self.matter.temperature = 50  # Set temperature for deposition
        self.matter.fire("deposition")
        self.assertEqual(self.matter.state(), "SOLID")

    @patch.object(Matter, 'safe_msg')
    def test_logging_freeze_event(self, mock_safe_msg):
        self.matter.state("LIQUID")
        self.matter.temperature = 100
        self.matter.fire("freeze")
        mock_safe_msg.assert_called_with("The substance has frozen from liquid to solid.", "FROZEN")

    @patch.object(Matter, 'safe_msg')
    def test_logging_melts_event(self, mock_safe_msg):
        self.matter.state("SOLID")
        self.matter.temperature = 80
        self.matter.fire("melts")
        mock_safe_msg.assert_called_with("The substance has melted from solid to liquid.", "MELTED")

    @patch.object(Matter, 'safe_msg')
    def test_logging_evaporate_event(self, mock_safe_msg):
        self.matter.state("LIQUID")
        self.matter.temperature = 110
        self.matter.fire("evaporate")
        mock_safe_msg.assert_called_with("The substance has evaporated from liquid to gas.", "EVAPORATED")

    @patch.object(Matter, 'info_msg')
    def test_logging_condense_event_when_success(self, mock_info_msg):
        self.matter.state("GAS")
        self.matter.temperature = 100
        self.matter.fire("condense")
        mock_info_msg.assert_called_with("The substance has condensed from gas to liquid.", "CONDENSED")

if __name__ == '__main__':
    unittest.main()