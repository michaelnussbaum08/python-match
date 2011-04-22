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
        bindings = match_key._bindings('test a')
        self.assertDictEqual({}, bindings)

    def test_bindings(self):
        match_key = MatchKey('test %M %M', [], ['var1', 'var2'])
        bindings = match_key._bindings('test a b')
        self.assertDictEqual({'var1':'a', 'var2':'b'}, bindings)

    def test_get_key_no_wildcard(self):
        match_key = MatchKey('test', [], [])
        self.assertEquals(match_key._get_key(), 'test')

    def test_get_key_with_wildcard(self):
        match_key = MatchKey('test %M %M', [], ['var1', 'var2'])
        self.assertEqual(match_key._get_key(), 'test [^ ]* [^ ]*')

    def test_is_match_all_wrong(self):
        match_key = MatchKey('test this', [], [])
        result = match_key.is_match('nope na')
        self.assertFalse(result[0])
        self.assertDictEqual(result[1], {})

    def test_is_match_partial_front_match(self):
        match_key = MatchKey('test this', [], [])
        result = match_key.is_match('test na')
        self.assertFalse(result[0])
        self.assertDictEqual(result[1], {})

    def test_is_match_partial_back_match(self):
        match_key = MatchKey('test this', [], [])
        result = match_key.is_match('nope this')
        self.assertFalse(result[0])
        self.assertDictEqual(result[1], {})

    def test_is_match_wilds_match(self):
        match_key = MatchKey('test %M %M', [], ['var1', 'var2'])
        result = match_key.is_match('test yup this')
        self.assertTrue(result[0])
        self.assertDictEqual(result[1], {'var1':'yup', 'var2':'this'})

    def test_is_match_wild_no_match_front(self):
        match_key = MatchKey('test %M', [], ['var1'])
        result = match_key.is_match('almost but')
        self.assertFalse(result[0])
        self.assertDictEqual(result[1], {})

    def test_is_match_wild_no_match_end(self):
        match_key = MatchKey('test %M nope', [], ['var1'])
        result = match_key.is_match('test yup almost')
        self.assertFalse(result[0])
        self.assertDictEqual(result[1], {})

if __name__=="__main__":
    unittest.main()
