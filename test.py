#!/usr/bin/env python3
import unittest

from combinations import generate_plug_settings, generate_ring_settings, ALPHABET


class TestPlugCombinations(unittest.TestCase):

    def testNoPlugs(self):
        """ No plugs at all """
        gen = generate_plug_settings(0)
        p = []
        expected_len = 1
        try:
            while True:
                p.append(next(gen))
                if len(p) > expected_len:
                    break
        except StopIteration:
            pass

        self.assertEqual(len(p), expected_len)
        self.assertEqual(p[0], '')

    def testOnePlugConnection(self):
        """ All combinations with one plug connection """
        gen = generate_plug_settings(1)
        p = []
        k = len(ALPHABET)
        expected_len = k*(k-1)//2
        try:
            while True:
                p.append(next(gen))
                if len(p) > expected_len:
                    break
        except StopIteration:
            pass

        self.assertEqual(len(p), expected_len)
        # check that all elements are unique
        self.assertEqual(len(set(p)), expected_len)

    def testOnePlugConnectionWithUnused(self):
        """ All combinations with one plug connection, but only some characters used """
        unused = set(ALPHABET[2:])
        gen = generate_plug_settings(1, unused)
        p = []
        expected_len = 50
        try:
            while True:
                p.append(next(gen))
                if len(p) > expected_len:
                    break
        except StopIteration:
            pass

        self.assertEqual(len(p), expected_len)
        # check for empty combination
        self.assertIn('', p)
        # check that all elements are unique
        self.assertEqual(len(set(p)), expected_len)


class TestRingSettingCombinations(unittest.TestCase):

    def testAllCombinations(self):
        gen = generate_ring_settings()
        p = []
        expected_len = len(ALPHABET)**3
        try:
            while True:
                p.append(next(gen))
                if len(p) > expected_len:
                    break
        except StopIteration:
            pass

        self.assertEqual(len(p), expected_len)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
