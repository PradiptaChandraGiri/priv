import os

def get_tree(startpath, exclude_dirs):
    tree = ''
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree += f'{indent}{os.path.basename(root)}/\n'
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not f.endswith('.pyc'):
                tree += f'{subindent}{f}\n'
    return tree

print(get_tree('.', ['.git', 'node_modules', 'portfolio-react', '.vscode']))
