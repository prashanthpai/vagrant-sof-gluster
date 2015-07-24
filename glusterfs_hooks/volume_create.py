#!/usr/bin/env python

from argparse import ArgumentParser
import ConfigParser
import string

from swift.common.storage_policy import POLICIES
from swift.common.utils import SWIFT_CONF_FILE

VALID_CHARS = '-' + string.letters + string.digits

parser = ArgumentParser(description="Add new volumes to swift.conf")
parser.add_argument("--volname")
args = parser.parse_args()
volname = args.volname

if not all(c in VALID_CHARS for c in volname):
    raise ValueError("Volume name does not conform to storage policy naming")

policy_exists = False
max_policy_idx = 0

for policy in POLICIES:
    if policy.name == volname and \
            policy.policy_type == 'replication':
        policy_exists = True
        break

for policy in POLICIES:
    if policy.idx > max_policy_idx:
        max_policy_idx = policy.idx

if not policy_exists:
    config = ConfigParser.RawConfigParser()
    config.read(SWIFT_CONF_FILE)
    section = "storage-policy:" + str(max_policy_idx + 1)
    config.add_section(section)
    config.set(section, 'name', volname)
    config.set(section, 'policy_type', 'replication')
    with open(SWIFT_CONF_FILE, 'wb') as configfile:
        config.write(configfile)
