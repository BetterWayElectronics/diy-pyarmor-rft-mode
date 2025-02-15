#!/usr/bin/env python3

import ast
import astunparse  # or use ast.unparse if needed?
import random
import string
import builtins
import base64
import os
import sys
import re

##############################################################################
# FANCY COLOURS
##############################################################################

def print_banner() -> str:
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=130))
    banner = r"""
__________          ___________
\______   \___  _  _\_   _____/
 |    |  _/\  \/ \/ /|   __)_ 
 |    |   \ \      //        \
 |______  /  \_/\_//_______  /
    DIY \/Pyarmor RFT Mode \/ v1.0.2
"""
    os.system("")
    faded_banner = ""
    colors = [
        (85, 0, 145),   # Dark purple
        (99, 43, 153),  # Intermediate colour 1
        (122, 87, 176), # Intermediate colour 2
        (146, 130, 199),# Intermediate colour 3
        (169, 173, 222),# Intermediate colour 4
        (173, 216, 230),# Intermediate colour 5
        (173, 216, 230) # Light blue
    ]
    color_index = 0

    for line in banner.splitlines():
        r, g, b = colors[color_index]
        faded_banner += (f"\033[38;2;{r};{g};{b}m{line}\033[0m\n")
        color_index = (color_index + 1) % len(colors)
    return faded_banner

def gradient_text(text: str, colors: list) -> str:
    os.system("")
    gradient = ""
    color_index = 0
    for char in text:
        if char != " ":
            r, g, b = colors[color_index]
            gradient += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
            color_index = (color_index + 1) % len(colors)
        else:
            gradient += char
    return gradient

##############################################################################
# LOGIC CONFIG
##############################################################################

ALL_BUILTINS = set(dir(builtins))
EXCLUDE_NAMES = []  # Populate via user input
ALIAS_PREFIX = "BwE_"  # Override via user input

def random_alias(prefix=None, length=5):
    """
    Generate or reuse a random alias, e.g. BwE_12345.
    Allows 'prefix' to be changed by user input.
    """
    if prefix is None:
        prefix = ALIAS_PREFIX
    digits = string.digits
    suffix = ''.join(random.choices(digits, k=length))
    return prefix + suffix

def starts_with_double_underscore(name: str) -> bool:
    return name.startswith("__")

##############################################################################
# UNIVERSAL RENAMER CLASS
##############################################################################

