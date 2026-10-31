import os, sys, socket
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import measure, verdict


class TestVpnLatency(unittest.TestCase):
    def test_local_server_measurable(self):
        srv = socket.socket(); srv.bind(("127.0.0.1", 0)); srv.listen(1)
        port = srv.getsockname()[1]
        try:
            samples = measure("127.0.0.1", port, count=2)
            self.assertEqual(len(samples), 2)
            self.assertTrue(all(s is not None for s in samples))
        finally:
            srv.close()

    def test_unreachable_verdict(self):
        self.assertEqual(verdict([None, None]), ("unreachable", None))

    def test_good_band(self):
        self.assertEqual(verdict([10.0, 20.0])[0], "good")
