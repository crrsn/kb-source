# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb search command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

from typing import Dict
import kb.db as db
import kb.initializer as initializer
import kb.printer.search as printer
import kb.history as history


def listc(args: Dict[str, str], config: Dict[str, str]):
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

    tags_list = None
    if args["tags"] and args["tags"] != "":
        tags_list = args["tags"].split(';')

    conn = db.create_connection(config["PATH_KB_DB"])
    rows = db.get_artifacts_by_filter(
        conn,
        title=args["query"],
        category=args["category"],
        tags=tags_list,
        status=args["status"],
        author=args["author"])

    # rows.sort(key=lambda x: x[1])
    artifacts = sorted(rows, key=lambda x: x.category)

    # Write to history file
    history.write(config["PATH_KB_HIST"], artifacts)

    # Is full_identifier mode enabled?
    if args["full_identifier"]:
        printer.print_search_result_full_mode(artifacts)
        return

    # print hello world for test
    if args["print"]:
        print("Hello World")
        return

    # Print resulting list
    color_mode = not args["no_color"]
    if args["verbose"]:
        printer.print_search_result_verbose(artifacts, color_mode)
    else:
        printer.print_search_result(artifacts, color_mode)

