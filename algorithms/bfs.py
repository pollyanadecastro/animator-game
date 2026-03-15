from collections import deque


def visit(node):
    if node.question:
        return node.question
    return node.answer


def bfs(root):

    if root is None:
        return []

    queue = deque([root])
    result = []

    while queue:

        node = queue.popleft()
        result.append(visit(node))

        if node.yes:
            queue.append(node.yes)

        if node.no:
            queue.append(node.no)

    return result
