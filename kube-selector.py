#!/usr/bin/env python

import errno
import os
import re
import sys
import tempfile
from iterfzf import iterfzf

conffiles = []
i = 1

CONF_PATH = os.path.join(os.getenv("HOME"), '.kube')
dst = os.path.join(CONF_PATH, 'config')

# Search for current symlink
try:
    current = os.readlink(dst)
except OSError as error:
    if error.errno == errno.EINVAL:
        print(
            "[ERROR] Current config file is not a symlink. Aborting to avoid current config loss.")
        sys.exit(1)
    if error.errno == errno.ENOENT:
        print("[WARN] Active config file not found")
        current = None

for conffile in os.listdir(CONF_PATH):
    if re.match('^config-', conffile):
        conffiles.append(conffile)

conffiles.sort()

# Put current config file in first place
for conffile in conffiles:
    if os.path.join(CONF_PATH, conffile) == current:
        conffiles.remove(conffile)
        conffiles.insert(0, conffile)

try:
    choice = iterfzf(conffiles)
    if choice == None:
        raise KeyboardInterrupt()
    else:
        val = choice
except KeyboardInterrupt:
    current_display = conffiles[0] if conffiles else "unknown"
    print("\n[INFO] Nothing changed. Your k8s config file is still %s Bye, bye !" % current_display)
    sys.exit(0)

src = os.path.join(CONF_PATH, val)
tmp = tempfile.mktemp(dir=CONF_PATH)
os.symlink(src, tmp)
os.replace(tmp, dst)

print("[OK] Your k8s config file is now '%s'" % val)