class UniversalRenamer(ast.NodeTransformer):
    """
    Renames:
      - function names, class names, global/local vars, import aliases, builtin references
    Skips:
      - function arguments in definitions (parameters)
      - keyword argument names in calls
      - names that start with '__'
      - strings in __all__
      - any item in EXCLUDE_NAMES
    Records rename events in `self.changes`.
    """
    def __init__(self):
        super().__init__()
        self.trace_log = {}    # old_name -> new_name
        self.changes = []      # (lineno, old_name, new_name)
        self.skip_all_strings = set()  # e.g. from __all__
        self.func_params_stack = []  # Holds parameter names for current function scope

    def _get_new_name(self, old_name, lineno=None):
        # Generate or reuse a random alias, unless excluded or starts with __
        if starts_with_double_underscore(old_name):
            return old_name
        if old_name in EXCLUDE_NAMES:
            return old_name

        if old_name not in self.trace_log:
            new_alias = random_alias()  # uses global ALIAS_PREFIX
            self.trace_log[old_name] = new_alias
            if lineno is not None:
                self.changes.append((lineno, old_name, new_alias))
        else:
            new_alias = self.trace_log[old_name]
            if lineno is not None:
                self.changes.append((lineno, old_name, new_alias))
        return self.trace_log[old_name]
        
    def visit_Global(self, node: ast.Global):
        # Rename each global name in the global statement.
        new_names = []
        for name in node.names:
            if starts_with_double_underscore(name) or name in EXCLUDE_NAMES:
                new_names.append(name)
            else:
                new_names.append(self._get_new_name(name))
        node.names = new_names
        return node

    def visit_Assign(self, node: ast.Assign):
       # If we see __all__ = ["foo", "bar"], record those strings so we skip renaming them.
        if (len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "__all__"
            and isinstance(node.value, ast.List)):
            for elt in node.value.elts:
                if isinstance(elt, ast.Str):
                    self.skip_all_strings.add(elt.s)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_name = node.name
        if not starts_with_double_underscore(old_name) and old_name not in EXCLUDE_NAMES:
            new_name = self._get_new_name(old_name, node.lineno)
            node.name = new_name

        # Extract parameter names and push onto the stack so they are not renamed inside the body.
        param_names = set()
        if node.args:
            for arg in node.args.args:
                param_names.add(arg.arg)
            if node.args.vararg:
                param_names.add(node.args.vararg.arg)
            for arg in node.args.kwonlyargs:
                param_names.add(arg.arg)
            if node.args.kwarg:
                param_names.add(node.args.kwarg.arg)
        self.func_params_stack.append(param_names)

        old_args = node.args
        node.args = None  # temporarily remove so generic_visit won't traverse them
        self.generic_visit(node)
        node.args = old_args
        self.func_params_stack.pop()
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        old_name = node.name
        if not starts_with_double_underscore(old_name) and old_name not in EXCLUDE_NAMES:
            new_name = self._get_new_name(old_name, node.lineno)
            node.name = new_name

        param_names = set()
        if node.args:
            for arg in node.args.args:
                param_names.add(arg.arg)
            if node.args.vararg:
                param_names.add(node.args.vararg.arg)
            for arg in node.args.kwonlyargs:
                param_names.add(arg.arg)
            if node.args.kwarg:
                param_names.add(node.args.kwarg.arg)
        self.func_params_stack.append(param_names)

        old_args = node.args
        node.args = None
        self.generic_visit(node)
        node.args = old_args
        self.func_params_stack.pop()
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        old_name = node.name
        if not starts_with_double_underscore(old_name) and old_name not in EXCLUDE_NAMES:
            new_name = self._get_new_name(old_name, node.lineno)
            node.name = new_name
        self.generic_visit(node)
        return node

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            old_name = alias.asname if alias.asname else alias.name
            if starts_with_double_underscore(old_name) or (old_name in EXCLUDE_NAMES):
                continue
            alias.asname = self._get_new_name(old_name, node.lineno)
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            old_name = alias.asname if alias.asname else alias.name
            if starts_with_double_underscore(old_name) or (old_name in EXCLUDE_NAMES):
                continue
            alias.asname = self._get_new_name(old_name, node.lineno)
        return node

    def visit_Name(self, node: ast.Name):
        old_id = node.id
        # If this name is a parameter in the current function scope, skip renaming.
        if self.func_params_stack and old_id in self.func_params_stack[-1]:
            return node
        if starts_with_double_underscore(old_id):
            return node
        if old_id in EXCLUDE_NAMES:
            return node
        if old_id in self.skip_all_strings:
            return node

        if isinstance(node.ctx, (ast.Store, ast.Del)):
            node.id = self._get_new_name(old_id, node.lineno)
        elif isinstance(node.ctx, ast.Load):
            if old_id in self.trace_log:
                node.id = self._get_new_name(old_id, node.lineno)
            else:
                if old_id in ALL_BUILTINS:
                    node.id = self._get_new_name(old_id, node.lineno)
        return node

    def visit_Call(self, node: ast.Call):
        self.visit(node.func)
        for kw in node.keywords:
            self.visit(kw.value)
        for arg in node.args:
            self.visit(arg)
        return node

    def visit_ListComp(self, node: ast.ListComp):
        for gen in node.generators:
            self.visit(gen)
        self.visit(node.elt)
        return node

    def visit_SetComp(self, node: ast.SetComp):
        for gen in node.generators:
            self.visit(gen)
        self.visit(node.elt)
        return node

    def visit_DictComp(self, node: ast.DictComp):
        for gen in node.generators:
            self.visit(gen)
        self.visit(node.key)
        self.visit(node.value)
        return node

    def visit_GeneratorExp(self, node: ast.GeneratorExp):
        for gen in node.generators:
            self.visit(gen)
        self.visit(node.elt)
        return node

