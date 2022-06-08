# 2022/06/07
# How to use shtab (auto complete) function

## What is 'shtab'

Automagic shell tab completion for Python CLI applications

## Test OS

1. Ubuntu - bash

## How to install 

### Install the shtab

    https://github.com/iterative/shtab

### Install kb tool - branch name: feature/shtab

	https://github.com/crrsn/kb-source/tree/feature/shtab

### Create a bash_completion file manually

	Run 'kb -s bash' to generate all configuration text
    Copy these text as a file (name: kb) and put it to /etc/bash_completion.d/

### Re-open the terminal

## How to use it? (Press [TAB] to list all option you can use)

    kb [TAB]
    kb -[TAB]
    kb add -[TAB]
    kb list -[TAB]

## Reference

- https://github.com/iterative/shtab

- https://docs.iterative.ai/shtab/use/
