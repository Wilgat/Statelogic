import unittest
from unittest.mock import patch
from os.path import join, realpath
import sys

# Adjust the path to import StateLogic
sys.path.insert(0, realpath(join(__file__, "../../")))
from statelogic import StateLogic

class TestStateLogic(unittest.TestCase):
    def test_default_state_should_be_none(self):
        state_logic = StateLogic()  # Creating instance directly
        self.assertIsNone(state_logic.state())

    def test_should_show_correct_states(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.transition("freeze", "LIQUID", "SOLID")
        state_logic.transition("condense", "GAS", "LIQUID")  # Set up transition
        expected_states = ["GAS", "LIQUID", "SOLID"]
        self.assertEqual(state_logic.states(), expected_states)

    def test_should_not_allow_reserved_words_as_transition_event(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.transition("freeze", "LIQUID", "SOLID")
        state_logic.transition("condense", "GAS", "LIQUID")  # Set up transition
        state_logic.transition("return", "LIQUID", "PLASMA")
        expected_transitions = ["condense", "freeze"]
        self.assertEqual(state_logic.events(), expected_transitions)

    def test_should_handle_illegal_state_gracefully(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.state("illegalState")
        self.assertIsNone(state_logic.state())

    def test_should_handle_illegal_state_transitions_gracefully(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.transition("freeze", "LIQUID", "SOLID")
        state_logic.transition("condense", "GAS", "LIQUID")  # Set up transition
        state_logic.transition("illegalTransition", "LIQUID", "SOLID")
        expected_transitions = ["condense", "freeze"]
        self.assertEqual(state_logic.events(), expected_transitions)

    def test_should_transition_to_first_state_correctly(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.state("SOLID")
        self.assertEqual(state_logic.state(), "SOLID")  # Next state is SOLID

    def test_should_not_transition_other_state_than_the_first_state(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.state("SOLID")
        state_logic.state("LIQUID")
        self.assertEqual(state_logic.state(), "SOLID")  # Remains SOLID

    def test_should_transit_correctly_by_fire(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.state("GAS")
        state_logic.transition("condense", "GAS", "LIQUID")
        state_logic.transition("freeze", "LIQUID", "SOLID")
        state_logic.fire('condense')
        self.assertEqual(state_logic.state(), "LIQUID")
        state_logic.fire('freeze')
        self.assertEqual(state_logic.state(), "SOLID")

    def test_should_not_transit_for_incorrect_transition(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.state("GAS")
        state_logic.transition("condense", "GAS", "LIQUID")
        state_logic.fire('condense')
        self.assertEqual(state_logic.state(), "LIQUID")
        state_logic.fire('condense')
        self.assertEqual(state_logic.state(), "LIQUID")

    def test_should_transit_correctly_by_transition_names(self):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.transition("freeze", "LIQUID", "SOLID")
        state_logic.transition("condense", "GAS", "LIQUID")  # Set up transition
        state_logic.state("GAS")
        state_logic.condense()
        self.assertEqual(state_logic.state(), "LIQUID")
        state_logic.freeze()
        self.assertEqual(state_logic.state(), "SOLID")

    @patch('builtins.print')
    def test_should_log_messages(self, mock_print):
        state_logic = StateLogic()  # Creating instance directly
        state_logic.infoMsg("Starting state transition")
        mock_print.assert_called()  # Check if logging occurred

    def test_should_call_hook_methods_on_state_transition(self):
        state_logic = StateLogic()  # Creating instance directly
        def fired(self):
            if not hasattr(self, "count"):
                self.count = 0
            self.count += 1
            return True

        state_logic.__dict__["fired"] = fired.__get__(state_logic)
        state_logic.before('freeze', state_logic.fired)
        state_logic.on('condense', state_logic.fired)
        state_logic.after('condense', state_logic.fired)
        state_logic.state('GAS')

        state_logic.fire("condense")  # Trigger
        self.assertEqual(state_logic.state(), 'LIQUID')
        self.assertEqual(state_logic.count, 2)
        state_logic.fire("freeze")  # Trigger
        self.assertEqual(state_logic.state(), 'LIQUID')
        self.assertEqual(state_logic.count, 3)