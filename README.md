# trigger-travis.sh

This script triggers a new [Travis-CI](https://travis-ci.org/) job.
Ordinarily, a new Travis job is triggered when a commit is pushed to a
GitHub repository.  The `trigger-travis.py` script provides a programmatic
way to trigger a new Travis job.

## Usage

    ./trigger-travis.py [--pro] [--branch BRANCH] [--vars VARS] \
        GITHUBID GITHUBPROJECT TRAVIS_ACCESS_TOKEN [MESSAGE]

`--pro` means to use `travis-ci.com` instead of `travis-ci.org`

`--branch BRANCH` means to use BRANCH instead of master.

`TRAVIS_ACCESS_TOKEN` is the Travis access token; see below for details.
(In the example above, `~/private/.travis-access-token` contains the Travis access token.)

`MESSAGE` is a string that will be displayed by Travis's web interface.
(For a commit push, Travis uses the commit message.)

## Travis access token

Your Travis access token is the text after "Your access token is " in
the output of this compound command:

    travis login && travis token

If the `travis` program isn't installed, then install it using either of these two
commands (whichever one works):

    gem install travis
    sudo apt-get install ruby-dev && sudo gem install travis

*Don't* do `sudo apt-get install travis` which installs a trajectory analyzer.

Note that the Travis access token output by `travis token` differs from the
Travis token available at https://travis-ci.org/profile .
If you store it in in a file, make sure the file is not readable by others,
for example by running:  chmod og-rwx ~/private/.travis-access-token

## Use in `.travis.yml`

To make one Travis build (if successful) trigger a different Travis build, do two things:

1.  Set an environment variable `TRAVIS_ACCESS_TOKEN` by navigating to
    https://travis-ci.org/MYGITHUBID/MYGITHUBPROJECT/settings.

    The `TRAVIS_ACCESS_TOKEN` environment variable will be set when Travis runs
    the job, but it won't be visible to anyone browsing https://travis-ci.org/ .

2.  Add the following to your `.travis.yml` file, where you replace
    *OTHERGITHUB* by a specific downstream project, but you leave
    `$TRAVIS_ACCESS_TOKEN` as literal text:

```
jobs:
  include:
    - stage: trigger downstream
      script: |
        if [[ ($TRAVIS_BRANCH == master) &&
              ($TRAVIS_PULL_REQUEST == false) ]] ; then
          curl -LO --retry 3 https://raw.githubusercontent.com/InformaticsMatters/trigger-travis/master/trigger-travis.py
          sh trigger-travis.py OTHERGITHUBID OTHERGITHUBPROJECT $TRAVIS_ACCESS_TOKEN
        fi
```

You don't need to supply a MESSAGE argument to `trigger-travis.py`; it will
default to the current (upstream) repository, commit id, and one line of
the commit message.

## Credits and alternatives

A fork of https://github.com/plume-lib/trigger-travis
