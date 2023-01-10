#!/usr/bin/env python

import os
import re
import sys
from iterfzf import iterfzf

conffiles = []
i = 1

CONF_PATH = os.path.join(os.getenv("HOME"), '.kube')
dst = os.path.join(CONF_PATH, 'config')

# Search for current symlink
try:
    current = os.readlink(dst)
except OSError as error:
    if error.errno == 22:
        print(
            "[ERROR] Current config file is not a symlink. Aborting to avoid current config loss.")
        sys.exit(1)
    if error.errno == 2:
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
    print("\n[INFO] Nothing changed. Your k8s config file is still %s Bye, bye !" % conffiles[0])
    sys.exit(0)

# Try to remove existing config file if exists
try:
    os.remove(dst)
except OSError:
    print("[WARN] Active config file was not found")

src = os.path.join(CONF_PATH, val)
os.symlink(src, dst)

print("[OK] Your k8s config file is now '%s'" % val)
