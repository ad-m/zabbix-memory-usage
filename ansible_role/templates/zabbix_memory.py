#!/usr/bin/python
import pwd
import sys
import json
import psutil
from collections import Counter


def struct_passwd_to_data(struct):
    return {'{#SYSTEMUSER_NAME}': struct.pw_name,
            '{#SYSTEMUSER_UID}': struct.pw_uid,
            '{#SYSTEMUSER_GID}': struct.pw_gid,
            '{#SYSTEMUSER_DIR}': struct.pw_dir}


def get_memory_stat():
    c = Counter()
    for x in psutil.process_iter():
        try:
            c[x.uids().real] += x.memory_info().rss
        except psutil.NoSuchProcess:
            pass
    return c


def discovery():
    stat = get_memory_stat()
    data = [struct_passwd_to_data(x) for x in pwd.getpwall() if x.pw_uid in stat]
    print(json.dumps({'data': data}, indent=4, sort_keys=True))


def memory_stats(uid):
    print(json.dumps(get_memory_stat()[uid], indent=4, sort_keys=True))


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("\t {0} discovery".format(sys.argv[0]))
        print("\t {0} memory_usage uid".format(sys.argv[0]))
    elif sys.argv[1] == 'discovery':
        discovery()
    elif sys.argv[1] == 'memory_usage':
        memory_stats(int(sys.argv[2]))


if __name__ == '__main__':
    main()
