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
import kb.printer.search as printer
from kb.printer.style import ALT_BGROUND, BOLD, UND, RESET


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
        print(config["PATH_KB"])
        print(config["PATH_KB_DB"])

        print(config)

    else:
        None_list = None
        conn = db.create_connection(config["PATH_KB_DB"])
        rows = db.get_artifacts_by_filter(
            conn,
            title=args["query"],
            category=None_list,
            tags=None_list,
            status=None_list,
            author=None_list)

        # rows.sort(key=lambda x: x[1])
        artifacts = sorted(rows, key=lambda x: x.category)

        #printer.print_search_result(artifacts, True)

        print("\n" + UND + "Database information" + RESET)
        print("Number of artifacts: " + str(len(artifacts)))

        count_jpg = 0
        count_pdf = 0
        for view_id, artifact in enumerate(artifacts):

            if (artifact.title.endswith('jpg')):
                count_jpg += 1
            if (artifact.title.endswith('pdf')):
                count_pdf += 1

        print("How mamy jpg files: " + str(count_jpg))
        print("How mamy pdf files: " + str(count_pdf))