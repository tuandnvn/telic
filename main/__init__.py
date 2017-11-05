from nltk.tree import Tree

def subtrees(tree, filter=None): 
    if not filter or filter(tree): 
        yield tree 
    for index in xrange(len(tree)):
        child = tree[index]
        if isinstance(child, Tree): 
            child.index_tag = tree.index_tag + [index] 
            for subtree in subtrees(child, filter): 
                yield subtree
                
def add_result(result, candidate_tuple, funcs):
    for func in funcs:
        if not func(candidate_tuple):
            return
    result.append(candidate_tuple)