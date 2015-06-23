import collections
import argparse

class TreeAutomaton:
    def __init__(self, nonterminals = [], nodes = [], leaves = [], startsymbols = [], productions = {}):
        sInN = True
        for symbol in startsymbols:
            if not symbol in nonterminals:
                sInN = False
        if sInN:
            self.N = nonterminals
            self.E = nodes
            self.Q = leaves
            self.S = startsymbols
            self.P = productions
            self.P_rev = reverse(self.P)
        else: print "Error: Not every Symbol in S is also in N."

    # def buildRule(self, treepart):
    # for element in treepart:

    def treeRule(rightside):
        #if rightside
        pass


    def checkHelper(self, subtree, ruleDict, count):

        # works basically similar to check(), with a few differences (more parameters, no check for startsymbols, ...)
        rule = ruleDict.keys()
        trees = []
        counter2 = count
        if not len(subtree) == len(rule):
            pass
        else:
            counter = 0
            for node in subtree:
                tmptree = collections.OrderedDict()
                el, nodeid = node.split("_")
                for rightside in self.P[rule[counter].split("_")[0]]:
                    if rightside[0].isalpha():
                        if rightside[0] == el:
                            if rightside[0].isupper():
                                tmptree = makeTree2(parseTreeString(rightside))[0]
                                for tmproot in tmptree:
                                    subtreelist = self.checkHelper(subtree[node], tmptree[tmproot], counter)
                                    tmptree[tmproot] = collections.OrderedDict()
                                    for subtree2 in subtreelist:
                                        for key in subtree2:
                                            tmptree[tmproot][key] = subtree2[key]
                            elif rightside[0].islower():
                                if not rightside == el:
                                    print "impossible"
                                else:
                                    tmptree[rightside[0]+"_0"] = "__NONE__"

                    else: print "This should not happen. (check helper 2)"
                trees.append(tmptree)
                counter+=1
                counter2+=1
        return trees

    def check(self, tree):
        parseforest = []
        counter = 0
        for node in tree:
            tmptree = collections.OrderedDict()
            el, nodeid = node.split("_")
            for leftside in self.P:
                # left side of production
                if leftside in self.S:
                    # is it a start symbol?
                    for rightside in self.P[leftside]:
                        # right side of production
                        if rightside[0].isalpha():
                            # is the first character of right side a letter (should alway be)
                            if rightside[0] == el:
                                # is the first character of right side the same as the node?
                                if rightside[0].isupper():
                                    # is the character uppercase? --> Has children
                                    tmptree = makeTree2(parseTreeString(rightside))[0]
                                    for tmproot in tmptree:
                                        subtreelist = self.checkHelper(tree[node], tmptree[tmproot], counter)
                                        tmptree[tmproot] = collections.OrderedDict()
                                        for subtree in subtreelist:
                                            for key in subtree:
                                                tmptree[tmproot][key] = subtree[key]

                                elif rightside[0].islower():
                                    # is the character lowercase? --> has no children
                                    pass
                                    # since we are in the first iteration (should only be root)
                        else: print "This should not happen. (check 2)"
                    parseforest.append(tmptree)
            counter+=1
        return parseforest


def reverse(dictionary):
    newDict = {}
    for element in dictionary:
        for v in dictionary[element]:
            if not v in newDict.keys():
                newDict[v] = []
            if not element in newDict[v]:
                newDict[v].append(element)
    return newDict

# parses the whole input string
def parseInput(instring):
    return instring.split(" ")

# parses the tree part of the input string, returns list representation
def parseTreeString(tree):
    stack = [[]]
    for x in tree:
        if x == '(':
            stack[-1].append([])
            stack.append(stack[-1][-1])
        elif x == ')':
            stack.pop()
            if not stack:
                return 'error: opening bracket is missing'
                # raise ValueError('error: opening bracket is missing')
        else:
            stack[-1].append(x)
    if len(stack) > 1:
        return 'error: closing bracket is missing'
        # raise ValueError('error: closing bracket is missing')
    return stack.pop()


