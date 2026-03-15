from collections import deque


def visit(node): 
    if node.question:
        return node.question
    return node.answer


def bfs(root):

    if root is None:
        return []

    queue = deque([(root, [])])
    results = []

    while queue:

        node, path = queue.popleft()

        new_path = path + [visit(node)]

        if node.is_leaf():
            results.append(" → ".join(new_path))

        else:
            if node.yes:
                queue.append((node.yes, new_path))

            if node.no:
                queue.append((node.no, new_path))

    
    return results
