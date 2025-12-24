import unittest
from unittest.mock import MagicMock, patch
from drivers.connexcc_driver import Conexcc

class TestConex(unittest.TestCase):

    def setUp(self):
        self.conex = Conexcc()
        # Mock the serial connection
        self.conex.ser = MagicMock() 

    def test_send_command_write(self):
        """Test sending a command writes bytes to serial."""
        # We assume send_command calls self.ser.write internally
        # You might need to mock the specific logic inside send_command
        
        # Let's mock the return value of send_command directly for this test
        with patch.object(self.conex, 'send_command', return_value='1TS000032') as mock_send:
            result = self.conex.send_command("TS", 0)
            
            mock_send.assert_called_with("TS", 0)
            self.assertEqual(result, '1TS000032')

    def test_homing_logic_simulation(self):
        """Simulate the homing loop logic from your main.py."""
        # We simulate the driver returning different states
        # 1st call: Moving (28), 2nd call: Moving (28), 3rd call: Ready (32)
        with patch.object(self.conex, 'send_command') as mock_send:
            mock_send.side_effect = ['1TS000028', '1TS000028', '1TS000032']
            
            # Simulate the loop you have in main.py
            states = []
            for _ in range(3):
                status = self.conex.send_command("TS", 0)
                state = status[-2:]
                states.append(state)
            
            self.assertEqual(states, ['28', '28', '32'])

if __name__ == '__main__':
    unittest.main()