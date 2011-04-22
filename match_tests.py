import unittest

from match import match, MatchKey
from errors import MatchError

class MatchKeyTest(unittest.TestCase):

    def test_empty_pattern(self):
        match_key = MatchKey('', [], [])
        self.assertEquals(match_key._subbed_in, '')
        self.assertEquals(match_key._char_indices_to_bind, [])
        self.assertEquals(match_key._word_indices_to_bind, [])
        self.assertEquals(match_key._to_binds, [])

    def test_too_many_binding_tokens(self):
        self.assertRaises(MatchError, MatchKey, 'test %M %M', [],
          ['var1'])

    def test_too_few_binding_tokens(self):
        self.assertRaises(MatchError, MatchKey, 'test %M', [],
          ['var1', 'var2'])

    def test_normal_sub_no_sub(self):
        match_key = MatchKey('', [], [])
        subbed_in = match_key._normal_sub('test', [])
        self.assertEquals(subbed_in, 'test')

    def test_normal_sub_no_match_tokens(self):
        match_key = MatchKey('', [], [])
        subbed_in = match_key._normal_sub('test %s %s',
          ['and', 'this'])
        self.assertEquals(subbed_in, 'test and this')

    def test_normal_sub_with_match_tokens(self):
        match_key = MatchKey('', [], [])
        subbed_in = match_key._normal_sub('test %M %s',
          ['this'])
        self.assertEquals(subbed_in, 'test %M this')

    def test_char_indices_to_bind(self):
        match_key = MatchKey('a %M %M', [], ['var1', 'var2'])
        self.assertEquals(match_key._char_indices_to_bind,
          [2, 5])

    def test_word_indices_to_bind(self):
        match_key = MatchKey('a %M %M' , [], ['var1', 'var2'])
        self.assertEquals(match_key._word_indices_to_bind,
          [1, 2])

    def test_no_bindings(self):
        match_key = MatchKey('test', [], [])
        bindings = match_key._bindings('not test')
        self.assertDictEqual({}, bindings)


if __name__=="__main__":
    unittest.main()
