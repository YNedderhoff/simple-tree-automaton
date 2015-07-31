import collections
import argparse


class TreeAutomaton:
    def __init__(self, non_terminals, nodes, leaves, start_symbols, productions):
        s_in_n = True
        for symbol in start_symbols:
            if not symbol in non_terminals:
                s_in_n = False
        if s_in_n:
            self.N = non_terminals
            self.E = nodes
            self.Q = leaves
            self.S = start_symbols
            self.P = productions
            self.P_rev = reverse(self.P)
        else:
            print "Error: Not every Symbol in S is also in N."

    def check_helper(self, subtree, rule_dict, count):

        # works basically similar to check(), with a few differences (more parameters, no check for startsymbols, ...)
        rule = rule_dict.keys()
        trees = []
        if not len(subtree) == len(rule):
            pass
        else:
            counter = 0
            for node in subtree:
                tmp_tree = collections.OrderedDict()
                el, node_id = node.split("_")
                for right_side in (right_side for right_side in self.P[rule[counter].split("_")[0]] if
                                   right_side[0].isalpha() and right_side[0] == el):
                    if right_side[0].isupper():
                        tmp_tree = make_tree_2(parse_tree_string(right_side))[0]
                        for tmp_root in tmp_tree:
                            subtree_list = self.check_helper(subtree[node], tmp_tree[tmp_root], counter)
                            tmp_tree[tmp_root] = collections.OrderedDict()
                            for subtree2 in subtree_list:
                                for key in subtree2:
                                    tmp_tree[tmp_root][key] = subtree2[key]
                    elif right_side[0].islower():
                        if right_side == el:
                            tmp_tree[right_side[0] + "_0"] = "__NONE__"
                trees.append(tmp_tree)
                counter += 1
        return trees

    def check(self, tree):
        parse_forest = []
        counter = 0
        for node in tree:
            tmp_tree = collections.OrderedDict()
            el, node_id = node.split("_")
            for left_side in (left_side for left_side in self.P if left_side in self.S):
                # left side of production if it is it a start symbol
                for right_side in (right_side for right_side in self.P[left_side] if
                                   right_side[0].isalpha() and right_side[0] == el):
                    # right side of production if the first character of right side is a letter (should alway be)
                    # and the first character of right side is the same as the node
                    if right_side[0].isupper():
                        # is the character uppercase? --> Has children
                        tmp_tree = make_tree_2(parse_tree_string(right_side))[0]
                        for tmp_root in tmp_tree:
                            subtree_list = self.check_helper(tree[node], tmp_tree[tmp_root], counter)
                            tmp_tree[tmp_root] = collections.OrderedDict()
                            for subtree in subtree_list:
                                for key in subtree:
                                    tmp_tree[tmp_root][key] = subtree[key]
                parse_forest.append(tmp_tree)
            counter += 1
        return parse_forest


def reverse(dictionary):
    new_dict = {}
    for element in dictionary:
        for v in dictionary[element]:
            if v not in new_dict.keys():
                new_dict[v] = []
            if element not in new_dict[v]:
                new_dict[v].append(element)
    return new_dict


# parses the whole input string
def parse_input(instring):
    return instring.split(" ")


# parses the tree part of the input string, returns list representation
def parse_tree_string(tree):
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


def make_tree_2(tree, node_id=0):
    # returns dictionary representation of tree in list representation, can also handle n1, n2, n3, ... for the check()
    # function of the automaton
    tmp_id = node_id
    tree_dict = collections.OrderedDict()
    for number, element in enumerate(tree):
        if str(type(element)) == "<type 'list'>":
            pass
        elif str(type(element)) == "<type 'str'>":
            if element.isalpha() and element.isupper():
                try:
                    if str(type(tree[number + 1])) == "<type 'list'>":
                        tmp_id += 1
                        tree_dict[element + "_" + str(tmp_id)], tmp_id = make_tree_2(tree[number + 1], tmp_id)
                    else:
                        tmp_id += 1
                        tree_dict[element + "_" + str(tmp_id)] = "__NONE__"
                except IndexError:
                    tmp_id += 1
                    tree_dict[element + "_" + str(tmp_id)] = "__NONE__"
            elif element.isalpha() and element.islower():
                if tree[number + 1].isdigit():
                    tmpelement = element + str(tree[number + 1])
                    tmp_id += 1
                    tree_dict[tmpelement + "_" + str(tmp_id)] = "__NONE__"
                else:
                    tmp_id += 1
                    tree_dict[element + "_" + str(tmp_id)] = "__NONE__"
            elif element == "#":
                tmp_id += 1
                tree_dict[element + "_" + str(tmp_id)] = "__NONE__"
            elif element == ",":
                pass
            elif element.isdigit():
                pass
            else:
                print "This should not happen (makeTree2 1)" + str(element)
        else:
            print "This should not happen (makeTree2 2) " + str(type(element))
    return tree_dict, tmp_id


def make_tree(tree, node_id=0):
    # returns dictionary representation of tree in list representation
    tmp_id = node_id
    tree_dict = collections.OrderedDict()
    for number, element in enumerate(tree):
        if str(type(element)) == "<type 'list'>":
            pass
        elif str(type(element)) == "<type 'str'>":
            if element.isalpha() and element.isupper():
                try:
                    if str(type(tree[number + 1])) == "<type 'list'>":
                        tmp_id += 1
                        tree_dict[element + "_" + str(tmp_id)], tmp_id = make_tree(tree[number + 1], tmp_id)
                    else:
                        tmp_id += 1
                        tree_dict[element + "_" + str(tmp_id)] = "__NONE__"
                except IndexError:
                    tmp_id += 1
                    tree_dict[element + "_" + str(tmp_id)] = "__NONE__"
            elif element.isalpha() and element.islower():
                tmp_id += 1
                tree_dict[element + "_" + str(tmp_id)] = "__NONE__"
            elif element == "#":
                tmp_id += 1
                tree_dict[element + "_" + str(tmp_id)] = "__NONE__"
            elif element == ",":
                pass
            else:
                print "This should not happen (makeTree 1) " + str(element)
        else:
            print "This should not happen (makeTree 2 " + str(type(element))
    return tree_dict, tmp_id