def makeTree2(tree, nodeid = 0):

    # returns dictionary representation of tree in list representation, can also handle n1, n2, n3, ... for the check() function of the automaton
    tmpid = nodeid
    treeDict = collections.OrderedDict()
    for number, element in enumerate(tree):
        if str(type(element)) == "<type 'list'>": pass
        elif str(type(element)) == "<type 'str'>":
            if element.isalpha() and element.isupper():
                try:
                    if str(type(tree[number+1])) == "<type 'list'>":
                        tmpid+=1
                        treeDict[element+"_"+str(tmpid)], tmpid = makeTree2(tree[number+1], tmpid)
                    else:
                        tmpid+=1
                        treeDict[element+"_"+str(tmpid)] = "__NONE__"
                except IndexError:
                    tmpid+=1
                    treeDict[element+"_"+str(tmpid)] = "__NONE__"
            elif element.isalpha() and element.islower():
                if tree[number+1].isdigit():
                    tmpelement = element+str(tree[number+1])
                    tmpid+=1
                    treeDict[tmpelement+"_"+str(tmpid)] = "__NONE__"
                else:
                    tmpid+=1
                    treeDict[element+"_"+str(tmpid)] = "__NONE__"
            elif element == "#":
                tmpid+=1
                treeDict[element+"_"+str(tmpid)] = "__NONE__"
            elif element == ",": pass
            elif element.isdigit(): pass
            else: print "This should not happen (makeTree2 1)"+str(element)
        else:
            print "This should not happen (makeTree2 2) " +str(type(element))
    return treeDict, tmpid

def makeTree(tree, nodeid = 0):

    # returns dictionary representation of tree in list representation
    tmpid = nodeid
    treeDict = collections.OrderedDict()
    for number, element in enumerate(tree):
        if str(type(element)) == "<type 'list'>": pass
        elif str(type(element)) == "<type 'str'>":
            if element.isalpha() and element.isupper():
                try:
                    if str(type(tree[number+1])) == "<type 'list'>":
                        tmpid+=1
                        treeDict[element+"_"+str(tmpid)], tmpid = makeTree(tree[number+1], tmpid)
                    else:
                        tmpid+=1
                        treeDict[element+"_"+str(tmpid)] = "__NONE__"
                except IndexError:
                    tmpid+=1
                    treeDict[element+"_"+str(tmpid)] = "__NONE__"
            elif element.isalpha() and element.islower():
                tmpid+=1
                treeDict[element+"_"+str(tmpid)] = "__NONE__"
            elif element == "#":
                tmpid+=1
                treeDict[element+"_"+str(tmpid)] = "__NONE__"
            elif element == ",": pass
            else: print "This should not happen (makeTree 1) "+str(element)
        else:
            print "This should not happen (makeTree 2 " +str(type(element))
    return treeDict, tmpid

#converts the tree back to a string
def write(tree):
    output = ""
    counter = 0
    for element in tree:
        counter+=1
        el, nodeid = element.split("_")
        if str(type(tree[element])) == "<class 'collections.OrderedDict'>":
            if counter == len(tree):
                output += el+"("+str(write(tree[element]))+")"
            else:
                output += el+"("+str(write(tree[element]))+"),"
        else:
            if counter == len(tree):
                output +=el
            else:
                output +=el+","

    return output

def lines( filestream ):

    # Generator that reads inputfiles linewise

    for line in filestream:
        yield line

def read(startsymbols, productions):

    # Creates N, E, Q, S, P out of two lists, containing the startsymbols and the productions

    N = []
    E = []
    Q = []
    S = []
    P = {}
    for line in lines(open(productions)):
        tmp = line.split("->")
        if not tmp[0].strip() in N:
            N.append(tmp[0].strip())

        counter=0
        for char in tmp[1].strip():
            if char.isupper():
                if not char in E:
                    E.append(char)
            elif char.islower():
                if not (counter+1) == (len(tmp[1].strip())):
                    if not tmp[1].strip()[counter+1].isdigit():
                        if not char in Q:
                            Q.append(char)
                else:
                    if not char in Q:
                        Q.append(char)
            counter+=1
        if tmp[0].strip() in P.keys():
            P[tmp[0].strip()].append(tmp[1].strip())
        else:
            P[tmp[0].strip()] = []
            P[tmp[0].strip()].append(tmp[1].strip())
    for line in lines(open(startsymbols)):
        S.append(line.strip())

    return N, E, Q, S, P

