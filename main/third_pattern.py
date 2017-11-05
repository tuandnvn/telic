'''
Created on Sep 8, 2014

@author: Tuan
'''
from nltk.tree import Tree

from main import subtrees, add_result
def match_third_pattern(tokens, syntactic_tree, dependency, coreference = []):
    """
    (VP
          (VBN used)
          (S (VP (TO to) (VP (VB relieve) (NP (NN pain))))))
    """
    result = []
    def find_pp(subtree):
        if (subtree.label() == 'VP' and subtree[0].label() == 'VBN'):
            return True
        return False
    syntactic_tree.index_tag = []
    for s in subtrees(syntactic_tree, find_pp):
        s_leaves = s[0].leaves()
        if 'used' in s_leaves:
            for leaf_index in xrange(len(s[0].leaves()),len(s.leaves())):
                pos_index = [s.leaf_treeposition(leaf_index)[:-1]]
                if s[pos_index].label()[0] == 'V':
                    telic_verb_candidate = s[pos_index][0]
                    tree_position_found = list(s.index_tag)
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
                                        if int(dep_head_index) == token_index + 1 and dep_type in ['dobj', 'agent', 'nsubjpass', 'nsubj']:
                                            is_found_arguments = True
                                            simple_dependant = str(tokens[int(dep[4]) - 1][3])
                                            add_result(result, ((simple_form_verb_candiate, token_index), (str(dep[0]), simple_dependant, int(dep[4]) - 1)), [])
                                    except ValueError:
                                        pass
                                if not is_found_arguments:
                                    add_result(result, ((simple_form_verb_candiate, token_index), ()), [])
    return result

def test():    
    tokens = [[u'adz', u'0', u'3', u'adz', u'NN', u'O'], [u'is', u'4', u'6', u'be', u'VBZ', u'O'], [u'an', u'7', u'9', u'a', u'DT', u'O'], [u'edge', u'10', u'14', u'edge', u'NN', u'O'], [u'tool', u'15', u'19', u'tool', u'NN', u'O'], [u'used', u'20', u'24', u'use', u'VBN', u'O'], [u'to', u'25', u'27', u'to', u'TO', u'O'], [u'cut', u'28', u'31', u'cut', u'VB', u'O'], [u'and', u'32', u'35', u'and', u'CC', u'O'], [u'shape', u'36', u'41', u'shape', u'VB', u'O'], [u'wood', u'42', u'46', u'wood', u'NN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN adz)) (VP (VBZ is) (NP (NP (DT an) (NN edge) (NN tool)) (VP (VBN used) (S (VP (TO to) (VP (VB cut) (CC and) (VB shape) (NP (NN wood))))))))))')
    dep = [[u'nsubj', u'tool', u'adz', u'5', u'1'], [u'cop', u'tool', u'is', u'5', u'2'], [u'det', u'tool', u'an', u'5', u'3'], [u'nn', u'tool', u'edge', u'5', u'4'], [u'root', u'ROOT', u'tool', u'0', u'5'], [u'partmod', u'tool', u'used', u'5', u'6'], [u'aux', u'cut', u'to', u'8', u'7'], [u'xcomp', u'used', u'cut', u'6', u'8'], [u'xcomp', u'used', u'shape', u'6', u'10'], [u'conj_and', u'cut', u'shape', u'8', u'10'], [u'dobj', u'cut', u'wood', u'8', u'11']]
    print tokens[0][0]
    print match_third_pattern(tokens, syntactic_tree, dep)
    
    tokens = [[u'barbell', u'0', u'7', u'barbell', u'NN', u'O'], [u'is', u'8', u'10', u'be', u'VBZ', u'O'], [u'a', u'11', u'12', u'a', u'DT', u'O'], [u'bar', u'13', u'16', u'bar', u'NN', u'O'], [u'to', u'17', u'19', u'to', u'TO', u'O'], [u'which', u'20', u'25', u'which', u'WDT', u'O'], [u'heavy', u'26', u'31', u'heavy', u'JJ', u'O'], [u'discs', u'32', u'37', u'disc', u'NNS', u'O'], [u'are', u'38', u'41', u'be', u'VBP', u'O'], [u'attached', u'42', u'50', u'attach', u'VBN', u'O'], [u'at', u'51', u'53', u'at', u'IN', u'O'], [u'each', u'54', u'58', u'each', u'DT', u'O'], [u'end', u'59', u'62', u'end', u'NN', u'O'], [u';', u'62', u'63', u';', u':', u'O'], [u'used', u'64', u'68', u'use', u'VBN', u'O'], [u'in', u'69', u'71', u'in', u'IN', u'O'], [u'weightlifting', u'72', u'85', u'weightlifting', u'NN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN barbell)) (VP (VBZ is) (NP (NP (DT a) (NN bar)) (SBAR (WHPP (TO to) (WHNP (WDT which))) (S (NP (JJ heavy) (NNS discs)) (VP (VBP are) (VP (VBN attached) (PP (IN at) (NP (NP (DT each) (NN end)) (: ;) (VP (VBN used) (PP (IN in) (NP (NN weightlifting))))))))))))))')
    dep = [[u'nsubj', u'bar', u'barbell', u'4', u'1'], [u'cop', u'bar', u'is', u'4', u'2'], [u'det', u'bar', u'a', u'4', u'3'], [u'root', u'ROOT', u'bar', u'0', u'4'], [u'prep_to', u'attached', u'bar', u'10', u'4'], [u'amod', u'discs', u'heavy', u'8', u'7'], [u'nsubjpass', u'attached', u'discs', u'10', u'8'], [u'auxpass', u'attached', u'are', u'10', u'9'], [u'rcmod', u'bar', u'attached', u'4', u'10'], [u'det', u'end', u'each', u'13', u'12'], [u'prep_at', u'attached', u'end', u'10', u'13'], [u'partmod', u'end', u'used', u'13', u'15'], [u'prep_in', u'used', u'weightlifting', u'15', u'17']]
    print tokens[0][0]
    print match_third_pattern(tokens, syntactic_tree, dep)
    
    tokens = [[u'analgesic', u'0', u'9', u'analgesic', u'JJ', u'O'], [u'is', u'10', u'12', u'be', u'VBZ', u'O'], [u'a', u'13', u'14', u'a', u'DT', u'O'], [u'medicine', u'15', u'23', u'medicine', u'NN', u'O'], [u'used', u'24', u'28', u'use', u'VBN', u'O'], [u'to', u'29', u'31', u'to', u'TO', u'O'], [u'relieve', u'32', u'39', u'relieve', u'VB', u'O'], [u'pain', u'40', u'44', u'pain', u'NN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (JJ analgesic)) (VP (VBZ is) (NP (NP (DT a) (NN medicine)) (VP (VBN used) (S (VP (TO to) (VP (VB relieve) (NP (NN pain))))))))))')
    dep = [[u'nsubj', u'medicine', u'analgesic', u'4', u'1'], [u'cop', u'medicine', u'is', u'4', u'2'], [u'det', u'medicine', u'a', u'4', u'3'], [u'root', u'ROOT', u'medicine', u'0', u'4'], [u'partmod', u'medicine', u'used', u'4', u'5'], [u'aux', u'relieve', u'to', u'7', u'6'], [u'xcomp', u'used', u'relieve', u'5', u'7'], [u'dobj', u'relieve', u'pain', u'7', u'8']]
    print tokens[0][0]
    print match_third_pattern(tokens, syntactic_tree, dep)