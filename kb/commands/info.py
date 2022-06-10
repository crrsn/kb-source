# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb show info command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""
from typing import Dict
import kb.db as db
import kb.initializer as initializer
import kb.history as history
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET, BROWN, RED
import os
import time
from datetime import datetime


def info(args: Dict[str, str], config: Dict[str, str]):
    """
    Search artifacts within the knowledge base of kb and sorted by category.

    Arguments:
    args:           - a dictionary containing the following fields:
                      query -> filter for the title field of the artifact
                      category -> filter for the category field of the artifact
                      tags -> filter for the tags field of the artifact
                      author -> filter for the author field of the artifact
                      status -> filter for the status field of the artifact
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB_DB        - the database path of KB
                      PATH_KB_DATA      - the data directory of KB
                      PATH_KB_HIST      - the history menu path of KB
                      EDITOR            - the editor program to call
    """
    # Check initialization
    initializer.init(config)

    # print(config)
    # {'PATH_KB': '/home/leo/.local/share/kb', 'PATH_KB_DB': '/home/leo/.local/share/kb/kb.db',
    # 'PATH_KB_HIST': '/home/leo/.local/share/kb/recent.hist', 'PATH_KB_DATA': '/home/leo/.local/share/kb/data',
    # 'PATH_KB_GIT': '/home/leo/.local/share/kb/.git', 'PATH_KB_CONFIG': '/home/leo/.local/share/kb/kb.conf.py',
    # 'PATH_KB_TEMPLATES': '/home/leo/.local/share/kb/templates',
    # 'PATH_KB_DEFAULT_TEMPLATE': '/home/leo/.local/share/kb/templates/default',
    # 'PATH_KB_MARKDOWN_TEMPLATE': '/home/leo/.local/share/kb/templates/markdown', 'DB_SCHEMA_VERSION': 1,
    # 'EDITOR': 'vim', 'INITIAL_CATEGORIES': ['default']}

    if args["show_path"]:
        print(BROWN + "\nPath of KB folder: " + RESET + config["PATH_KB"])
        print(BROWN + "Path of KB Database File: " + RESET + config["PATH_KB_DB"])
        print(BROWN + "Show All Configurations:" + RESET)
        print(config)
        print()
    else:
        conn = db.create_connection(config["PATH_KB_DB"])
        rows = db.get_artifacts_by_filter(
            conn,
            title="",
            category=None,
            tags=None,
            status=None,
            author=None)

        # rows.sort(key=lambda x: x[1])
        artifacts = sorted(rows, key=lambda x: x.category)
        # --------------------------------------------------------------
        print("\n" + UND + "KB Database Path         " + RESET)
        print(BROWN + config["PATH_KB"] + RESET)
        # --------------------------------------------------------------
        print("\n" + UND + "Database Information                              " + RESET)
        print(BROWN + "Total Number of artifacts: " + str(len(artifacts)) + RESET)
        print(" Size: {:.2f} MB (only data folder)".format(get_dir_size(config["PATH_KB_DATA"]) / 1024 / 1024))
        print(" Size: {:.2f} MB (with git)".format(get_dir_size(config["PATH_KB"]) / 1024 / 1024))

        fileTypeCountDict = dict()
        categoryListDict = dict()
        totalCategory = 0
        totalExtension = 0

        for artifact in artifacts:
            filename, file_extension = os.path.splitext(artifact.title)
            file_extension = file_extension.replace('.', '')
            # if file without extension, that is txt
            if file_extension == '':
                file_extension = 'txt'
            if file_extension not in fileTypeCountDict:
                # new extension, create a key/value for it
                fileTypeCountDict[file_extension] = 1
                totalExtension += 1
            else:
                # exist extension, value+1
                fileTypeCountDict[file_extension] += 1

            # analysis the category
            if artifact.category not in categoryListDict:
                categoryListDict[artifact.category] = 1
                totalCategory += 1
            else:
                categoryListDict[artifact.category] += 1

        # sort and print the list of file type counts
        d_view = [(v, k) for k, v in categoryListDict.items()]
        d_view.sort(reverse=True)  # natively sort tuples by first element
        print(BROWN + 'Sort by Category ({}):'.format(totalCategory) + RESET)
        # config the len of print for align
        len_num = len(str(max(int(v) for v, k in d_view))) # find the number digits
        len_name = max(len(k) for v, k in d_view) + 11  # len(RED+RESET) = 11
        print_sort_by(d_view, len_num, len_name)

        # sort and print the list of file type counts
        d_view = [(v, k) for k, v in fileTypeCountDict.items()]
        d_view.sort(reverse=True)  # natively sort tuples by first element
        print(BROWN + 'Sort by Extension ({}):'.format(totalExtension) + RESET)
        # config the len of print for align
        len_num = len(str(max(int(v) for v, k in d_view))) # find the number digits
        len_name = max(len(k) for v, k in d_view) + 11  # len(RED+RESET) = 11
        print_sort_by(d_view, len_num, len_name)

        # --------------------------------------------------------------
        print("\n" + UND + "   [ ID ] Last {} Modified File Name & its Timestamp                 ".format(args["print_number"]) + RESET)
        last_modified_file, last_modified_time, age = get_last_modify(config["PATH_KB_DATA"], args["print_number"])

        for i in range(0, len(last_modified_file)):
            result_line = " - [" + str(i).rjust(3) + " ] {} ({})\n".format(last_modified_time[i], age[i]) + BROWN \
                          + "          {}".format(last_modified_file[i]) + RESET
            print(result_line)
        print()

        # Write to history file
        with open(config["PATH_KB_HIST"], "w") as hfile:
            hfile.write("view_id,db_id\n")
            for view_id, result in enumerate(last_modified_file):
                for art in artifacts:
                    if art.path == result.split('/data/')[1]:
                        hfile.write("{},{}\n".format(view_id, art.id))

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total  # bytes