def normalform(N, P):
    # if necessary, converts productions to normalform, and, if necessary adds symbols to the nonterminals
    normalP = {}
    normalN = N
    converting = False
    for leftside in P:
        normalP[leftside] = []
        for rightside in P[leftside]:
            if len(rightside) > 1:
                tree, nodeid = makeTree2(parseTreeString(rightside))
                for root in tree.keys():
                    r, no2 = root.split("_")
                    newstring = r+"(" # this is going to be the replacement for the old production (something is replaced by a nonterminal)
                    childcounter=1
                    for child in tree[root]:
                        c, no1 = child.split("_")
                        if child[0].isupper():
                            # this means, the grammar is not in normal form
                            converting = True
                            counter = 0
                            while "n"+str(counter) in P.keys(): # generating a number for a new, not yet existing nonterminal
                                counter+=1
                            while "n"+str(counter) in normalP.keys():
                                counter+=1
                            newchilds = []
                            newstring2 = c+"(" # this is going to be the right side of the new rule
                            counter2 = 1
                            for i1 in  tree[root][child].keys():
                                i2, i3 = i1.split("_")
                                if counter2 == len(tree[root][child].keys()):
                                    newstring2+=i2
                                else:
                                    newstring2+=i2+","
                                counter2+=1
                            newstring2+=")"
                            ruleexists = False
                            for leftside2 in P: # check if needed production already exists
                                for rightside2 in P[leftside2]:
                                    if rightside2 == newstring2:
                                        ruleexists = True
                            if not ruleexists: normalP["n"+str(counter)] = [newstring2] # if needed production doesn't exists, it's generated here
                            if childcounter == len(tree[root]):
                                newstring+="n"+str(counter)
                            else:
                                newstring+="n"+str(counter)+","
                        else:
                            if childcounter == len(tree[root]):
                                newstring+=c
                            else:
                                newstring+=c+","
                        childcounter+=1
                    newstring+=")"
                    normalP[leftside].append(newstring)
            else: normalP[leftside].append(rightside)
    for k in normalP.keys(): # here the new Nonterminal list is generated
        if not k in normalN:
            normalN.append(k)
    if converting: print "Converting grammar to normal form ...\n"
    else: print "Grammar is in normal form.\n"
    return normalN, normalP

def run(s):

    argpar = argparse.ArgumentParser(description='')

    argpar.add_argument('-s','--startsymbols',dest='starts',help='startsymbols',required=True)
    argpar.add_argument('-p','--productions',dest='prods',help='productions',required=True)
    argse = argpar.parse_args()

    N, E, Q, S, P = read(argse.starts, argse.prods)

    Nn, Pn = normalform(N, P)

    TA = TreeAutomaton(Nn, E, Q, S, Pn)

    print "Input string:\n\t" + str(s)
    commands = parseInput(s)
    print "Tree string:\n\t" + str(commands[0])

    #This block checks if the input string is correctly formatted.
    if len(commands) > 1:
        print "To many arguments given."
        return

    tree, nodeid = makeTree(parseTreeString(commands[0]))
    parses = TA.check(tree)

    accepted = False
    for x in parses:
        if write(x) == commands[0]: accepted = True
    print accepted


#############
"""
treestringlist = [
    "A(A(b,a),b)",
    "A(A(b,a),B(a,b))",
    "A(B(a,b),b)",
    "A(A(b,B(a,b)),a)",
    ]
for t in treestringlist:
    run(t)
    print "________________________________"

"""
#treestring = "A(A(b,a),b)"
treestring = raw_input("Input string in defined format:\n")
run(treestring)


