from collections import deque

def bfs(root):
    if root is None:
        return
    queue = deque([(root, [])])
    while queue:
        node, path = queue.popleft()
        path = path + [node.question or node.answer]
        if node.is_leaf():
            print(" → ".join(filter(None, path)))
        if node.yes:
            queue.append((node.yes, path))
        if node.no:
            queue.append((node.no, path))
