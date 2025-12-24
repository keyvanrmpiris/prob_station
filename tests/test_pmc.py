import unittest
from unittest.mock import MagicMock, patch
from drivers.pcm_driver import Pcm

class TestPcm(unittest.TestCase):

    def setUp(self):
        self.pcm = Pcm()
        self.pcm.instrument = MagicMock()

    def test_connect(self):
        with patch('drivers.pcm_driver.Pcm.connect') as mock_conn:
            self.pcm.connect()
            mock_conn.assert_called_once()

    def test_send_command(self):
        """Test passing arguments to the PCM driver."""
        with patch.object(self.pcm, 'send_command') as mock_send:
            self.pcm.send_command("TEST_CMD")
            mock_send.assert_called_with("TEST_CMD")

if __name__ == '__main__':
    unittest.main()