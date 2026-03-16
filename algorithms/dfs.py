def visit(node):
    if node.question:
        return node.question
    return node.answer


def dfs(node, path=None):

    if node is None:
        return []

    if path is None:
        path = []

    path = path + [visit(node)]

    if node.answer:
        return [" → ".join(path)]

    result = []

    result += dfs(node.yes, path)
    result += dfs(node.no, path)

    return result
