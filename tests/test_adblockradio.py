import unittest
import logging
import sys

from adblockradio.adblockradio import App, ConsoleApp


class TestApp(unittest.TestCase):
    def test___init___without_args(self):
        app = App([])
        self.assertIsNotNone(app._player)
        self.assertIsNotNone(app.run)
        app.terminate()


class TestConsole(unittest.TestCase):
    def test___init__(self):
        app = ConsoleApp()
        self.assertIsNotNone(app._player)
        self.assertIsNotNone(app.run)
        app.terminate()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    unittest.main()
