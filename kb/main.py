# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb main module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

__all__ = ()

import sys

from kb.cl_parser import parse_args
from kb.commands.add import add
from kb.commands.delete import delete
from kb.commands.edit import edit
from kb.commands.erase import erase
from kb.commands.export import export
from kb.commands.grep import grep
from kb.commands.ingest import ingest
from kb.commands.search import search
from kb.commands.sync import sync
from kb.commands.template import template
from kb.commands.update import update
from kb.commands.view import view
from kb.config import DEFAULT_CONFIG
from kb.commands.listc import listc
from kb.commands.info import info

COMMANDS = {
    "add": add,
    "delete": delete,
    "edit": edit,
    "update": update,
    "list": search,
    "view": view,
    "grep": grep,
    "erase": erase,
    "import": ingest,
    "export": export,
    "template": template,
    "sync": sync,
    "listc": listc,
    "info": info,
}


def dispatch(function, *args, **kwargs):
    """
    Dispatch command line action to proper
    kb function
    """
    return COMMANDS[function](*args, **kwargs)


def main():
    """Main routine of kb."""
    args = parse_args(sys.argv[1:])

    cmd = args.command
    cmd_params = vars(args)

    dispatch(cmd, cmd_params, config=DEFAULT_CONFIG)
