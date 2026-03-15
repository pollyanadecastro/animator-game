def visit(node):
    if node.question:
        return node.question
    return node.answer


def dfs(node, path=None, results=None):

    if node is None:
        return []

    if path is None:
        path = []

    if results is None:
        results = []

    path = path + [visit(node)]

    if node.is_leaf():
        results.append(" → ".join(path))
    else:
        dfs(node.yes, path, results)
        dfs(node.no, path, results)


    return results
