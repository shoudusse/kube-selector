#!/usr/bin/env python
# pylint: disable=invalid-name
"""Interactively select a kubectl config file and symlink it as the active config."""

import errno
import os
import re
import sys
import tempfile
from iterfzf import iterfzf

CONF_PATH = os.path.join(os.getenv("HOME"), '.kube')
DST = os.path.join(CONF_PATH, 'config')
conffiles = []

CURRENT = None
try:
    CURRENT = os.readlink(DST)
except OSError as error:
    if error.errno == errno.EINVAL:
        print(
            "[ERROR] Current config file is not a symlink. Aborting to avoid current config loss.")
        sys.exit(1)
    if error.errno == errno.ENOENT:
        print("[WARN] Active config file not found")

for conffile in os.listdir(CONF_PATH):
    if re.match('^config-', conffile):
        conffiles.append(conffile)

conffiles.sort()

for conffile in list(conffiles):
    if os.path.join(CONF_PATH, conffile) == CURRENT:
        conffiles.remove(conffile)
        conffiles.insert(0, conffile)

try:
    choice = iterfzf(conffiles)
    if choice is None:
        raise KeyboardInterrupt()
    val = choice
except KeyboardInterrupt:
    CURRENT_DISPLAY = conffiles[0] if conffiles else "unknown"
    print(f"\n[INFO] Nothing changed. Your k8s config file is still {CURRENT_DISPLAY} Bye, bye !")
    sys.exit(0)

src = os.path.join(CONF_PATH, val)
tmp = tempfile.mktemp(dir=CONF_PATH)
os.symlink(src, tmp)
os.replace(tmp, DST)

print(f"[OK] Your k8s config file is now '{val}'")
