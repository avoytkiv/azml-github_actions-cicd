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
- [x] Work with linting and unit testing in GitHub Actions
- [x] Work with environments in GitHub Actions
- [x] Deploy a model with GitHub Action

Running a training job:

```shell
az ad sp create-for-rbac --name "test-principal" --role contributor --scopes /subscriptions/a8c5d49d-e0aa-4576-97cc-fa6b18ce0f6a resourceGroups/RG001 --json-auth
```
   
![job output](https://github.com/avoytkiv/azml-github_actions-cicd/assets/74664634/c78084f5-3800-41d0-847b-de8d42d3f774)
