'''
Created on Sep 8, 2014

@author: Tuan
'''
from nltk.tree import Tree

from main import subtrees, add_result

def is_not_contain(candidate_tuple):
    simple_form_verb_candiate = candidate_tuple[0][0]
    if simple_form_verb_candiate in ['have', 'contain', 'include', ]:
        return False
    return True

def is_not_tobe(candidate_tuple):
    simple_form_verb_candiate = candidate_tuple[0][0]
    if simple_form_verb_candiate in ['be']:
        return False
    return True

def match_second_pattern(tokens, syntactic_tree, dependency, coreference=[]):
    """
    (SBAR
          (WHNP (WDT that))
          (S
            (VP
              (VP (VBZ has) (NP (NNS sleeves)))
              (CC and)
              (VP
                (VBZ covers)
                (NP (DT the) (NN body))
                (PP (IN from) (NP (NN shoulder)))
                (ADVP (RB down)))
    (SBAR
          (WHNP (WDT that))
          (S
            (VP
              (VBZ provides)
              (NP (NN privacy) (CC and) (NN protection))
              (PP (IN from) (NP (NN danger)))
    """
    result = []
    def find_pp(subtree):
        if (subtree.label() == 'SBAR'):
            return True
        return False
    syntactic_tree.index_tag = []
    for s in subtrees(syntactic_tree, find_pp):
        s_leaves = s[0].leaves()
        for rel_terms in ['that', 'where', 'which']:
            if rel_terms in s_leaves:
                for leaf_index in xrange(len(s.leaves())):
                    pos_index = [s.leaf_treeposition(leaf_index)[:-1]]
                    if s[pos_index].label()[0] == 'V' :
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
                                                add_result(result, ((simple_form_verb_candiate, token_index), (str(dep[0]), simple_dependant, int(dep[4]) - 1)), [is_not_contain, is_not_tobe])
                                        except ValueError:
                                            pass
                                    if not is_found_arguments:
                                        add_result(result, ((simple_form_verb_candiate, token_index), ()), [is_not_contain, is_not_tobe])
    return result

