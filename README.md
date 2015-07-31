# simple-tree-automaton
A simple tree automaton

[![Code Issues](http://www.quantifiedcode.com/api/v1/project/8710eecb3a4440e6885983c255266775/badge.svg)](http://www.quantifiedcode.com/app/project/8710eecb3a4440e6885983c255266775)

How to run program?

```
python <program-name>.py -s <startsymbols> -p <productions>
```

The startsymbols file lists the startsymbols per line. The grammar is stored in the productions file. It has to be a regular tree grammar (RTG). The productions file stores the productions in Tiburon format.

* n0 → A(n1,n2) : non-terminal n0 goes to the tree rooted in A with nonterminals n1 and n2
* n1 → a : non-terminal n1 goes to the leaf symbol a
* n2 → b : non-terminal n2 goes to the leaf symbol b

For details see the example files "startsymbols.txt" and "productions.txt"

As input, you write a tree as a string composed of nodes, opening/closing brackets and commas:

* A
* A(a,B(b,c))
* A(B(a,b),C(D(d,e)))

As output you'll get _True_ if the automaton accepts the tree given the start symbols and the productions, or _False_, if not.
