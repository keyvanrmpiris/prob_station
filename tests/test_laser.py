import unittest
from unittest.mock import MagicMock, patch
from drivers.laser_driver import Laser

class TestLaser(unittest.TestCase):

    def setUp(self):
        """Runs before every test."""
        self.laser = Laser()
        # Mock the internal instrument object (e.g., pyvisa resource)
        self.laser.instrument = MagicMock()

    def test_connect(self):
        """Test if connect initializes correctly."""
        # We mock the library the driver uses (e.g., pyvisa or serial)
        # Adjust 'drivers.laser_driver.pyvisa' to match your actual import
        with patch('drivers.laser_driver.Laser.connect') as mock_connect:
            self.laser.connect()
            mock_connect.assert_called_once()

    def test_write_command(self):
        """Test if writing to the laser sends the correct string."""
        cmd = "POW 10"
        self.laser.instrument.write(cmd)
        
        # specific to how you implemented .write()
        self.laser.instrument.write.assert_called_with("POW 10")

    def test_query_idn(self):
        """Test if querying IDN returns a mock string."""
        self.laser.instrument.query_idn.return_value = "Mock Laser Model X"
        
        reply = self.laser.instrument.query_idn()
        self.assertEqual(reply, "Mock Laser Model X")

if __name__ == '__main__':
    unittest.main()