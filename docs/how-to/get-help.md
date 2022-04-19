---
summary: How-to Get help and support for dcm2bids-related questions
authors:
  - Samuel Guay
date: 2022-04-17
---

# How to get help and support

We work hard to make sure dcm2bids is robust and we welcome comments and
questions to make sure it meets your use case!

While the dcm2bids volunteers and the neuroimaging community at large do their
best to respond to help requests about dcm2bids, there are steps you can do to
try to find answers and ways to optimize how to ask questions on the different
channels. The path may be different according to your situation whether you want
to ask a usage question or report a bug.

## Where to **look** for answers

Before looking for answers on any Web search engine, the best places to look for
answers are:

### 1. **This documentation**

You can use the built-in search function with key words or look throughout the
documentation. If you end up finding your answer somewhere else, please inform
us by [opening an issue](#open-an-issue). If you faced an undocumented challenge
while using dcm2bids, it is very likely others will face it as well. By
gathering community knowledge, the documentation will improve drastically. Refer
to the [Request a new feature section](#request-a-new-feature) below if you are
unfamiliar with GitHub and issues.

### 2. **Community support channels**

There is a couple of places you can look for

#### **[NeuroStars][neurostars]**

!!! info "What is [neurostars.org][neurostars]?"

    [NeuroStars][neurostars] is a question and answer forum for neuroscience
    researchers, infrastructure providers and software developers, and free to
    access. It is managed by the [International Neuroinformatics Coordinating
    Facility (INCF)][incf] and it is widely used by the neuroimaging community.

[NeuroStars][neurostars] is a gold mine of information about how others solved
their problems or got answered to their questions regarding anything
neuroscience, especially neuroimaging. [NeuroStars][neurostars] is a good place
to ask questions related to dcm2bids and the [BIDS][bids] standards. Before
asking your own questions, you may want to **first browse through questions that
were tagged with the [dcm2bids tag][neurostars-dcm2bids]**.

To look for everything related to a specific tag, here's how you can do it for
the **dcm2bids** tag:

!!! tip "The quick way"

    Type in your URL bar [https://neurostars.org/tag/dcm2bids][neurostars-dcm2bids] or click directly on it to bring the page will all post tagged with a dcm2bids tag. Then if you click on search, the **dcm2bids** will already be selected for you.

1.  Go to [https://neurostars.org][neurostars].
2.  Click on the **search** (:mag:) icon.
3.  Either **click on options** to bring the advanced search and go to next step
    **OR start typing _dcm2bids_**.
4.  In the tag section on the right pane, select **dcm2bids**.
5.  Type your question in the search bar.
    <!-- prettier-ignore-start -->

    - You might have to refine your question a couple of times to find the most
    relevant answers.
    <!-- prettier-ignore-end -->

??? example "Steps in pictures"

    ![](../assets/img/neurostars-1-dark.png#border#only-dark){ loading=lazy }
    ![](../assets/img/neurostars-2-dark.png#border#only-dark){ loading=lazy }
    ![](../assets/img/neurostars-3-dark.png#border#only-dark){ loading=lazy }
    ![](../assets/img/neurostars-4-dark.png#border#only-dark){ loading=lazy }
    ![](../assets/img/neurostars-1-light.png#border#only-light){ loading=lazy }
    ![](../assets/img/neurostars-2-light.png#border#only-light){ loading=lazy }
    ![](../assets/img/neurostars-3-light.png#border#only-light){ loading=lazy }
    ![](../assets/img/neurostars-4-light.png#border#only-light){ loading=lazy }

The next step before going on a search engine is to go where we develop
dcm2bids, namely GitHub.

#### **GitHub**

While we use GitHub to develop dcm2bids, some people have opened issues that
could be relevant to your situation. You can browse through the open and closed
issues: https://github.com/UNFmontreal/Dcm2Bids/issues?q=is%3Aissue and search
for specific keywords or error messages.

If you find a specific issue and would like more details about it, you can
simply write an additional comment in the _Leave a comment_ section and press
_Comment_.

??? example "Example in picture"

    ![](../assets/img/github-issue-dark.png#border#only-dark){ loading=lazy }
    ![](../assets/img/github-issue-light.png#border#only-light){ loading=lazy }

## Where to **ask** for questions, report a bug or request a feature

After having read thoroughly all information you could find online about your
question or issue, you may still some lingering questions or even more
questions - that is okay! After all, maybe you would like to use dcm2bids for a
specific use-case that has never been mentioned anywhere before. Below are
described 3 ways to request help depending on your situation:

1. Ask a question about dcm2bids
2. Report a bug
3. Request a new feature

### Questions related to using dcm2bids:

We encourage you to post your question on [NeuroStars][neurostars] with
[dcm2bids][neurostars-dcm2bids] as an optional tag. The tag is really important
because [NeuroStars][neurostars-dcm2bids] will notify the `dcm2bids` team only
if the tag is present. You will get a quicker reply this way.

### Report a bug

If you think you've found a bug :bug:, and you could not find an issue already
mentioning the problem, please open an issue on [our
repository][dcm2bids-issues]. If you don't know how to open an issue, refer to
the [open an issue](#open-an-issue) section below.

### Request a new feature

If you have more an inquiry or suggestion to make than a bug to report, we
encourage you to start a conversation in the [Discussions
section][dcm2bids-discussions]. Similar to the bug reporting procedure, follow
the [open an issue](#open-an-issue) below.

---

### Open an issue

To open or comment on an issue, you will need a [GitHub][github] account.

Issues are individual pieces of work (a bug to fix or a feature) that need to be
completed to move the project forwards. We highly recommend you open an issue to
explain what you want to do and how it echoes a specific demand from the
community. Keep in mind the scope of the `dcm2bids` project.

A general guideline: if you find yourself tempted to write a great big issue
that is difficult to describe as one unit of work, please consider splitting it
into two or more. Moreover, it will be interesting to see how others approach
your issue and give their opinion and advice to solve it.

If you have more an inquiry or suggestion to make than a bug to report, we
encourage you to start a conversation in the [Discussions
section][dcm2bids-discussions]. Note that issues may be converted to a
discussion if deemed relevant by the maintainers.

[bids]: http://bids.neuroimaging.io
[dcm2bids-doc]: https://unfmontreal.github.io/Dcm2Bids/
[dcm2bids-discussions]: https://github.com/UNFmontreal/Dcm2Bids/discussions/
[dcm2bids-issues]: https://github.com/UNFmontreal/Dcm2Bids/issues
[github]: https://github.com
[neurostars]: https://neurostars.org/
[neurostars-dcm2bids]: https://neurostars.org/tag/dcm2bids
