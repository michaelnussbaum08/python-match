import re

from errors import MatchError

#TODO: bind locals and globals with inspect.getouterframes(inspect.currentframe())[0][0].f_locals
#TODO: lots of error checking, making sure same amounts of things, proper types
#TODO: match things other then strings

def match(match_on, cases, local_vars={}, global_vars={}):
    '''string, ordered dictionary mapping MatchKey objects
    to strings of python code -> void, executes matching code'''
    locals().update(local_vars)
    globals().update(global_vars)
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
        '''string, list of strings, list of strings and (function, string)
        Strings in sub_ins will be subbed in for '%s' tokens.
        Functions in to_binds take one arg, the variable they
        might bind, and they must return a boolean.  If the
        function returns False then the pattern doesn't match.
        Strings in to_binds will be bound to variable names.'''
        self._bind_conditions, self._to_binds  = self._extract_binds(to_binds)
        self._subbed_in = self._normal_sub(pattern, sub_ins)
        self._char_indices_to_bind = [m.start() for m in \
          re.finditer('%M', self._subbed_in)]
        self._word_indices_to_bind = [index for index, word in \
          enumerate(self._subbed_in.split()) if word == "%M"]

        if len(self._char_indices_to_bind) != len(to_binds):
            raise MatchError("Number of format tokens doesn't" +\
              "match format args")

    def is_match(self, match_on):
        '''string -> boolean, dict mapping bindings to values'''
        key = self._get_key()
        regex_match = re.match(key, match_on)
        if hasattr(regex_match, 'group') and \
          regex_match.group(0) == match_on:
            match = True
            bindings = self._bindings(match_on)
            if not self._valid_bind_conditions(bindings):
                match = False
                bindings = {}
        else:
            match = False
            bindings = {}
        return match, bindings

    def _extract_binds(self, to_binds):
        '''list of strings and (function, string) ->
            dictionary mapping ints to functions, list of strings'''
        conditions = {}
        var_names = []
        for index, value in enumerate(to_binds):
            if isinstance(value, str):
                var_names.append(value)
            elif isinstance(value, tuple):
                var_names.append(value[1])
                conditions[index] = value[0]
        return conditions, var_names

    def _valid_bind_conditions(self, bindings):
        '''dict mapping bindings to values -> boolean'''
        is_valid = True
        for index, new_var in enumerate(self._to_binds):
            if index in self._bind_conditions:
                condition_fun = self._bind_conditions[index]
                if not condition_fun(bindings[new_var]):
                    is_valid = False
        return is_valid

    def _bindings(self, match_on):
        '''string -> dict mappings bindings to values'''
        bindings = {}
        for count, var in enumerate(self._to_binds):
            bindings[var] = match_on.split()[\
              self._word_indices_to_bind[count]]
        return bindings

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
                to_sub = sub_ins[subbed_count]
                subbed_in += str(to_sub)
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
