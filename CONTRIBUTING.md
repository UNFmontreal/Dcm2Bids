# Contributing to dcm2bids

Welcome to the `dcm2bids` repository and thank you for thinking about
contributing! :heart:

This document has been written in such a way you feel at ease to find your way
on how you can make a difference for the `dcm2bids` community.

We tried to cover as much as possible in few words possible. If you have any
questions don't hesitate to share them in the section below.

There are multiple ways to be helpful to the `dcm2bids` community.

If you already know what you are looking for, you can select one of the section
below:

- [Contributing to dcm2bids](#contributing-to-dcm2bids)
  - [Welcome](#welcome)
  - [Contributing through Neurostars](#contributing-through-neurostars)
  - [Contributing through GitHub](#contributing-through-github)
  - [Recommended workflow](#recommended-workflow)
    - [Open an issue or choose one to fix](#open-an-issue-or-choose-one-to-fix)
    - [Fork the `dcm2bids` repository](#fork-the-dcm2bids-repository)
    - [Test your branch](#test-your-branch)
    - [Check list](#check-list)
    - [Submit and tag your pull request](#submit-and-tag-your-pull-request)
  - [Recognizing your contribution](#recognizing-your-contribution)
  - [Thank you!](#thank-you)

If you don't know where or how to get started, keep on reading below.

## Welcome

`dcm2bids` is a small project started in 2017 by Christophe Bedetti
([@cbedetti](https://github.com/cbedetti)). In 2021, we have started a
new initiative and we're excited to have you join!

You can introduce yourself on our [Welcome to Dcm2Bids Discussion][dcm2bids-introduce-yourself]
and tell us how you would like to contribute in the `dcm2bids` community.
Let us know what your interests are and we will help you find an issue to
contribute to if you haven't already spotted one yet. Most of our discussions
will take place on open [issues][dcm2bids-issues] and in the newly created
[GitHub Discussions][dcm2bids-discussions]. Thanks so much!
As a reminder, we expect all contributions to `dcm2bids` to adhere to our
[Code of Conduct][dcm2bids-coc].

## Contributing through Neurostars

The `dcm2bids` community highlight all contributions to `dcm2bids`. Helping users
on [Neurostars](https://neurostars.org) forum is one of them.

Neurostars has a `dcm2bids` tag that helps us following any question regarding
the project. You can ask Neurostars to notify you when a new message tagged with `dcm2bids` has been posted. If you know the answer, you can reply following our
[code of conduct][dcm2bids-coc].

??? info "How to receive email notifications from Neurostars"
    If you want to receive email notifications, you have to go set your settings accordingly on Neurostars. The procedure below will get you to this (personalized) URL: https://neurostars.org/u/**YOURUSERNAME**/preferences/tags :

    1. Click on your picture in the top right corner
    2. Click on the 👤 (user) icon
    3. Click on ⚙️ **Preferences**
    4. Click on **Notifications**
    5. Click on **Tags**
    6. We recommend to add `dcm2bids` to the **Watched** section, but you can add it to any section that fits your need.

## Contributing through GitHub

[Git][link_git] is a really useful tool for [version control][vcs].
[GitHub][link_github] sits on top of git and supports collaborative and
distributed working.

Before you start you'll need to set up a free [GitHub][link_github] account and
sign in. You can sign up [through this link][link_github_signup] and then _interact_ on our repository at [https://github.io/UNFmontreal/Dcm2Bids](https://github.io/UNFmontreal/Dcm2Bids).

You'll use [Markdown][markdown] to discuss on GitHub. You can think of
Markdown as a few little symbols around your text that
will allow GitHub to render the text with a little bit of formatting. For
example you can write words as **bold** (`**bold**`), or in _italics_
(`*italics*`), or as a [link](https://youtu.be/dQw4w9WgXcQ)
(`[link](https://youtu.be/dQw4w9WgXcQ)`) to another webpage.

!!! info "Did you know?"
    Most software documentation websites are written in Markdown. Even the `dcm2bids` [documentation website][dcm2bids-doc] is written in Markdown!

    GitHub has a helpful guide to [get you started with writing and formatting Markdown][writing_formatting_github].

## Recommended workflow

We will be excited when you'll suggest a new PR to fix, enhance or develop
`dcm2bids`. In order to make this as fluid as possible we recommend to follow
this workflow:

### Open an issue or choose one to fix

Issues are individual pieces of work that need to be completed to move the
project forwards. Before starting to work on a new pull request we highly
recommend you open an issue to explain what you want to do and how it echoes a
specific demand from the community. Keep in mind the [scope][dcm2bids-scope] of
the `dcm2bids` project. If you have more an inquiry or suggestion to make 
than a bug to report, we encourage you to start a conversation in the
[Discussions section][dcm2bids-discussions].

A general guideline: if you find yourself tempted to write a great big issue
that is difficult to describe as one unit of work, please consider splitting it
into two or more. Moreover, it will be interesting to see how others approach
your issue and give their opinion and maybe give you advice to find the best way
to code it. Finally, it will prevent you to start working on something that is
already in progress.

The list of all labels is [here][dcm2bids-labels] and include:

- [![Help Wanted](https://img.shields.io/badge/-help%20wanted-159818.svg)][link_helpwanted]
  _These issues contain a task that a member of the team has determined we need
  additional help with._

  If you feel that you can contribute to one of these issues, we especially
  encourage you to do so!

- [![Bug](https://img.shields.io/badge/-bug-fc2929.svg)][link_bugs] _These
  issues point to problems in the project._

  If you find new a bug, please give as much detail as possible in your issue,
  including steps to recreate the error. If you experience the same bug as one
  already listed, please add any additional information that you have as a
  comment.

- [![Enhancement](https://img.shields.io/badge/-enhancement-84b6eb.svg)][link_enhancement]
  _These issues are asking for enhancements to be added to the project._

  Please try to make sure that your enhancement is distinct from any others that
  have already been requested or implemented. If you find one that's similar but
  there are subtle differences please reference the other request in your issue.

### Fork the `dcm2bids` repository

This way you'll be able to work on your own instance of `dcm2bids`. It will be a
safe place where nothing can affect the main repository. Make sure your master
branch is always [up-to-date][git-fork-update] with dcm2bids' master branch. You
can also follow these command lines.

The first time you try to sync your [fork][git-fork], you may have to set the [upstream branch][git-fork-remote]:
```bash
git remote add upstream https://github.com/UNFmontreal/Dcm2Bids.git
git remote -v # Verify the new upstream repo appears.
```

```bash
git checkout master
git fetch upstream master
git merge upstream/master
```

Then create a new branch for each issue. Using a new branch allows you to follow
the standard GitHub workflow when making changes. [This guide][git-guide]
provides a useful overview for this workflow. Please keep the name of your
branch short and self explanatory.

```bash
git checkout -b MYBRANCH
```

### Test your branch

If you are proposing new features, you'll need to add new tests as well. In any
case, you have to test your branch prior to submit your PR.

If you have new code you will have to run pytest:

```bash
pytest -v tests/test_dcm2bids.py
```

`dcm2bids` project is following [PEP8][pep8] convention whenever possible. You
can check your code using this command line:

```bash
flake8 FileIWantToCheck
```

Regardless, when you open a Pull Request, we use [Tox][tox] to run all unit and
integration tests.

If you have propose a PR about a modification on the documentation you can have
a preview from an editor like Atom using `CTRL+SHIFT+M`.

### Check list

Pull Request Checklist (For Fastest Review):

- [x] Check that all tests are passing ("All tests passsed")
- [x] Make sure you have docstrings for any new functions
- [x] Make sure that docstrings are updated for edited functions
- [x] Make sure you note any issues that will be closed by your PR
- [x] Add a clear description of the purpose of you PR

### Submit and tag your pull request

When you submit a pull request we ask you to follow the tag specification. In
order to simplify reviewers work, we ask you to use at least one of the
following tags:

- ==[BRK]== for changes which break existing builds or tests
- ==[DOC]== for new or updated documentation
- ==[ENH]== for enhancements
- ==[FIX]== for bug fixes
- ==[TST]== for new or updated tests
- ==[REF]== for refactoring existing code
- ==[MAINT]== for maintenance of code
- ==[WIP]== for work in progress

You can also combine the tags above, for example if you are updating both a test
and the documentation: [TST, DOC].

## Recognizing your contribution

We welcome and recognize [all contributions][link_all-contributors-spec] from
documentation to testing to code development. You can see a list of current
contributors in the [README](/README.md) (kept up to date by the [all
contributors bot][link_all-contributors-bot]). You can see
[here][link_all-contributors-bot-usage] for instructions on how to use the bot.

## Thank you!

You're amazing. :wave::smiley:

_&mdash; Based on contributing guidelines from the
[STEMMRoleModels][link_stemmrolemodels] and [tedana][link_tedana] projects._

---

[markdown]: https://en.wikipedia.org/wiki/Markdown
[link_git]: https://git-scm.com/
[link_github]: http://github.com/
[link_github_signup]: https://github.com/join
[link_tedana]: https://github.com/ME-ICA/tedana
[link_stemmrolemodels]: https://github.com/KirstieJane/STEMMRoleModels
[dcm2bids-labels]: https://github.com/UNFmontreal/Dcm2Bids/labels
[link_bugs]: https://github.com/UNFmontreal/Dcm2Bids/labels/bug
[link_helpwanted]: https://github.com/UNFmontreal/Dcm2Bids/labels/help%20wanted
[link_enhancement]: https://github.com/UNFmontreal/Dcm2Bids/labels/enhancement
[dcm2bids-issues]: https://github.com/UNFmontreal/Dcm2Bids/issues
[dcm2bids-coc]: https://unfmontreal.github.io/Dcm2Bids/CODE_OF_CONDUCT
[dcm2bids-discussions]: https://github.com/UNFmontreal/Dcm2Bids/discussions/
[dcm2bids-introduce-yourself]: https://github.com/UNFmontreal/Dcm2Bids/discussions/123
[dcm2bids-scope]: /#scope
[dcm2bids-doc]: /
[writing_formatting_github]: https://guides.github.com/features/mastering-markdown/
[git-fork]: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-forks
[git-fork-remote]: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork
[git-fork-update]: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork
[git-guide]: https://guides.github.com/introduction/flow/
[pep8]: https://www.python.org/dev/peps/pep-0008/
[tox]: https://tox.readthedocs.io/
[link_all-contributors-spec]: https://allcontributors.org/docs/en/specification
[link_all-contributors-bot]: https://allcontributors.org/docs/en/bot/overview
[link_all-contributors-bot-usage]: https://allcontributors.org/docs/en/bot/usage
[vcs]: https://en.wikipedia.org/wiki/Version_control
