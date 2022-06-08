# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb export command module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import time
from typing import Dict
from kb.printer.style import UND, BOLD, UND, RESET, RED, MAGENTA, GREEN
import git
import kb.filesystem as fs
import socket

def sync(args: Dict[str, str], config: Dict[str, str]):
    """
    Synchronize the knowledge base with a remote repository.

    Arguments:
    args:           - a dictionary containing the following fields:
                      file -> a string representing the wished output
                        filename
    config:         - a configuration dictionary containing at least
                      the following keys:
                      PATH_KB           - the main path of KB
    """

    operation = args["operation"]

    if operation == "init":
        if is_local_git_repo_initialized(config["PATH_KB_GIT"]):
            print("Warning: a git repository already exists...")
            cancel_repo = input(
                "Do you want to re-init your repository ? [Type YES in that case] "
            )
            if cancel_repo == "YES":
                fs.remove_directory(config["PATH_KB_GIT"])
                git_init(config["PATH_KB"])
            else:
                print('Maybe you wanted to type "kb sync push" or "kb sync pull"!')
        else:
            git_init(config["PATH_KB"])
    elif operation == "push":
        if not is_local_git_repo_initialized(config["PATH_KB_GIT"]):
            print("Warning: You did not initialize any repository...")
            print("try: kb sync init")
            return
        git_push(config["PATH_KB"])
    elif operation == "pull":
        if not is_local_git_repo_initialized(config["PATH_KB_GIT"]):
            print("Warning: no local git repository has been instantiated!")
            cancel_repo = input(
                "Do you want to remove possible local kb files "
                "and sync from a remote repository? [Type YES in that case] "
            )
            if cancel_repo == "YES":
                try:
                    fs.remove_directory(config["PATH_KB"])
                except BaseException:
                    pass
                git_clone(config["PATH_KB"])
        else:
            git_pull(config["PATH_KB_GIT"])
    elif operation == "info":
        if not is_local_git_repo_initialized(config["PATH_KB_GIT"]):
            print("No local git repository has been instantiated!")
            return
        show_info(config["PATH_KB"])
    elif operation == "reset":
        if not is_local_git_repo_initialized(config["PATH_KB_GIT"]):
            print("No local git repository has been instantiated!")
            return
        git_reset(config["PATH_KB"])
    else:
        print("Error: No valid operation has been specified")
        return


def is_local_git_repo_initialized(git_path):
    if fs.is_directory(git_path):
        return True

def git_reset(repo_path):

    repo = git.cmd.Git(repo_path)
    _status = repo.execute(["git", "status", "--porcelain"])

    if _status:
        print(UND + "Git status (git status --porcelain)" + RESET)
        print(GREEN + "(M: Modified / D: Deleted / ?? Untracked new file)" + RESET)
        print(RED + _status + RESET)

        answer = input("Above changed (modified or new created) data will be reset. " +
                       RED + "\nAre you sure you want to reset? [y/n]" + RESET)
        confirm = answer.lower() not in ["y", "yes"]
        if confirm:
            print("No data was reset")
            return
        repo = git.Repo(repo_path)
        repo.git.reset('--hard')
        print("Repository correctly reset!")

    else:
        print("No need to reset. Your repository is clean.")


def git_push(repo_path):
    try:
        kb_repo = git.Repo(repo_path)
        kb_repo.git.add("--all")
        timestamp = time.strftime("%d/%m/%Y-%H:%M:%S")
        kb_repo.index.commit("[{hostname}] kb synchronization {ts}".format(hostname=socket.gethostname(), ts=timestamp))
        kb_repo.remote(
            name="origin").push(
            refspec="{}:{}".format(
                "main",
                "main"))
        print("Repository correctly synchronized to remote!")
    except BaseException:
        print("Some error occurred while pushing the code")
        print(
            "Check your internet connection or the existence of the remote repository"
        )


def git_pull(repo_path):

    repo = git.cmd.Git(repo_path[:-4])
    _status = repo.execute(["git", "status", "--porcelain"])
    if _status:
        print(RED + "Pull Fault: The local data is change. Please remove it and try again!" + RESET)
        print(RED + "Using 'git reset --hard' to reset the repository." + RESET)
        print(UND + "Git status (git status --porcelain)" + RESET)
        print(GREEN + "(M: Modified / D: Deleted / ?? Untracked new file)" + RESET)
        print(RED + _status + RESET)

    else:
        try:
            kb_repo = git.Repo(repo_path)
            origin = kb_repo.remotes.origin
            origin.pull(origin.refs[0].remote_head)
            print("Repository correctly synchronized from remote!")
        except BaseException:
            print("Some error occurred while pulling the code")
            print(
                "Check your internet connection or the existence of the remote repository"
            )


def git_clone(repo_path):
    remote_repo_url = input(
        "Insert the URL of the remote repo (e.g., https://github/user/mykb): "
    )
    if remote_repo_url:
        git.Repo.clone_from(remote_repo_url, repo_path)
        print("Knowledge base correctly pulled from remote!")
    else:
        print("Error: Check your internet connection or provide a valid repository")


def git_init(repo_path):
    print("Create a remote empty repository on github/gitlab or other git provider...")
    remote_repo_url = input(
        """Insert the URL of the created empty remote repo
         (e.g., https://github/user/mykb): """
    )
    if remote_repo_url:
        local_repo = git.Repo.init(repo_path)
        remote = local_repo.create_remote("origin", url=remote_repo_url)
        local_repo.git.add("--all")
        timestamp = time.strftime("%d/%m/%Y-%H:%M:%S")
        local_repo.index.commit("kb synchronization {ts}".format(ts=timestamp))
        print("Initialization with remote may take time...")
        print("Please provide remote credentials and wait...")
        remote.push(refspec="{}:{}".format("main", "main"))
        print("Remote repository correctly initialized!")
    else:
        print("Error: Provide a valid remote URL")


def show_info(repo_path):

    #print(git.cmd.Git(repo_path[:-4]).execute(["git", "fetch", "origin main"]))

    repo = git.cmd.Git(repo_path)

    print("\n" + UND + "Git status (git status --porcelain)" + RESET)
    print(GREEN + "(M: Modified / D: Deleted / ?? Untracked new file)" + RESET)
    print(RED + repo.execute(["git", "status", "--porcelain"]) + RESET)

    print("\n" + UND + "Branch info (git branch -av)" + RESET + '')
    print(repo.execute(["git", "branch", "-av"]))

    print("\n" + UND + "Remote repository (git remote -v)" + RESET)
    print(repo.execute(["git", "remote", "-v"]))

    print("\n" + UND + "Logs (git log --oneline -n3 --graph)" + RESET)
    print(repo.execute(["git", "log", "--oneline", "-n3", "--graph"]))
