# Contributing to dcm2bids

Welcome to the dcm2bids repository and thank you for thinking about
 contributing! :heart:

This document has been written in such a way you feel at ease to find your way
 on how you can make a difference for the `dcm2bids` community.

We tried to cover as much as possible in few words possible. If you have any
questions don't hesitate to share them in the section below.

There are multiple ways to be helpful to the dcm2bids community

If you already know what you are looking for, you can select one of the section below:

* [Welcome](#welcome)
* [Contributing through Neurostars](#contributing-through-neurostars)
* [Contributing through Github ](#contributing-through-github)
  + [Create a pull request](#create-a-pull-request)
  + [Create an issue](#create-a-pull-request)
  + [Fork the dcm2bids repository](#fork-the-dcm2bids-repository)
  + [Test your branch](#test-your-branch)
  + [Check list](#check-list)
  + [Submit and tag your pull request](#submit-and-tag-your-pull-request)
  + [Create an issue, tag with labels and contribute](#create-an-issue,-tag-with-labels-and-contribute)
* [Recognizing your contribution](#recognizing-your-contribution)

Don't know where to get started?
Read [Welcome](#welcome) and pop into
this [thread][dcm2bids-introduce-yourself] to introduce yourself! Let us know what your interests are and we
will help you find an issue to contribute to. Thanks so much!

## Welcome

dcm2bids is a small project started in 2017 by Christophe Bedetti([@cbedetti](https://github.com/cbedetti)).
Now 2021, we are starting a new initiative and we're excited to have you join!
You can introduce yourself on the open issue [welcome][dcm2bids-welcome] and
tell us how you would like to contribute in the `dcm2bids` community.
Most of our discussions will take place on open [issues][dcm2bids-issues].

As a reminder, we expect all contributions to `dcm2bids` to adhere
to our [code of conduct][dcm2bids-coc].

## Contributing through Neurostars

The dcm2bids community highlight all contributions to `dcm2bids`.
Helping users on Neurostars forum is one of them.

Neurostars has a `dcm2bids` tag that helps us following any question regarding
the project. You can ask for Neurostars to send you notifications when a new
 message has been posted. If you know the answer, you can reply following
 our [Code of Conduct][dcm2bids-coc].

## Contributing through GitHub

[git][link_git] is a really useful tool for version control.
[GitHub][link_github] sits on top of git and supports collaborative and distributed working.

Before you start you'll need to set up a free [GitHub][link_github] account and sign in.
Here are some [instructions][link_signupinstructions].

You'll use [Markdown][markdown] to chat in issues and pull requests on GitHub.
You can think of Markdown as a few little symbols around your text that will allow GitHub
to render the text with a little bit of formatting.
For example you could write words as bold (`**bold**`), or in italics (`*italics*`),
or as a [link][rick_roll] (`[link](https://https://youtu.be/dQw4w9WgXcQ)`) to another webpage.

GitHub has a helpful page on
[getting started with writing and formatting Markdown on GitHub][writing_formatting_github].

### Create a pull request

We will be excited when you'll suggest a new PR to fix, enhance or develop `dcm2bids`.
In order to make this as fluid as possible we recommend to follow this workflow:

### Create an issue

Before starting to work on a new pull request we highly recommend you open an
 issue with the label *enhancement* to explain what you want to do and how it
 echoes a specific demand from the community. Moreover, it will be
 interesting to see how others approach your issue and give their opinion and
 maybe give you advice to find the best way to code it. Finally, it will prevent
 you to start working on something that is already in progress.
 Keep in mind the [scope][dcm2bids-scope] of the `dcm2bids` project.

#### Fork the `dcm2bids` repository

This way you'll be able to work on your own instance of `dcm2bids`. It will be
a safe place where nothing can affect the main repository. Make sure your
master is always [up-to-date][git-fork-update]. You can also follow these
command lines.

```
git checkout master
git fetch upstream master
git merge upstream/master
```

Then create a new branch for each issue. Using a new branch allows you to
follow the standard GitHub workflow when making changes.
[This guide][git-guide] provides a useful overview for this workflow. 
Please keep the name of your branch short and self explanatory.

```
git checkout -b MYBRANCH
```

#### Test your branch

If you are proposing new features, you'll need to add new tests as well.
In any case, you have to test your branch prior to submit your PR.

If you have new code you will have to run pytest:

```
pytest -v tests/test_dcm2bids.py
```

`dcm2bids` project is following [PEP8][pep8] convention whenever possible.
You can check your code using this command line:

```
flake8 FileIWantToCheck
```

Regardless, when you open a Pull Request, we use [Tox][tox] to run all unit and
integration tests.

If you have propose a PR about a modification on the documentation you can
have a preview from an editor like Atom using `CTRL+SHIFT+M`.

#### Pull request: check list

Pull Request Checklist (For Fastest Review):

- [ ] Check that all tests are passing ("All tests passsed")
- [ ] Make sure you have docstrings for any new functions
- [ ] Make sure that docstrings are updated for edited functions
- [ ] Make sure you note any issues that will be closed by your PR
- [ ] Add a clear description of the purpose of you PR

#### Submit and tag your pull request

When you submit a pull request we ask you to follow the tag specification. In order to simplify reviewers work, we ask you to use at least one of the following tags:

* [BRK] for changes which break existing builds or tests
* [DOC] for new or updated documentation
* [ENH] for enhancements
* [FIX] for bug fixes
* [TST] for new or updated tests
* [REF] for refactoring existing code
* [MAINT] for maintenance of code
* [WIP] for work in progress

You can also combine the tags above, for example if you are updating both a test and the documentation: [TST, DOC].


### Create an issue, tag with labels and contribute

Issues are individual pieces of work that need to be completed to move the project forwards. A general guideline: if you find yourself tempted to write a great big issue that is difficult to describe as one unit of work, please consider splitting it into two or more.

The current list of labels are [here][dcm2bids-labels] and include:

* [![Help Wanted](https://img.shields.io/badge/-help%20wanted-159818.svg)][link_helpwanted] *These issues contain a task that a member of the team has determined we need additional help with.*

    If you feel that you can contribute to one of these issues, we especially encourage you to do so!

* [![Bug](https://img.shields.io/badge/-bug-fc2929.svg)][link_bugs] *These issues point to problems in the project.*

    If you find new a bug, please give as much detail as possible in your issue, including steps to recreate the error.
    If you experience the same bug as one already listed, please add any additional information that you have as a comment.

* [![Enhancement](https://img.shields.io/badge/-enhancement-84b6eb.svg)][link_enhancement] *These issues are asking for enhancements to be added to the project.*

    Please try to make sure that your enhancement is distinct from any others that have already been requested or implemented.
    If you find one that's similar but there are subtle differences please reference the other request in your issue.


## Recognizing your contribution

We welcome and recognize [all contributions][link_all-contributors-spec]
from documentation to testing to code development.
You can see a list of current contributors in the [README](/README.md)
(kept up to date by the [all contributors bot][link_all-contributors-bot]).
You can see [here][link_all-contributors-bot-usage] for instructions on
how to use the bot.

## Thank you!

You're amazing. :wave::smiley:

*&mdash; Based on contributing guidelines from the [STEMMRoleModels][link_stemmrolemodels] and [tedana][link_tedana] projects.*

[link_git]: https://git-scm.com/
[link_github]: http://github.com/
[link_tedana]: https://github.com/ME-ICA/tedana
[link_stemmrolemodels]: https://github.com/KirstieJane/STEMMRoleModels
[dcm2bids-labels]: https://github.com/UNFmontreal/Dcm2Bids/labels
[link_bugs]: https://github.com/UNFmontreal/Dcm2Bids/labels/bug
[link_helpwanted]: https://github.com/UNFmontreal/Dcm2Bids/labels/help%20wanted
[link_enhancement]: https://github.com/UNFmontreal/Dcm2Bids/labels/enhancement
[dcm2bids-issues]: https://github.com/UNFmontreal/Dcm2Bids/issues
[dcm2bids-coc]: https://github.com/UNFmontreal/Dcm2Bids/CODE_OF_CONDUCT.md
[dcm2bids-introduce-yourself]: https://github.com/UNFmontreal/Dcm2Bids/issues
[writing_formatting_github]: https://help.github.com/articles/getting-started-with-writing-and-formatting-on-github
[git-fork-update]: https://help.github.com/articles/syncing-a-fork/
[git-guide]: https://guides.github.com/introduction/flow/
[pep8]: https://www.python.org/dev/peps/pep-0008/
[tox]: https://tox.readthedocs.io/
