def visit(node):
    if node.question:
        return node.question
    return node.answer


def dfs(node, path=None):

    if node is None:
        return

    if path is None:
        path = []

    path.append(visit(node))

    dfs(node.yes, path)
    dfs(node.no, path)

    return path