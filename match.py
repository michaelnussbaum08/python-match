import re


class MatchKey(object):

    def __init__(self, pattern, sub_ins, to_binds):
        '''string, tuple, tuple'''
        self._to_binds = to_binds
        self._subbed_in = self._normal_sub(pattern, sub_ins)
        self._indices_to_bind = [m.start() for m in \
          re.finditer('%M', self._subbed_in)]

        #single tuple args become not tuples, check what we have
        if(isinstance(self._to_binds, str) and \
          len(self._indices_to_bind) != 1):
            raise Exception("Number of format tokens doesn't" +\
              "match format args")

        if(isinstance(self._to_binds, tuple) and \
          len(self._indices_to_bind) != len(self._to_binds)):
            raise Exception("Number of format tokens doesn't" +\
              "match format args")


    def _normal_sub(self, pattern, sub_ins):
        '''string, tuple -> string
        Replaces %s in patter with sub_ins in order'''
        char_index = 0
        subbed_count = 0
        subbed_in = ''
        while char_index < len(pattern):
            print subbed_in
            char = pattern[char_index]
            try:
                next_char = pattern[char_index+1]
            except IndexError:
                next_char = None

            if char == '%' and next_char != 'M':
                #preserve proper string formatting
                if isinstance(sub_ins, tuple):
                    to_sub = sub_ins[subbed_count]
                else:
                    to_sub = sub_ins
                print to_sub
                subbed_in += "{}".format(to_sub)
                char_index += 2
                subbed_count += 1
            else:
                subbed_in += char
                char_index += 1
        return subbed_in

    def get_key(self):
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
