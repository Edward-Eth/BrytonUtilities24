import unittest
import os
import sys

from BrytonUtilities import gpx_utilities


class Test_gpx_utilities(unittest.TestCase):
    """Test cases for the functions in the gpx_utilities file."""

    def test_gpx_ors(self):
        # I don't use this website, it's crap in my opinion so I'm not going to make unit tests for it.
        self.assertIsNone(None)

    def test_decode_gpx_plotaroute(self):
        # Find path to test file
        gpx_path = os.path.join(
            os.path.dirname(os.path.split(os.path.abspath(__file__))[0]),
            "testData",
            "PAR.gpx",
        )
        decoded_route = gpx_utilities.decode_gpx_plotaroute(gpx_path)

        routeAsAList = list(
            zip(
                decoded_route["latitude"],
                decoded_route["longitude"],
                decoded_route["Instruction"],
                decoded_route["name"],
                decoded_route["altitude"],
            )
        )

        for i, routePoint in enumerate(routeAsAList):
            self.assertAlmostEqual(float(routePoint[0]), 50 + i * 0.00001, 6)
            self.assertAlmostEqual(float(routePoint[1]), i * 0.00001, 6)


if __name__ == "__main__":
    unittest.main()