# converts the tree back to a string
def write(tree):
    output = ""
    counter = 0
    for element in tree:
        counter += 1
        el, node_id = element.split("_")
        if str(type(tree[element])) == "<class 'collections.OrderedDict'>":
            if counter == len(tree):
                output += el + "(" + str(write(tree[element])) + ")"
            else:
                output += el + "(" + str(write(tree[element])) + "),"
        else:
            if counter == len(tree):
                output += el
            else:
                output += el + ","

    return output


def lines(file_stream):
    # Generator that reads inputfiles linewise

    for line in file_stream:
        yield line


def read(start_symbols, productions):
    # Creates N, E, Q, S, P out of two lists, containing the startsymbols and the productions

    n = []
    e = []
    q = []
    s = []
    p = {}
    for line in lines(open(productions)):
        tmp = line.split("->")
        if not tmp[0].strip() in n:
            n.append(tmp[0].strip())

        counter = 0
        for char in tmp[1].strip():
            if char.isupper():
                if not char in e:
                    e.append(char)
            elif char.islower():
                if not (counter + 1) == (len(tmp[1].strip())):
                    if not tmp[1].strip()[counter + 1].isdigit():
                        if char not in q:
                            q.append(char)
                else:
                    if char not in q:
                        q.append(char)
            counter += 1
        if tmp[0].strip() in p.keys():
            p[tmp[0].strip()].append(tmp[1].strip())
        else:
            p[tmp[0].strip()] = []
            p[tmp[0].strip()].append(tmp[1].strip())
    for line in lines(open(start_symbols)):
        s.append(line.strip())

    return n, e, q, s, p


def normal_form(n, P):
    # if necessary, converts productions to normalform, and, if necessary adds symbols to the nonterminals
    normal_p = {}
    normal_n = n
    converting = False
    for left_side in P:
        normal_p[left_side] = []
        for right_side in P[left_side]:
            if len(right_side) > 1:
                tree, node_id = make_tree_2(parse_tree_string(right_side))
                for root in tree.keys():
                    r, no2 = root.split("_")
                    new_string = r + "("  # this is going to be the replacement for the old production (something is replaced by a nonterminal)
                    child_counter = 1
                    for child in tree[root]:
                        c, no1 = child.split("_")
                        if child[0].isupper():
                            # this means, the grammar is not in normal form
                            converting = True
                            counter = 0
                            while "n" + str(
                                    counter) in P.keys():  # generating a number for a new, not yet existing nonterminal
                                counter += 1
                            while "n" + str(counter) in normal_p.keys():
                                counter += 1

                            new_string_2 = c + "("  # this is going to be the right side of the new rule
                            counter_2 = 1
                            for i1 in tree[root][child].keys():
                                i2, i3 = i1.split("_")
                                if counter_2 == len(tree[root][child].keys()):
                                    new_string_2 += i2
                                else:
                                    new_string_2 += i2 + ","
                                counter_2 += 1
                            new_string_2 += ")"
                            rule_exists = False
                            for left_side_2 in P:  # check if needed production already exists
                                for right_side_2 in P[left_side_2]:
                                    if right_side_2 == new_string_2:
                                        rule_exists = True
                            if not rule_exists: normal_p["n" + str(counter)] = [
                                new_string_2]  # if needed production doesn't exists, it's generated here
                            if child_counter == len(tree[root]):
                                new_string += "n" + str(counter)
                            else:
                                new_string += "n" + str(counter) + ","
                        else:
                            if child_counter == len(tree[root]):
                                new_string += c
                            else:
                                new_string += c + ","
                        child_counter += 1
                    new_string += ")"
                    normal_p[left_side].append(new_string)
            else:
                normal_p[left_side].append(right_side)
    for k in normal_p.keys():  # here the new Nonterminal list is generated
        if k not in normal_n:
            normal_n.append(k)
    if converting:
        print "Converting grammar to normal form ...\n"
    else:
        print "Grammar is in normal form.\n"
    return normal_n, normal_p


def run(in_string):
    arg_par = argparse.ArgumentParser(description='')

    arg_par.add_argument('-s', '--startsymbols', dest='starts', help='startsymbols', required=True)
    arg_par.add_argument('-p', '--productions', dest='prods', help='productions', required=True)
    argse = arg_par.parse_args()

    n, e, q, s, p = read(argse.starts, argse.prods)

    n_n, p_n = normal_form(n, p)

    t_a = TreeAutomaton(n_n, e, q, s, p_n)

    print "Input string:\n\t" + str(in_string)
    commands = parse_input(in_string)
    print "Tree string:\n\t" + str(commands[0])

    # This block checks if the input string is correctly formatted.
    if len(commands) > 1:
        print "To many arguments given."
        return

    tree, node_id = make_tree(parse_tree_string(commands[0]))
    parses = t_a.check(tree)

    accepted = False
    for x in parses:
        if write(x) == commands[0]:
            accepted = True
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
# treestring = "A(A(b,a),b)"
treestring = raw_input("Input string in defined format:\n")
run(treestring)

