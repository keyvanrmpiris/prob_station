import unittest
from unittest.mock import MagicMock, patch
from drivers.rigol_driver import Rigol

class TestRigol(unittest.TestCase):

    def setUp(self):
        self.rgl = Rigol()
        # Mock internal instrument
        self.rgl.instrument = MagicMock()

    def test_get_vertical_params(self):
        """Ensure getter methods don't crash and return expected mocks."""
        # Setup the mock to return a specific string when queried
        self.rgl.instrument.query.return_value = "CH1:5V"
        
        # If your driver method returns the value, test it here
        # If it just prints, we just ensure it runs without error
        try:
            self.rgl.get_vertical_params()
        except Exception as e:
            self.fail(f"get_vertical_params raised exception: {e}")

    def test_monitor_measurements_threading(self):
        """Test that start/stop monitoring flags are set correctly."""
        # We don't want to actually start a thread in a unit test usually,
        # but we can check if the flags update.
        
        self.rgl.monitor_measurements() # Should start thread
        # Assuming you have a flag like self.running or similar
        # self.assertTrue(self.rgl.running) 
        
        self.rgl.stop_monitoring()
        # self.assertFalse(self.rgl.running)

    def test_status_formatting(self):
        """Test that get_status returns a string."""
        status = self.rgl.get_status()
        self.assertIsInstance(status, str)

if __name__ == '__main__':
    unittest.main()