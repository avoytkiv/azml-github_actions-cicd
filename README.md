# azml-github_actions-cicd

Workflow:

- [x] Convert a notebook to production code	
- [x] Use an Azure Machine Learning job for automation
    - [x] Create a compute cluster
    - [x] Register a data asset 
    - [x] Create a job that takes the data asset as input and train script as a command
- [x] Trigger Azure Machine Learning jobs with GitHub Actions
    - [x] Create a service principal using the Azure CLI (to authenticate GitHub to manage the Azure Machine Learning workspace)
    - [x] Store the Azure credentials in a GitHub secret
    - [x] Define a GitHub Action in YAML
- [x] Trigger GitHub Actions with feature-based development
    - [x] Protect the main branch to block direct pushes to main
    - [x] Create a new branch
    - [x] Make a change and push it
    - [x] Create a pull request and merge it into the main branch
- [x] Work with linting and unit testing in GitHub Actions
    - [x] Install the tool (Flake8 or Pytest)
    - [x] Run the tests by specifying the folders within your repo that need to be checked.
- [x] Work with environments in GitHub Actions
- [x] Deploy a model with GitHub Action

Running a training job:


The production code is hosted in the main branch.
A data scientist creates a feature branch for model development.
The data scientist creates a pull request to propose to push changes to the main branch.
When a pull request is created, a GitHub Actions workflow is triggered to verify the code.
When the code passes linting and unit testing, the lead data scientist needs to approve the proposed changes.
After the lead data scientist approves the changes, the pull request is merged, and the main branch is updated accordingly.

## Useful resources

- [Verify your code locally](https://learn.microsoft.com/en-us/training/modules/source-control-for-machine-learning-projects/5-verify-your-code-locally)
- [Testing with pytest](https://learn.microsoft.com/en-us/training/modules/test-python-with-pytest/)
- [Setting up linters in VS Code](https://py-vscode.readthedocs.io/en/latest/files/linting.html#:~:text=Setting%20Up%20Linters%20in%20VS%20Code&text=To%20set%20them%20up%3A,option%20Python%3ELinting%3AFlake8%20Enabled)