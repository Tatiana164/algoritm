class TreeNode:
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children or []


def sum_numbers(root: TreeNode) -> int:
    def dfs(node, current):
        if node is None:
            return 0

        current = current * 10 + node.val

        if not node.children:
            return current

        total = 0
        for child in node.children:
            total += dfs(child, current)
        return total

    return dfs(root, 0)


#       1
#      / \
#     2   3
#         / \
#        1   2

tree = TreeNode(1, [
    TreeNode(2),
    TreeNode(3, [
        TreeNode(1),
        TreeNode(2)
    ])
])
print(sum_numbers(tree))  # → 275 (13 + 131 + 132)
