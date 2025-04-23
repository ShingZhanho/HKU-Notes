# Created by Jacob Shing on 2025-04-23

# resolve-targets.py
# A script for resolving LaTeX build targets for GitHub Actions integration.
# Read build-targets.txt for syntax.

targets_tree = {}
targets_list = []

def main():
    global targets_tree

    # Read the build-targets.txt file
    file_lines: list[str] = []
    with open("build/build-targets.txt", "r") as file:
        for line in file:
            file_lines.append(line)
        file.close()
    # Remove comments and empty lines
    file_lines = [line.strip(' \n') for line in file_lines if not line.startswith("#") and line.strip(' \n\t') != ""]
    targets_tree = build_tree(file_lines)
    # Flatten the tree into a list
    targets_list = flatten_tree(targets_tree)

    output_str = "set-matrix=["
    for target in targets_list:
        output_str += f"\"{target}\","
    output_str = output_str[:-1] + "]"

    # print to stdout
    print(output_str)

def build_tree(lines) -> dict:
    tree = {}
    stack = [(-1, tree)]  # (indent_level, current_dict)
    for line in lines:
        # Skip comments and empty lines
        if line.strip() == "" or line.lstrip().startswith("#"):
            continue
        # Count leading tabs for indentation level
        indent = 0
        while line.startswith('\t' * (indent + 1)):
            indent += 1
        key = line.strip()
        # Remove from stack until we find the correct parent
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent_dict = stack[-1][1]
        # Merge if key exists, else create
        if key not in parent_dict:
            parent_dict[key] = {}
        stack.append((indent, parent_dict[key]))
    # Recursively convert empty dicts to None
    def clean(d):
        for k, v in d.items():
            if v == {}:
                d[k] = None
            else:
                clean(v)
    clean(tree)
    return tree

def flatten_tree(tree) -> list:
    result = []
    def dfs(node, path):
        for key, child in node.items():
            new_path = path + [key]
            if child is None:
                result.append("".join(new_path))
            else:
                dfs(child, new_path)
    dfs(tree, [])
    return result

if __name__ == "__main__":
    main()
