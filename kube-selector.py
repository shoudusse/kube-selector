#!/usr/bin/env python

import os
import re

conffiles = []
i = 1

CONF_PATH = os.path.join(os.getenv("HOME"),'.kube')

for conffile in os.listdir(CONF_PATH):
    if re.match('^config-', conffile):
        conffiles.append(conffile)
        print("%i: %s" % (i, conffile))
        i = i + 1

val = int(input("Selection: "))

# Try to remove existing config file if exists
try:
    os.remove(os.path.join(CONF_PATH, 'config'))
except os.error as error:
    print("[WARN] active config file was not found")

src = os.path.join(CONF_PATH, conffiles[val - 1])
dst = os.path.join(CONF_PATH, 'config')
os.symlink(src, dst)

print("[OK] Your k8s config file is now %s" % conffiles[val - 1])
