# You don't need to install unittest, which is the lib in cython and exists with python
# cd to this folder and run `python -m unittest testStateLogic.py
# ` 
import unittest
from unittest.mock import patch
from os.path import join, realpath

# The following code tried to import statelogic folder
# by moving to parent folder
import sys
sys.path.insert(0, realpath(join(__file__, "../../")))
from statelogic import StateLogic

class TestStateLogic(unittest.TestCase):
    def setUp(self):
        # Initialize a new instance of StateLogic before each test
        self.state_logic = StateLogic()
        self.state_logic.transition("freeze", "LIQUID", "SOLID")
        self.state_logic.transition("condense", "GAS", "LIQUID")  # Set up transition

    def test_default_state_should_be_none(self):
        self.assertIsNone(self.state_logic.state())

    def test_should_show_correct_states(self):
        expected_states = ["GAS", "LIQUID", "SOLID"]
        self.assertEqual(self.state_logic.states(), expected_states)

    def test_should_not_allow_reserved_words_as_transition_event(self):
        self.state_logic.transition("return", "LIQUID", "PLASMA")
        expected_transitions = ["condense", "freeze"]
        self.assertEqual(self.state_logic.events(), expected_transitions)

    def test_should_handle_illegal_state_gracefully(self):
        self.state_logic.state("illegalState")
        self.assertIsNone(self.state_logic.state())

    def test_should_handle_illegal_state_transitions_gracefully(self):
        self.state_logic.transition("illegalTransition", "LIQUID", "SOLID")
        expected_transitions = ["condense", "freeze"]
        self.assertEqual(self.state_logic.events(), expected_transitions)

    def test_should_transition_to_first_state_correctly(self):
        self.state_logic.state("SOLID")
        self.assertEqual(self.state_logic.state(), "SOLID")  # Next state is SOLID

    def test_should_not_transition_other_state_than_the_first_state(self):
        self.state_logic.state("SOLID")
        self.state_logic.state("LIQUID")
        self.assertEqual(self.state_logic.state(), "SOLID")  # Next state is SOLID

    def test_should_transit_correctly_by_fire(self):
        self.state_logic.state("GAS")
        self.state_logic.fire('condense')
        self.assertEqual(self.state_logic.state(), "LIQUID")
        self.state_logic.fire('freeze')
        self.assertEqual(self.state_logic.state(), "SOLID")

    def test_should_not_transit_for_incorrect_transition(self):
        self.state_logic.state("GAS")
        self.state_logic.fire('condense')
        self.assertEqual(self.state_logic.state(), "LIQUID")
        self.state_logic.fire('condense')
        self.assertEqual(self.state_logic.state(), "LIQUID")

    def test_should_transit_correctly_by_transition_names(self):
        s = StateLogic()
        s.transition("freeze", "LIQUID", "SOLID")
        s.transition("condense", "GAS", "LIQUID")  # Set up transition
        s.state("GAS")
        s.condense()
        self.assertEqual(s.state(), "LIQUID")
        s.freeze()
        self.assertEqual(s.state(), "SOLID")

    @patch('builtins.print')
    def test_should_log_messages(self, mock_print):
        self.state_logic.infoMsg("Starting state transition")
        mock_print.assert_called()  # Check if logging occurred

    def test_should_call_hook_methods_on_state_transition(self):
        def fired(self):
            if not hasattr(self, "count"):
                self.count=0
            self.count = self.count + 1
            return True
        self.state_logic.__dict__["fired"] = fired.__get__(self)
        # Setup event hooks
        self.state_logic.before('freeze', self.state_logic.fired)
        self.state_logic.on('condense', self.state_logic.fired)
        self.state_logic.after('condense', self.state_logic.fired)
        
        self.state_logic.state('GAS')
        self.state_logic.fire("condense")  # Trigger the condense transition
        self.assertEqual(self.state_logic.state(), 'LIQUID')
        self.assertEqual(self.state_logic.count, 2)
        
        self.state_logic.fire("freeze")  # Trigger the freeze transition   
        self.assertEqual(self.state_logic.state(), 'SOLID')
        self.assertEqual(self.state_logic.count, 3)

    def test_should_fail_transition_for_false_returned_by_hook_methods(self):
        def fired(self):
            if not hasattr(self, "count"):
                self.count=0
            self.count = self.count + 1
            return False
        self.state_logic.__dict__["fired"] = fired.__get__(self)
        # Setup event hooks
        self.state_logic.before('freeze', self.state_logic.fired)
        self.state_logic.on('condense', self.state_logic.fired)
        self.state_logic.after('condense', self.state_logic.fired)
        self.state_logic.state('GAS')

        self.state_logic.fire("condense")  # Trigger
        self.assertEqual(self.state_logic.state(), 'LIQUID')
        self.assertEqual(self.state_logic.count, 2)
        self.state_logic.fire("freeze")  # Trigger
        self.assertEqual(self.state_logic.state(), 'LIQUID')
        self.assertEqual(self.state_logic.count, 3)
        