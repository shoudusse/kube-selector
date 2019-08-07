#!/usr/bin/env python

import os
import re
import sys

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
            "[ERROR] Current config file is not a symlink. Aborting to avoid current config lost.")
        sys.exit(1)
    if error.errno == 2:
        print("[WARN] Active config file was not found")
        current = None

for conffile in os.listdir(CONF_PATH):
    if re.match('^config-', conffile):
        conffiles.append(conffile)
        if os.path.join(CONF_PATH, conffile) == current:
            indice = "> %i" % i
        else:
            indice = "  %i" % i
        print("%s: %s" % (indice, conffile))
        i = i + 1

try:
    val = int(input("Selection: "))
except KeyboardInterrupt:
    print("\n[INFO] Nothing changed. Bye, bye !")
    sys.exit(0)

# Try to remove existing config file if exists
try:
    os.remove(dst)
except OSError:
    print("[WARN] Active config file was not found")

src = os.path.join(CONF_PATH, conffiles[val - 1])
os.symlink(src, dst)

print("[OK] Your k8s config file is now '%s'" % conffiles[val - 1])
