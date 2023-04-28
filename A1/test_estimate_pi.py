import unittest
import os
from unittest.mock import Mock
from estimate_pi import estimate_pi, PiFileWriter

class TestEstimatePi(unittest.TestCase):
    def test_estimate_pi(self):
        pi_expected = 3.141592653589793
        pi_actual = estimate_pi(1000000)
        self.assertAlmostEqual(pi_expected, pi_actual, delta=0.01)
    
    def test_string_iterations(self): 
        with self.assertRaises(TypeError) as cm:
            estimate_pi('1000000')
        self.assertEqual(str(cm.exception), "Argument must be a positive integer")
    
    def test_PiFileWriter(self):
        pi = 3.141592653589793
        PiFileWriter.write(str(pi), 'pi.txt')
        with open('pi.txt', 'r') as file:
            pi_actual = file.read()
        self.assertEqual(pi_actual, str(pi))
        os.remove('pi.txt')

    def test_mock_PiFileWriter(self):
        mock_file_writer = Mock(name="PiFileWriter")
        mock_file_writer.write.return_value = None
        pi = 3.141592653589793
        mock_file_writer.write(str(pi), 'pi.txt')
        mock_file_writer.write.assert_called_once_with(str(pi), 'pi.txt')

if __name__ == '__main__':
    unittest.main()
