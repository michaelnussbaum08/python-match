import re

#TODO: lots of error checking, making sure same amounts of things, proper types

def match(match_on, cases):
    '''string, ordered dictionary mapping MatchKey objects
    to strings of python code -> void, executes matching code'''
    for case, consequence in cases.items():
        match_result = case.is_match(match_on)
        if match_result[0]:
            new_vars = match_result[1]
            locals().update(new_vars)
            exec(consequence)

class MatchKey(object):
    '''To be used as a dictionary key in the match function.
    Uses a pattern string to define a regex to match on.
    Identifies values identified by "%M" tokens in the pattern,
    which are represented as wildcards in the regex, so that
    they can be bound as variables.'''

    def __init__(self, pattern, sub_ins, to_binds):
        '''string, list of strings, list of strings
        Strings in sub_ins will be subbed in for '%s' tokens.
        Strings in to_binds will be variable names.'''
        self._to_binds = to_binds
        self._subbed_in = self._normal_sub(pattern, sub_ins)
        self._char_indices_to_bind = [m.start() for m in \
          re.finditer('%M', self._subbed_in)]
        self._word_indices_to_bind = [index for index, word in \
          enumerate(self._subbed_in.split()) if word == "%M"]

        if len(self._char_indices_to_bind) != len(to_binds):
            raise Exception("Number of format tokens doesn't" +\
              "match format args")

    def is_match(self, match_on):
        '''string -> boolean, dict mapping bindings to values'''
        key = self._get_key()
        regex_match = re.match(key, match_on)
        if hasattr(regex_match, 'group') and \
          regex_match.group(0) == match_on:
            match = True
            bindings = self._bindings(match_on)
        else:
            match = False
            bindings = {}
        return match, bindings

    def _bindings(self, match_on):
        '''string -> dict mappings bindings to values'''
        bindings = {}
        for count, var in enumerate(self._to_binds):
            bindings[var] = match_on.split()[\
              self._word_indices_to_bind[count]]
        return bindings

    def _get_next_word(self, words, start_index):
        '''string, integer -> string'''
        total_index = None
        for index, char in enumerate(words[start_index:]):
            total_index = index + start_index
            if char == ' ':
                return words[start_index:total_index]
            elif total_index == len(words) - 1:
                return words[start_index:total_index+1]

    def _normal_sub(self, pattern, sub_ins):
        '''string, tuple -> string
        Replaces %s in patter with sub_ins in order'''
        char_index = 0
        subbed_count = 0
        subbed_in = ''
        while char_index < len(pattern):
            char = pattern[char_index]
            try:
                next_char = pattern[char_index+1]
            except IndexError:
                next_char = None

            if char == '%' and next_char != 'M':
                #preserve proper string formatting
                to_sub = sub_ins[subbed_count]
                #TODO: change string formatting so it works with < 2.7
                subbed_in += "{}".format(to_sub)
                char_index += 2
                subbed_count += 1
            else:
                subbed_in += char
                char_index += 1
        return subbed_in

    def _get_key(self):
        '''void -> string
        Replaces %M in _subbed_in with regex wildcards'''
        match_string = ''
        char_index = 0
        while char_index < len(self._subbed_in):
            char = self._subbed_in[char_index]
            if char_index in self._char_indices_to_bind:
                match_string += '[^ ]*'
                #extra jump to get over token
                char_index += 2
            else:
                match_string += char
                char_index += 1
        return match_string
