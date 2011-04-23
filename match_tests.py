import unittest

from match import match, MatchKey
from errors import MatchError
'''
class MatchTest(unittest.TestCase):

   def test_empty(self):
       result = match('test', {})
       print result
'''
class MatchKeyTest(unittest.TestCase):

    def setUp(self):
        self.true_fun = lambda x: True
        self.false_fun = lambda x: False

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

    def test_condition_false_no_match(self):
        match_key = MatchKey('test %M', [], [(is_a, 'var1')])
        result = match_key.is_match('test b')
        self.assertFalse(result[0])
        self.assertDictEqual(result[1], {})

    def test_condition_is_match(self):
        match_key = MatchKey('test %M', [], [(is_a, 'var1')])
        result = match_key.is_match('test a')
        self.assertTrue(result[0])
        self.assertDictEqual(result[1], {'var1':'a'})

    def test_condition_is_match_mixed_args(self):
        match_key = MatchKey('test %M %M', [], [(is_a, 'var1'), 'var2'])
        result = match_key.is_match('test a b')
        self.assertTrue(result[0])
        self.assertDictEqual(result[1], {'var1':'a', 'var2':'b'})

    def test_extract_binds_strings(self):
        match_key = MatchKey('', [], [])
        binds = match_key._extract_binds(['var1', 'var2'])
        self.assertEquals(binds[1], ['var1', 'var2'])
        self.assertDictEqual(binds[0], {})

    def test_extract_binds_tuples(self):
        def not_is_a(x):
            return not is_a(x)
        match_key = MatchKey('', [], [])
        binds = match_key._extract_binds([(is_a, 'var1'),
          (not_is_a, 'var2')])
        self.assertEquals(binds[1], ['var1', 'var2'])
        self.assertDictEqual(binds[0], {0:is_a,
          1:not_is_a})

    def test_extract_binds_mixed_args(self):
        match_key = MatchKey('', [], [])
        binds = match_key._extract_binds([(is_a, 'var1'), 'var2'])
        self.assertEquals(binds[1], ['var1', 'var2'])
        self.assertDictEqual(binds[0], {0:is_a})

def is_a(x):
    if x == 'a':
        return True
    return False



if __name__=="__main__":
    unittest.main()
