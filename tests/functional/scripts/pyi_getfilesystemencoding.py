#-----------------------------------------------------------------------------
# Copyright (c) 2005-2015, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


import sys


frozen_encoding = str(sys.getfilesystemencoding())


# For various OS is encoding different.
# On Windows it should be still mbcs.
if sys.platform.startswith('win'):
    encoding = 'mbcs'
# On Mac OS X the value should be still the same.
elif sys.platform.startswith('darwin'):
    encoding = 'utf-8'
# On Linux and other unixes it should be None.
# Please note that on Linux the value differs from the value
# in interactive shell.
else:
    if sys.version_info[0] < 3:
        encoding = 'None'
    else:
        # Python 3 reports encoding 'utf-8'.
        encoding = 'utf-8'


print('Encoding expected: ' + encoding)
print('Encoding current: ' + frozen_encoding)


if not frozen_encoding == encoding:
    raise SystemExit('Frozen encoding %s is not the same as unfrozen %s.' %
                     (frozen_encoding, encoding))
