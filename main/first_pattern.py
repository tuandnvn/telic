'''
Created on Sep 8, 2014

@author: Tuan
'''
from nltk.tree import Tree
from main import subtrees

def match_first_pattern(tokens, syntactic_tree, dependency, coreference = []):
    """
    for one sentence
    for V-ing or S or to-V
    (PP (IN for) (S (VP (VBG taking) (NP (NNS photographs)))))
    (PP (IN for) (NP (NP (DT an) (NN undertaking)) (CC or) (S (VP (TO to) (VP (VB perform) (NP (DT a) (NN service)))))))
    """
    result = []
    def find_pp(subtree):
        if (subtree.label() == 'PP' and subtree[0].label() == 'IN'):
            return True
        return False
    syntactic_tree.index_tag = []
    for s in subtrees(syntactic_tree, find_pp):
        s_leaves = s[0].leaves()
        if len(s_leaves) == 1 and s_leaves[0] == 'for':
            for leaf_index in xrange(len(s.leaves())):
                pos_index = [s.leaf_treeposition(leaf_index)[:-1]]
                if s[pos_index].label()[0] == 'V':
                    telic_verb_candidate = s[pos_index][0]
                    tree_position_found = s.index_tag
                    for i in s.leaf_treeposition(leaf_index):
                        tree_position_found.append(i)
                   
                    for token_index in xrange(len(tokens)):
                        token = tokens[token_index]
                        if token[0] == telic_verb_candidate:
                            simple_form_verb_candiate = str(token[3])
                            if syntactic_tree.leaf_treeposition(token_index) == tuple(tree_position_found):
                                is_found_arguments = False
                                for dep in dependency:
                                    dep_type = dep[0]
                                    dep_head_index = dep[3]
                                    try:
                                        if int(dep_head_index) == token_index + 1 and dep_type in ['dobj', 'nsubj', 'agent', 'prep_in', 'prep_on']:
                                            is_found_arguments = True
                                            simple_dependant =  str(tokens[int(dep[4])-1][3])
                                            result.append(((simple_form_verb_candiate, token_index), (str(dep[0]), simple_dependant, int(dep[4])-1 )))
                                    except ValueError:
                                        pass
                                if not is_found_arguments:
                                    result.append(((simple_form_verb_candiate, token_index), ()))
    return result

def test():
    tokens = [["equipment", "0", "9", "equipment", "NN", "O"], ["is", "10", "12", "be", "VBZ", "O"], ["an", "13", "15", "a", "DT", "O"], ["instrumentality", "16", "31", "instrumentality", "NN", "O"], ["needed", "32", "38", "need", "VBN", "O"], ["for", "39", "42", "for", "IN", "O"], ["an", "43", "45", "a", "DT", "O"], ["undertaking", "46", "57", "undertaking", "NN", "O"], ["or", "58", "60", "or", "CC", "O"], ["to", "61", "63", "to", "TO", "O"], ["perform", "64", "71", "perform", "VB", "O"], ["a", "72", "73", "a", "DT", "O"], ["service", "74", "81", "service", "NN", "O"]]
    syntactic_tree = Tree.fromstring("(ROOT (S (NP (NN equipment)) (VP (VBZ is) (NP (NP (DT an) (NN instrumentality)) (VP (VBN needed) (PP (IN for) (NP (NP (DT an) (NN undertaking)) (CC or) (S (VP (TO to) (VP (VB perform) (NP (DT a) (NN service))))))))))))")
    dep = [["nsubj", "instrumentality", "equipment", "4", "1"], ["cop", "instrumentality", "is", "4", "2"], ["det", "instrumentality", "an", "4", "3"], ["root", "ROOT", "instrumentality", "0", "4"], ["partmod", "instrumentality", "needed", "4", "5"], ["det", "undertaking", "an", "8", "7"], ["prep_for", "needed", "undertaking", "5", "8"], ["aux", "perform", "to", "11", "10"], ["prep_for", "needed", "perform", "5", "11"], ["conj_or", "undertaking", "perform", "8", "11"], ["infmod", "undertaking", "perform", "8", "11"], ["det", "service", "a", "13", "12"], ["dobj", "perform", "service", "11", "13"]]
    print tokens[0][0]
    print match_first_pattern(tokens, syntactic_tree, dep)
    
    tokens = [['plant', u'0', u'5', u'plant', u'NN', u'O'], [u'is', u'6', u'8', u'be', u'VBZ', u'O'], [u'buildings', u'9', u'18', u'building', u'NNS', u'O'], [u'for', u'19', u'22', u'for', u'IN', u'O'], [u'carrying', u'23', u'31', u'carry', u'VBG', u'O'], [u'on', u'32', u'34', u'on', u'IN', u'O'], [u'industrial', u'35', u'45', u'industrial', u'JJ', u'O'], [u'labor', u'46', u'51', u'labor', u'NN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN plant)) (VP (VBZ is) (NP (NP (NNS buildings)) (PP (IN for) (S (VP (VBG carrying) (PP (IN on) (NP (JJ industrial) (NN labor))))))))))')
    dep = [[u'nsubj', u'buildings', u'plant', u'3', u'1'], [u'cop', u'buildings', u'is', u'3', u'2'], [u'root', u'ROOT', u'buildings', u'0', u'3'], [u'prepc_for', u'buildings', u'carrying', u'3', u'5'], [u'amod', u'labor', u'industrial', u'8', u'7'], [u'prep_on', u'carrying', u'labor', u'5', u'8']]
    print tokens[0][0]
    print match_first_pattern(tokens, syntactic_tree, dep)
    
    tokens = [['camera', u'0', u'6', u'camera', u'NN', u'O'], [u'is', u'7', u'9', u'be', u'VBZ', u'O'], [u'equipment', u'10', u'19', u'equipment', u'NN', u'O'], [u'for', u'20', u'23', u'for', u'IN', u'O'], [u'taking', u'24', u'30', u'take', u'VBG', u'O'], [u'photographs', u'31', u'42', u'photograph', u'NNS', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN camera)) (VP (VBZ is) (NP (NP (NN equipment)) (PP (IN for) (S (VP (VBG taking) (NP (NNS photographs)))))))))')
    dep = [[u'nsubj', u'equipment', u'camera', u'3', u'1'], [u'cop', u'equipment', u'is', u'3', u'2'], [u'root', u'ROOT', u'equipment', u'0', u'3'], [u'prepc_for', u'equipment', u'taking', u'3', u'5'], [u'dobj', u'taking', u'photographs', u'5', u'6']]
    print tokens[0][0]
    print match_first_pattern(tokens, syntactic_tree, dep)