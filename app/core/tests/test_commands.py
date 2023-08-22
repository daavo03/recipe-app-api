"""
Test custom Django management commands.
"""
# Patch in order to mock the behavior of the DB
from unittest.mock import patch
# One of the errors we might get when connect to DB before it's ready
from psycopg2 import OperationalError as Psycopg2Error
# Helper function allow us to call a command by the name
from django.core.management import call_command
# Exception that may get thrown by the DB
from django.db.utils import OperationalError
# Base test class for creating our unit test
from django.test import SimpleTestCase


# Command that we're going to be mocking, we provide the path.
# The last 2 is bc we're going to be using the Command.check which is provided by the Command base class it has a check method
# that allow us to check the status of the DB. We're going to be mocking that check to simulate the response
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """
    Test commands.
    """

    # Because the path, it's adding a new argument to each of the calls that we make to our test methods
    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for DB if DB is ready.
        """

        # This just says when check is called inside our test case, we just want to return the True value
        patched_check.return_value = True

        # This will execute the code inside of wait_for_db.py
        call_command('wait_for_db')

        # This ensures that the mock check method is called with a parameter
        patched_check.assert_called_once_with(databases=['default'])

    # Second test case. What should happen if the DB isn't ready
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test for waiting DB when getting OperationalError.
        """

        # We want to rise some exceptions that would be raised if the DB wasn't ready
        # The way you make it raise an exception is using the side_effect.
        # side_effect allows you to pass in various different items that get handled differently
        # depending on the type
        # If we pass in an exception, then the mocking library knows that it should raise that exception.
        # If we pass in a boolean, then it will return the boolean value
        # So this allow us to define different values that happen each time we call it in the order that we call it.
        # What we're doing here is the first 2 times we call the mocked method, we want it to raise the Pyscopg2Error and then
        # we raise 3 operational errors. Finally the True means the sixth time we call it, we're going to get True back
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
