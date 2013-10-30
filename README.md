Noncontracting-Grammar
======================

a [Noncontracting Grammar](http://en.wikipedia.org/wiki/Noncontracting_grammar) written in Python 2.7

g1 ... g5 are test files 

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