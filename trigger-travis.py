#!/usr/bin/env python

# Trigger a new Travis-CI job.
# A Python variant of trigger-travis.sh that supports passing variables.
# See that bash script for the basics behind what's happening.
#
# Here we add the ability to pass variables to the dependent project
# and move from bash to a much richer scripting environment (ie. Python).
# Add variables using '--vars' where VARS is a comma-separated list of
# variable names and values, e.g. "A=B,C=D". The variables will be added
# to the travis evv/global list.
#
# Usage:
#   trigger-travis.py
#       [--pro]
#       [--branch BRANCH]
#       [--vars VARS]
#       GITHUBID
#       GITHUBPROJECT
#       TRAVIS_ACCESS_TOKEN
#       [MESSAGE]

import argparse
import os
import requests

# Build a command-line parser
# and parse the command-line...
PARSER = argparse.ArgumentParser(description='Trigger Travis')
PARSER.add_argument('--pro', action="store_true", default=False)
PARSER.add_argument('--branch', type=str, default='master')
PARSER.add_argument('--vars', type=str)
PARSER.add_argument('namespace', type=str)
PARSER.add_argument('project', type=str)
PARSER.add_argument('token', type=str)
PARSER.add_argument('message', nargs='?')
ARGS = PARSER.parse_args()

# This repo?
TRAVIS_REPO_SLUG = os.environ.get('TRAVIS_REPO_SLUG')

# Any variables to process?
# True if the length of '--vars' is greater than 2
# i.e. we have "A=1". "-" is passed in by some scripts to imply none.
# If there are arguments, split the comma-separated list into a simple list
VARS = []
if ARGS.vars and len(ARGS.vars) > 2:
    VARS = ARGS.vars.split(',')
# A user message?
# If not then supply a basic one,
# so the downstream repo logs why it was triggered.
if ARGS.message:
    MESSAGE = ARGS.message
else:
    MESSAGE = 'Triggered by upstream build of "{}"'.format(TRAVIS_REPO_SLUG)
# Travis com or org?
TRAVIS_URL = 'travis-ci.com' if ARGS.pro else 'travis-ci.org'

# Construct the payload
# Headers and URL
DATA = {'request': {'branch': ARGS.branch,
                    'message': MESSAGE,
                    'config': {'merge_mode': 'deep_merge_append',
                               'env': {'global': VARS}}}}
HEADERS = {'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Travis-API-Version': '3',
           'Authorization': 'token {}'.format(ARGS.token)}
URL = 'https://api.{}/repo/{}%2F{}/requests'.format(TRAVIS_URL,
                                                    ARGS.namespace,
                                                    ARGS.project)

# Trigger...
print(URL)
response = requests.post(URL, headers=HEADERS, json=DATA, timeout=4.0)
print(response)
print(response.text)
