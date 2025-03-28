import unittest
from unittest.mock import patch
from os.path import join, realpath
import sys

# Adjust the path to import StateLogic
sys.path.insert(0, realpath(join(__file__, "../../")))
from statelogic import StateLogic

class TestStateLogic(unittest.TestCase):

    def test_default_state_should_be_none(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition

        self.assertIsNone(self.state())

    def test_should_show_correct_states(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition

        expected_states = ["GAS", "LIQUID", "SOLID"]
        self.assertEqual(self.states(), expected_states)

    def test_should_not_allow_reserved_words_as_transition_event(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.transition("return", "LIQUID", "PLASMA")
        expected_transitions = ["condense", "freeze"]
        self.assertEqual(self.events(), expected_transitions)

    def test_should_handle_illegal_state_gracefully(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.state("illegalState")
        self.assertIsNone(self.state())

    def test_should_handle_illegal_state_transitions_gracefully(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.transition("illegalTransition", "LIQUID", "SOLID")
        expected_transitions = ["condense", "freeze"]
        self.assertEqual(self.events(), expected_transitions)

    def test_should_transition_to_first_state_correctly(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.state("SOLID")
        self.assertEqual(self.state(), "SOLID")  # Next state is SOLID

    def test_should_not_transition_other_state_than_the_first_state(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.state("SOLID")
        self.state("LIQUID")
        self.assertEqual(self.state(), "SOLID")  # Next state is SOLID

    def test_should_transit_correctly_by_fire(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.state("GAS")
        self.fire('condense')
        self.assertEqual(self.state(), "LIQUID")
        self.fire('freeze')
        self.assertEqual(self.state(), "SOLID")

    def test_should_not_transit_for_incorrect_transition(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.state("GAS")
        self.fire('condense')
        self.assertEqual(self.state(), "LIQUID")
        self.fire('condense')
        self.assertEqual(self.state(), "LIQUID")

    def test_should_transit_correctly_by_transition_names(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.state("GAS")
        self.condense()
        self.assertEqual(self.state(), "LIQUID")
        self.freeze()
        self.assertEqual(self.state(), "SOLID")

    @patch('builtins.print')
    def test_should_log_messages(self, mock_print):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        self.infoMsg("Starting state transition")
        mock_print.assert_called()  # Check if logging occurred

    def test_should_call_hook_methods_on_state_transition(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        def fired(self):
            if not hasattr(self, "count"):
                self.count=0
            self.count = self.count + 1
            return True
        self.__dict__["fired"] = fired.__get__(self)
        # Setup event hooks
        self.before('freeze', self.fired)
        self.on('condense', self.fired)
        self.after('condense', self.fired)
        
        self.state('GAS')
        self.fire("condense")  # Trigger the condense transition
        self.assertEqual(self.state(), 'LIQUID')
        self.assertEqual(self.count, 2)
        
        self.fire("freeze")  # Trigger the freeze transition   
        self.assertEqual(self.state(), 'SOLID')
        self.assertEqual(self.count, 3)

    def test_should_fail_transition_for_false_returned_by_hook_methods(self):
        # Extend StateLogic to the Unittest Class everytime 
        # to enhance the capability of Unittest to have state functions
        StateLogic(self)        # don't need to get return object
        self.transition("freeze", "LIQUID", "SOLID")
        self.transition("condense", "GAS", "LIQUID")  # Set up transition
        def fired(self):
            if not hasattr(self, "count"):
                self.count=0
            self.count = self.count + 1
            return False
        self.before('freeze', fired)
        self.on('condense', fired)
        self.after('condense', fired)
        self.state('GAS')

        self.fire("condense")  # Trigger
        self.assertEqual(self.state(), 'LIQUID')
        self.assertEqual(self.count, 2)
        self.fire("freeze")  # Trigger
        self.assertEqual(self.state(), 'LIQUID')
        self.assertEqual(self.count, 3)
        