def rename_everything(code: str):
    tree = ast.parse(code)
    transformer = UniversalRenamer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)
    new_code = astunparse.unparse(new_tree)
    return new_code, transformer.trace_log, transformer.changes

def insert_builtin_definitions(source: str, trace_log: dict) -> str:
    import_lines = ["import base64\n", "import builtins\n"]
    definitions = []

    for old_name, new_name in trace_log.items():
        if starts_with_double_underscore(old_name):
            continue
        if old_name in EXCLUDE_NAMES:
            continue
        if old_name in ALL_BUILTINS:
            encoded = base64.b64encode(old_name.encode()).decode()
            definitions.append(
                f"{new_name} = getattr(builtins, base64.b64decode(\"{encoded}\").decode())\n"
            )

    if not definitions:
        return source

    lines = source.splitlines(True)
    insert_idx = 1 if (lines and lines[0].startswith("#!")) else 0
    lines[insert_idx:insert_idx] = import_lines + definitions
    return "".join(lines)

def write_changes_log(changes_list, log_filename="trace_log.log"):
    changes_sorted = sorted(changes_list, key=lambda x: x[0])
    with open(log_filename, "w", encoding="utf-8") as f:
        for (lineno, old_name, new_name) in changes_sorted:
            f.write(f"Line {lineno}: {old_name} -> {new_name}\n")
    print(f"RFT Log Saved: '{log_filename}'")

def choose_py_file():
    py_files = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]
    if not py_files:
        print("\nNo .Py Files Found In Current Directory.")
        return None

    print("\nSelect A Python File To Transform:")
    for i, fname in enumerate(py_files, start=1):
        print(f"{i}. {fname}")

    while True:
        choice = input(f"\nEnter The Number [1-{len(py_files)}]: ")
        if not choice.isdigit():
            print("\nPlease Enter A Valid Number.")
            continue
        idx = int(choice)
        if 1 <= idx <= len(py_files):
            return py_files[idx-1]
        else:
            print("\nChoice Out Of Range. Try Again.")

def fix_fstring_escapes(code_str: str) -> str:
    # First, fix colon-backslash preceding a closing quote.
    code_str = re.sub(r'(:\\)(?=\')', r':\\\\', code_str)
    # Next, fix any backslash preceding a {.
    code_str = re.sub(r'\\(?=\{)', r'\\\\', code_str)
    # Finally, fix any single backslash preceding a letter (not one of valid escapes) with double backslash.
    code_str = re.sub(r'(?<!\\)\\(?!\\|\'|\"|n|r|t|b|f|v|a)([A-Za-z])', r'\\\\\1', code_str)
    return code_str

def main():
    os.system("cls" if os.name == "nt" else "clear")
    from sys import stdout
    stdout.write(print_banner())

    infile = choose_py_file()
    if not infile:
        return

    alias_input = input("Enter Alias Prefix (Press Enter For Default 'BwE_'): ")
    if alias_input.strip():
        global ALIAS_PREFIX
        ALIAS_PREFIX = alias_input.strip() + "_"

    exclude_input = input("Enter Names To Exclude, Comma-Separated (Or Press Enter For None): ")
    if exclude_input.strip():
        names = [n.strip() for n in exclude_input.split(",")]
        global EXCLUDE_NAMES
        EXCLUDE_NAMES = names
    else:
        EXCLUDE_NAMES.clear()

    base, ext = os.path.splitext(infile)
    outfile = base + "_rft.py"
    log_file = f"{base}_tracelog.log"

    with open(infile, "r", encoding="utf-8") as f:
        code = f.read()

    new_code, trace_log, changes = rename_everything(code)
    final_code = insert_builtin_definitions(new_code, trace_log)
    final_code = fix_fstring_escapes(final_code)

    with open(outfile, "w", encoding="utf-8") as out:
        out.write(final_code)

    colors = [
        (179, 183, 242),
        (183, 226, 240),
        (183, 226, 240)
    ]
    
    print(gradient_text(f"\nTransformed '{infile}' -> '{outfile}'", colors))
    write_changes_log(changes, log_file)

if __name__ == "__main__":
    main()