def get_last_modify(folder, print_number=5):
    file_name = list()
    get_file_time = list()
    for path, subdirs, files in os.walk(folder):
        for name in files:
            file_name.append(os.path.join(path, name))
            get_file_time.append(os.path.getmtime(os.path.join(path, name)))

    files = list(zip(file_name, get_file_time))
    files = sorted(files, key=lambda x: x[1], reverse=True)
    # last_modified_file = None if len(files) == 0 else files[0][0]

    last_modified_file = list()
    last_modified_time = list()
    age = list()

    for file in files[0:print_number]:
        last_modified_file.append(file[0])
        last_modified_time.append(datetime.fromtimestamp(
            os.path.getmtime(file[0])).strftime('%Y-%m-%d %H:%M:%S'))

        min_total = int(str(int((time.time() - os.path.getmtime(file[0])) // 60)))
        _day = min_total // (24 * 60)
        _hour = (min_total - _day * 24 * 60) // 60
        _min = min_total - _day * 24 * 60 - _hour * 60

        if _day:
            age.append("{day} {dayString} {hour} {hourString} {min} {minString} ago"
                       .format(day=_day, hour=_hour, min=_min,
                               dayString=("days" if _day > 1 else "day"),
                               hourString=("hours" if _hour > 1 else "hour"),
                               minString=("minutes" if _min > 1 else "minute"),
                               )
                       )
        elif _hour:
            age.append("{hour} {hourString} {min} {minString} ago"
                       .format(hour=_hour, min=_min,
                               hourString=("hours" if _hour > 1 else "hour"),
                               minString=("minutes" if _min > 1 else "minute"),
                               )
                       )
        else:
            age.append("{min} {minString} ago"
                       .format(min=_min,
                               minString=("minutes" if _min > 1 else "minute"),
                               )
                       )
    return last_modified_file, last_modified_time, age

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def print_sort_by(d_view, len_num, len_name):
    # convert data to pairs for print two column
    pairs = chunks(d_view, 2)
    for x in pairs:
        x1 = str(x[0][0])
        x2 = RED + str(x[0][1]) + RESET
        if len(x) > 1:
            x3 = str(x[1][0])
            x4 = RED + str(x[1][1]) + RESET
            print("   {} {}  {} {}".format(x1.rjust(len_num), x2.ljust(len_name), x3.rjust(len_num), x4.ljust(len_name)))
        else:
            print("   {} {} ".format(x1.rjust(len_num), x2.ljust(len_name)))
