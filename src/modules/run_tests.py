import unittest
from src.modules.chat_api.tests import test_chat_api_controller

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_chat_api_controller.ChatAPITest))
    
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