def test():
    tokens = [[u'shelter', u'0', u'7', u'shelter', u'NN', u'O'], [u'is', u'8', u'10', u'be', u'VBZ', u'O'], [u'a', u'11', u'12', u'a', u'DT', u'O'], [u'structure', u'13', u'22', u'structure', u'NN', u'O'], [u'that', u'23', u'27', u'that', u'WDT', u'O'], [u'provides', u'28', u'36', u'provide', u'VBZ', u'O'], [u'privacy', u'37', u'44', u'privacy', u'NN', u'O'], [u'and', u'45', u'48', u'and', u'CC', u'O'], [u'protection', u'49', u'59', u'protection', u'NN', u'O'], [u'from', u'60', u'64', u'from', u'IN', u'O'], [u'danger', u'65', u'71', u'danger', u'NN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN shelter)) (VP (VBZ is) (NP (NP (DT a) (NN structure)) (SBAR (WHNP (WDT that)) (S (VP (VBZ provides) (NP (NN privacy) (CC and) (NN protection)) (PP (IN from) (NP (NN danger))))))))))')
    dep = [[u'nsubj', u'structure', u'shelter', u'4', u'1'], [u'cop', u'structure', u'is', u'4', u'2'], [u'det', u'structure', u'a', u'4', u'3'], [u'root', u'ROOT', u'structure', u'0', u'4'], [u'nsubj', u'provides', u'structure', u'6', u'4'], [u'rcmod', u'structure', u'provides', u'4', u'6'], [u'dobj', u'provides', u'privacy', u'6', u'7'], [u'dobj', u'provides', u'protection', u'6', u'9'], [u'conj_and', u'privacy', u'protection', u'7', u'9'], [u'prep_from', u'provides', u'danger', u'6', u'11']]
    print tokens[0][0]
    print match_second_pattern(tokens, syntactic_tree, dep)
    
    tokens = [[u'coat', u'0', u'4', u'coat', u'NN', u'O'], [u'is', u'5', u'7', u'be', u'VBZ', u'O'], [u'an', u'8', u'10', u'a', u'DT', u'O'], [u'outer', u'11', u'16', u'outer', u'JJ', u'O'], [u'garment', u'17', u'24', u'garment', u'NN', u'O'], [u'that', u'25', u'29', u'that', u'WDT', u'O'], [u'has', u'30', u'33', u'have', u'VBZ', u'O'], [u'sleeves', u'34', u'41', u'sleeve', u'NNS', u'O'], [u'and', u'42', u'45', u'and', u'CC', u'O'], [u'covers', u'46', u'52', u'cover', u'VBZ', u'O'], [u'the', u'53', u'56', u'the', u'DT', u'O'], [u'body', u'57', u'61', u'body', u'NN', u'O'], [u'from', u'62', u'66', u'from', u'IN', u'O'], [u'shoulder', u'67', u'75', u'shoulder', u'NN', u'O'], [u'down', u'76', u'80', u'down', u'RB', u'O'], [u';', u'80', u'81', u';', u':', u'O'], [u'worn', u'82', u'86', u'wear', u'VBG', u'O'], [u'outdoors', u'87', u'95', u'outdoors', u'NNS', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN coat)) (VP (VBZ is) (NP (NP (DT an) (JJ outer) (NN garment)) (SBAR (WHNP (WDT that)) (S (VP (VP (VBZ has) (NP (NNS sleeves))) (CC and) (VP (VBZ covers) (NP (DT the) (NN body)) (PP (IN from) (NP (NN shoulder))) (ADVP (RB down)))))) (: ;) (S (VP (VBG worn) (NP (NNS outdoors))))))))')
    dep = [[u'nsubj', u'garment', u'coat', u'5', u'1'], [u'cop', u'garment', u'is', u'5', u'2'], [u'det', u'garment', u'an', u'5', u'3'], [u'amod', u'garment', u'outer', u'5', u'4'], [u'root', u'ROOT', u'garment', u'0', u'5'], [u'nsubj', u'has', u'garment', u'7', u'5'], [u'nsubj', u'covers', u'garment', u'10', u'5'], [u'rcmod', u'garment', u'has', u'5', u'7'], [u'dobj', u'has', u'sleeves', u'7', u'8'], [u'rcmod', u'garment', u'covers', u'5', u'10'], [u'conj_and', u'has', u'covers', u'7', u'10'], [u'det', u'body', u'the', u'12', u'11'], [u'dobj', u'covers', u'body', u'10', u'12'], [u'prep_from', u'covers', u'shoulder', u'10', u'14'], [u'advmod', u'covers', u'down', u'10', u'15'], [u'dep', u'garment', u'worn', u'5', u'17'], [u'dobj', u'worn', u'outdoors', u'17', u'18']]
    print tokens[0][0]
    print match_second_pattern(tokens, syntactic_tree, dep)
    
    tokens = [[u'aerosol', u'0', u'7', u'aerosol', u'NN', u'O'], [u'is', u'8', u'10', u'be', u'VBZ', u'O'], [u'a', u'11', u'12', u'a', u'DT', u'O'], [u'dispenser', u'13', u'22', u'dispenser', u'NN', u'O'], [u'that', u'23', u'27', u'that', u'WDT', u'O'], [u'holds', u'28', u'33', u'hold', u'VBZ', u'O'], [u'a', u'34', u'35', u'a', u'DT', u'O'], [u'substance', u'36', u'45', u'substance', u'NN', u'O'], [u'under', u'46', u'51', u'under', u'IN', u'O'], [u'pressure', u'52', u'60', u'pressure', u'NN', u'O'], [u'and', u'61', u'64', u'and', u'CC', u'O'], [u'that', u'65', u'69', u'that', u'IN', u'O'], [u'can', u'70', u'73', u'can', u'MD', u'O'], [u'release', u'74', u'81', u'release', u'VB', u'O'], [u'it', u'82', u'84', u'it', u'PRP', u'O'], [u'as', u'85', u'87', u'as', u'IN', u'O'], [u'a', u'88', u'89', u'a', u'DT', u'O'], [u'fine', u'90', u'94', u'fine', u'JJ', u'O'], [u'spray', u'95', u'100', u'spray', u'NN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN aerosol)) (VP (VBZ is) (NP (NP (DT a) (NN dispenser)) (SBAR (SBAR (WHNP (WDT that)) (S (VP (VBZ holds) (NP (DT a) (NN substance)) (PP (IN under) (NP (NN pressure)))))) (CC and) (SBAR (IN that) (S (VP (MD can) (VP (VB release) (NP (PRP it)) (PP (IN as) (NP (DT a) (JJ fine) (NN spray))))))))))))')
    dep = [[u'nsubj', u'dispenser', u'aerosol', u'4', u'1'], [u'cop', u'dispenser', u'is', u'4', u'2'], [u'det', u'dispenser', u'a', u'4', u'3'], [u'root', u'ROOT', u'dispenser', u'0', u'4'], [u'nsubj', u'holds', u'dispenser', u'6', u'4'], [u'nsubj', u'release', u'dispenser', u'14', u'4'], [u'rcmod', u'dispenser', u'holds', u'4', u'6'], [u'det', u'substance', u'a', u'8', u'7'], [u'dobj', u'holds', u'substance', u'6', u'8'], [u'prep_under', u'holds', u'pressure', u'6', u'10'], [u'mark', u'release', u'that', u'14', u'12'], [u'aux', u'release', u'can', u'14', u'13'], [u'rcmod', u'dispenser', u'release', u'4', u'14'], [u'conj_and', u'holds', u'release', u'6', u'14'], [u'dobj', u'release', u'it', u'14', u'15'], [u'det', u'spray', u'a', u'19', u'17'], [u'amod', u'spray', u'fine', u'19', u'18'], [u'prep_as', u'release', u'spray', u'14', u'19']]
    coref = [[[[u'it', 0, 4, 14, 15], [u'a substance', 0, 7, 6, 8]]]]
    print tokens[0][0]
    print match_second_pattern(tokens, syntactic_tree, dep, coref)
    
    tokens = [[u'wrestling_mat', u'0', u'13', u'wrestling_mat', u'NN', u'O'], [u'is', u'14', u'16', u'be', u'VBZ', u'O'], [u'a', u'17', u'18', u'a', u'DT', u'O'], [u'mat', u'19', u'22', u'mat', u'NN', u'O'], [u'on', u'23', u'25', u'on', u'IN', u'O'], [u'which', u'26', u'31', u'which', u'WDT', u'O'], [u'wrestling', u'32', u'41', u'wrestling', u'NN', u'O'], [u'matches', u'42', u'49', u'match', u'NNS', u'O'], [u'are', u'50', u'53', u'be', u'VBP', u'O'], [u'conducted', u'54', u'63', u'conduct', u'VBN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN wrestling_mat)) (VP (VBZ is) (NP (NP (DT a) (NN mat)) (SBAR (WHPP (IN on) (WHNP (WDT which) (NN wrestling))) (S (NP (NNS matches)) (VP (VBP are) (VP (VBN conducted)))))))))')
    dep = [[u'nsubj', u'mat', u'wrestling_mat', u'4', u'1'], [u'cop', u'mat', u'is', u'4', u'2'], [u'det', u'mat', u'a', u'4', u'3'], [u'root', u'ROOT', u'mat', u'0', u'4'], [u'det', u'wrestling', u'mat', u'7', u'4'], [u'prep_on', u'conducted', u'wrestling', u'10', u'7'], [u'nsubjpass', u'conducted', u'matches', u'10', u'8'], [u'auxpass', u'conducted', u'are', u'10', u'9'], [u'rcmod', u'mat', u'conducted', u'4', u'10']]
    print tokens[0][0]
    print match_second_pattern(tokens, syntactic_tree, dep)
    
    tokens = [[u'abutment', u'0', u'8', u'abutment', u'NN', u'O'], [u'is', u'9', u'11', u'be', u'VBZ', u'O'], [u'a', u'12', u'13', u'a', u'DT', u'O'], [u'masonry', u'14', u'21', u'masonry', u'NN', u'O'], [u'support', u'22', u'29', u'support', u'NN', u'O'], [u'that', u'30', u'34', u'that', u'WDT', u'O'], [u'touches', u'35', u'42', u'touch', u'NNS', u'O'], [u'and', u'43', u'46', u'and', u'CC', u'O'], [u'directly', u'47', u'55', u'directly', u'RB', u'O'], [u'receives', u'56', u'64', u'receive', u'VBZ', u'O'], [u'thrust', u'65', u'71', u'thrust', u'NN', u'O'], [u'or', u'72', u'74', u'or', u'CC', u'O'], [u'pressure', u'75', u'83', u'pressure', u'NN', u'O'], [u'of', u'84', u'86', u'of', u'IN', u'O'], [u'an', u'87', u'89', u'a', u'DT', u'O'], [u'arch', u'90', u'94', u'arch', u'NN', u'O'], [u'or', u'95', u'97', u'or', u'CC', u'O'], [u'bridge', u'98', u'104', u'bridge', u'NN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN abutment)) (VP (VBZ is) (NP (NP (DT a) (NN masonry) (NN support)) (SBAR (WHNP (WDT that)) (S (NP (NP (NNS touches)) (ADVP (CC and) (RB directly))) (VP (VBZ receives) (NP (NP (NN thrust) (CC or) (NN pressure)) (PP (IN of) (NP (DT an) (NN arch) (CC or) (NN bridge)))))))))))')
    dep = [[u'nsubj', u'support', u'abutment', u'5', u'1'], [u'cop', u'support', u'is', u'5', u'2'], [u'det', u'support', u'a', u'5', u'3'], [u'nn', u'support', u'masonry', u'5', u'4'], [u'root', u'ROOT', u'support', u'0', u'5'], [u'dobj', u'receives', u'support', u'10', u'5'], [u'nsubj', u'receives', u'touches', u'10', u'7'], [u'cc', u'directly', u'and', u'9', u'8'], [u'advmod', u'touches', u'directly', u'7', u'9'], [u'rcmod', u'support', u'receives', u'5', u'10'], [u'dobj', u'receives', u'thrust', u'10', u'11'], [u'dobj', u'receives', u'pressure', u'10', u'13'], [u'conj_or', u'thrust', u'pressure', u'11', u'13'], [u'det', u'arch', u'an', u'16', u'15'], [u'prep_of', u'thrust', u'arch', u'11', u'16'], [u'prep_of', u'thrust', u'bridge', u'11', u'18'], [u'conj_or', u'arch', u'bridge', u'16', u'18']]
    print tokens[0][0]
    print match_second_pattern(tokens, syntactic_tree, dep)
    
    tokens = [[u'abattoir', u'0', u'8', u'abattoir', u'NN', u'O'], [u'is', u'9', u'11', u'be', u'VBZ', u'O'], [u'a', u'12', u'13', u'a', u'DT', u'O'], [u'building', u'14', u'22', u'building', u'NN', u'O'], [u'where', u'23', u'28', u'where', u'WRB', u'O'], [u'animals', u'29', u'36', u'animal', u'NNS', u'O'], [u'are', u'37', u'40', u'be', u'VBP', u'O'], [u'butchered', u'41', u'50', u'butcher', u'VBN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN abattoir)) (VP (VBZ is) (NP (NP (DT a) (NN building)) (SBAR (WHNP (WHADVP (WRB where)) (NNS animals)) (S (VP (VBP are) (VP (VBN butchered)))))))))')
    dep = [[u'nsubj', u'building', u'abattoir', u'4', u'1'], [u'cop', u'building', u'is', u'4', u'2'], [u'det', u'building', u'a', u'4', u'3'], [u'root', u'ROOT', u'building', u'0', u'4'], [u'advmod', u'animals', u'where', u'6', u'5'], [u'nsubjpass', u'butchered', u'animals', u'8', u'6'], [u'auxpass', u'butchered', u'are', u'8', u'7'], [u'rcmod', u'building', u'butchered', u'4', u'8']]
    print tokens[0][0]
    print match_second_pattern(tokens, syntactic_tree, dep)
    
    tokens = [[u'hat', u'0', u'3', u'hat', u'NN', u'O'], [u'is', u'4', u'6', u'be', u'VBZ', u'O'], [u'headdress', u'7', u'16', u'headdress', u'NN', u'O'], [u'that', u'17', u'21', u'that', u'WDT', u'O'], [u'protects', u'22', u'30', u'protect', u'VBZ', u'O'], [u'the', u'31', u'34', u'the', u'DT', u'O'], [u'head', u'35', u'39', u'head', u'NN', u'O'], [u'from', u'40', u'44', u'from', u'IN', u'O'], [u'bad', u'45', u'48', u'bad', u'JJ', u'O'], [u'weather', u'49', u'56', u'weather', u'NN', u'O'], [u';', u'56', u'57', u';', u':', u'O'], [u'has', u'58', u'61', u'have', u'VBZ', u'O'], [u'shaped', u'62', u'68', u'shape', u'VBN', u'O'], [u'crown', u'69', u'74', u'crown', u'NN', u'O'], [u'and', u'75', u'78', u'and', u'CC', u'O'], [u'usually', u'79', u'86', u'usually', u'RB', u'O'], [u'a', u'87', u'88', u'a', u'DT', u'O'], [u'brim', u'89', u'93', u'brim', u'NN', u'O']]
    syntactic_tree = Tree.fromstring('(ROOT (S (NP (NN hat)) (VP (VBZ is) (NP (NP (NN headdress)) (SBAR (WHNP (WDT that)) (S (VP (VBZ protects) (S (NP (NP (DT the) (NN head)) (PP (IN from) (NP (JJ bad) (NN weather)))) (: ;) (VP (VBZ has) (VP (VBN shaped) (NP-TMP (NP (NN crown)) (CC and) (ADVP (RB usually)) (NP (DT a) (NN brim)))))))))))))')
    dep = [[u'nsubj', u'headdress', u'hat', u'3', u'1'], [u'cop', u'headdress', u'is', u'3', u'2'], [u'root', u'ROOT', u'headdress', u'0', u'3'], [u'nsubj', u'protects', u'headdress', u'5', u'3'], [u'rcmod', u'headdress', u'protects', u'3', u'5'], [u'det', u'head', u'the', u'7', u'6'], [u'nsubj', u'shaped', u'head', u'13', u'7'], [u'amod', u'weather', u'bad', u'10', u'9'], [u'prep_from', u'head', u'weather', u'7', u'10'], [u'aux', u'shaped', u'has', u'13', u'12'], [u'ccomp', u'protects', u'shaped', u'5', u'13'], [u'tmod', u'shaped', u'crown', u'13', u'14'], [u'tmod', u'shaped', u'usually', u'13', u'16'], [u'advmod', u'crown', u'usually', u'14', u'16'], [u'conj_and', u'crown', u'usually', u'14', u'16'], [u'det', u'brim', u'a', u'18', u'17'], [u'tmod', u'shaped', u'brim', u'13', u'18'], [u'conj_and', u'crown', u'brim', u'14', u'18']]
    print tokens[0][0]
    print match_second_pattern(tokens, syntactic_tree, dep)
    
# test()
