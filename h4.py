#!/usr/bin/python
# -*- coding: latin-1 -*-
# Kyle Falconer
# CSC 333 - Fall 2012 - Homework 4
# Time-stamp: <2012-10-16 00:15 CDT>
#
#    Copyright 2012 Kyle Falconer
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
h4.py reads a noncontracting grammar G from standard input,
  followed by a line containing * and then zero or more strings,
  one per line. For each string x, the program must output the 
  line yes if x is derivable from G and no otherwise. Noncontracting 
  grammars define the context-sensitive languages (or CSLs). 
  Historically, the CSLs were defined by context-sensitive grammars, 
  but noncontracting grammars are more common in modern usage.

Usage: at shell prompt
    $ echo -n "S -> abc\n\tS -> aSBc\n\tBc -> cB\n\tcB -> Bc\n\tbB -> bb\n\t*\n\taabbcc\n\tababbcc" > test.txt
    $ python h4.py < test.txt
"""

from collections import deque
import re, time
class NCG:
    """
    rules are of the form
    \tα → β where |α| ≤ |β|, where |α| denotes the length of α.
    terminal symbols are lowercase letters and uppercase letters are variables

    """

    def __init__(self):
        self.rules = []



    def parse_rule(self, rule):
        """
        parse and insert a rule given as a string in the form "a -> b"
        """
        R = rule.split(' ')
        self.add_rule(R[0], R[2])


    def add_rule(self, LHS, RHS):
        """
        inserts a rule which is composed of variables and terminal symbols.
        LHS → RHS
        """
        self.rules.append((LHS, RHS, re.compile(r'(?=('+re.escape(RHS)+'))')))


    def replace_iter(self, pattern, replacement_string, haystack):
        """
        replace_iter makes a replacement over each of the possible matches in haystack.

        pattern -- a compiled RegEx against which the search is run.
        replacement_string -- the string which is to replace any matches.
        haystack -- the string which the searches were made
        returns a list of the modified strings.
        
        """
        resultants = []
        matches = re.finditer(pattern, haystack)
        for match in matches:
            indices = match.span(1)
            mutation = haystack[0:indices[0]]+replacement_string+haystack[indices[1]:]
            if mutation not in self.C:
                resultants.append(mutation)

        #print str(resultants)+' '+str(haystack)
        return resultants


    def derivable(self, x):
        """
        Performs a bottom-up, breadth-first search of the possible derivations of x using
        the rules defined in this grammar. Backed with a Queue.
        return True if x is derivable from this grammar.
        This implementation is quite slow, to the point of being exponential.
        I suspect the speed issue is due to duplicates in the Q.
        """
        S = self.rules[0][0]
        self.Q = deque()    # yet to consider
        self.Q.append(x)
        self.C = []          # already considered

        while len(self.Q) > 0:
            current_string = self.Q.pop()
            if current_string is S:
                self.add_rule(S, x)
                return True
            if current_string not in self.C:
                
                self.C.append(current_string)
                for rule in self.rules:
                    self.Q.extend(self.replace_iter(rule[2], rule[0], current_string))
        return False

   
    def derivable2(self, x):
        """
        Performs a bottom-up, semi-random breadth-first search of the possible derivations of x using
        the rules defined in this grammar. Backed with a Set.
        return True if x is derivable from this grammar.
        This implementation is significantly faster than the one backed with the Queue.
        """
        S = self.rules[0][0]
        self.Q = set()      # yet to consider
        self.C = set()       # already considered

        # derivable_timer = 0
        # replace_iter_timer = 0
        # d_timer = time.time()


        self.Q.add(x)
        while len(self.Q) > 0:
            current_string = self.Q.pop()
            # print current_string+""
            if current_string is S:
                self.add_rule(S, x)

                # d2_timer = time.time()
                # derivable_timer = (d2_timer-d_timer)-replace_iter_timer
                # print '%s took %0.3f ms' % ("derivable", (derivable_timer)*1000.0)
                # print '%s took %0.3f ms' % ("replace_iter", (replace_iter_timer)*1000.0)
                return True
            if current_string not in self.C:                
                self.C.add(current_string)
                for rule in self.rules:
                    # r_timer = time.time()
                    self.Q.update(set(self.replace_iter(rule[2], rule[0], current_string)))
                    # r2_timer = time.time()
                    replace_iter_timer+=r2_timer-r_timer
                
        # d2_timer = time.time()
        # derivable_timer = (d2_timer-d_timer)-replace_iter_timer
        # print '%s took %0.3f ms' % ("derivable", (derivable_timer)*1000.0)
        # print '%s took %0.3f ms' % ("replace_iter", (replace_iter_timer)*1000.0)
        return False


    def describe(self):
        """
        return a string containing the rules in the grammar
        """
        description = ""
        for rule in self.rules:
            if rule is not None:
                description += str(rule[0])+" -> "+str(rule[1]) +"\n"

        return description



import sys, doctest
def main():

    doctest.testmod()

    args = sys.stdin
    test_strings = []
    grammar = NCG()

    saw_marker = False
    for line in args:
        if "*" is line.strip():
            saw_marker=True
            continue
        if not saw_marker:
            grammar.parse_rule(line.strip())
        else:
            test_strings.append(line.strip())

    for s in test_strings:
        # print "\n"+s
        print  "yes" if grammar.derivable(s) else "no"


if __name__ == '__main__':
    main()

