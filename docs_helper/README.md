# How to build the doc locally

The GHA workflow is set to build the documentation and has more steps than
the usual `mkdocs serve`. So if you want to see the documentation locally,
you can use the following steps:

1. Create a virtual environment and install the dependencies in `requirements-docs.txt` with python 3.11.
2. Install dcm2bids within the virtual environment: `pip install -e .`.
3. Run `dcm2bids -h > docs_helper/help.txt && dcm2bids_helper -h > docs_helper/helper.txt && dcm2bids_scaffold -h > docs_helper/help_scaffold.txt`
4. Run `mkdocs serve` to see the documentation locally.

Note that this will only run the latest local version of the documentation. `mike` takes care of the versioning through the GHA workflow.