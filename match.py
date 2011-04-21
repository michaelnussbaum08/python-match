import re

#TODO: lots of error checking, making sure same amounts of things, proper types

class MatchKey(object):

    def __init__(self, pattern, sub_ins, to_binds):
        '''string, list, list'''
        self._to_binds = to_binds
        self._subbed_in = self._normal_sub(pattern, sub_ins)
        self._indices_to_bind = [m.start() for m in \
          re.finditer('%M', self._subbed_in)]

        if len(self._indices_to_bind) != len(to_binds):
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
            #TODO: not getting a second binding
            bindings[var] = self._get_next_word(match_on,
              self._indices_to_bind[count])
        return bindings

    def _get_next_word(self, words, start_index):
        '''string, integer -> string'''
        total_index = None
        print words[start_index:]
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
        #TODO: pull out keywords and bind them
        match_string = ''
        char_index = 0
        while char_index < len(self._subbed_in):
            char = self._subbed_in[char_index]
            if char_index in self._indices_to_bind:
                match_string += '[^ ]*'
                #extra jump to get over token
                char_index += 2
            else:
                match_string += char
                char_index += 1
        return match_string
