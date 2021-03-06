#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


from modulegraph.modulegraph import RuntimeModule
from PyInstaller.utils.hooks import hookutils

def hook(module_graph):
    """
    Add the `six.moves` module as a dynamically defined runtime module node and
    all modules mapped by `six._SixMetaPathImporter` as aliased module nodes to
    the passed graph.

    This function adds a placeholder node for the dynamically defined
    `six.moves` module. This adds a reference from that module to its parent
    `six` module, ensuring that the latter will be frozen into this executable.

    `six._SixMetaPathImporter` is a PEP 302-compliant module importer converting
    imports independent of the current Python version into imports specific to
    that version (e.g., under Python 3, from `from six.moves import tkinter_tix`
    to `import tkinter.tix`). For each such mapping, this hook adds a
    corresponding module alias to the current graph.
    """
    # Dictionary from conventional module names to "six.moves" attribute names
    # (e.g., from `tkinter.tix` to `six.moves.tkinter_tix`).
    real_to_six_module_name = hookutils.eval_statement(
'''
import six
print('{')

# Iterate over the "six._moved_attributes" list rather than the
# "six._importer.known_modules" dictionary, as "urllib"-specific moved modules
# are overwritten in the latter with unhelpful "LazyModule" objects.
for moved_module in six._moved_attributes:
    # If this is a moved attribute rather than module, skip to the next object.
    if not isinstance(moved_module, six.MovedModule):
        continue

    print('  %s: %s,' % (
        repr(moved_module.mod), repr('six.moves.' + moved_module.name)))

print('}')
''')

    module_graph.add_module(RuntimeModule('six.moves'))
    for real_module_name, six_module_name in real_to_six_module_name.items():
        module_graph.alias_module(real_module_name, six_module_name)
