import unittest

from open_eos import open_eos

# Path to which all other EOS locations are relative
EOS_ROOT = 'root://eoslhcb.cern.ch//eos/lhcb/user/a/apearce/CharmProduction'
# Path relative to EOS_ROOT containing test files
FIXTURES_DIR = 'fixtures'
# A non-empty file that should be readable by eos_open
TEST_FILE = 'test.txt'


class TestOpenEOS(unittest.TestCase):
    def test_open_eos(self):
        path = '{0}/{1}/{2}'.format(EOS_ROOT, FIXTURES_DIR, TEST_FILE)
        try:
            with open_eos(path) as f:
                self.assertGreater(len(f.readlines()), 0)
        except IOError as e:
            self.fail('IOError: ' + e.message)


if __name__ == '__main__':
    unittest.main()
