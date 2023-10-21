# End-to-end MLOPs with Azure ML

<img width="75%" alt="Screenshot 2023-10-11 at 12 16 46" src="https://github.com/avoytkiv/azml-github_actions-cicd/assets/74664634/5a413f01-1cb0-4400-b0a2-8ad913f743b1">  


**Tasks:**      

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
    - [x] Install the tools (`Flake8` and `Pytest`)
    - [x] Run the tests by specifying the folders within repo that need to be checked.
- [x] Work with environments in GitHub Actions
    - [x] Create `development`, `stage` and `production` environments in Github repo and store secrets for each environment 
    - [x] Add an approval check for the `production` environment.
    - [x] Remove the global repo `AZURE_CREDENTIALS` secret, so that each environment will only be able to use its own secret.
    - [x] For each environment, add the `AZURE_CREDENTIALS` secret that contains the service principal output.
    - [x] Create a new data asset in the `production` workspace
    - [x] Create one GitHub Actions workflow, triggered by changes being pushed to the `main` branch, with two jobs:
        - The **experiment** job that trains the model using the diabetes-dev-folder dataset in the `development` environment.
        - The **production** job that trains the model in the production environment, using the production data (the diabetes-prod-folder data asset as input).
    - [x] Add a condition that the production job is only allowed to run when the experiment job ran successfully
- [x] Deploy a model with GitHub Action
    - [x] Package and register the model as an MLflow model from the production job.
    - [x] Create an online (managed) endpoint.
    - [x] Test the deployed model automatically with the same GitHub Action workflow (ensure that the testing only happens when the model deployment is completed successfully).


### Use an Azure Machine Learning job for automation

Workflow:   

1. The production code is hosted in the main branch.
2. A data scientist creates a feature branch for model development.
3. The data scientist creates a pull request to propose to push changes to the main branch.
4. When a pull request is created, a GitHub Actions workflow is triggered to verify the code.
5. When the code passes linting and unit testing, the lead data scientist needs to approve the proposed changes.   


<img width="796" alt="Screenshot 2023-10-04 at 14 38 28" src="https://github.com/avoytkiv/azml-github_actions-cicd/assets/74664634/acd563d9-091c-4f6b-8294-5f40873f61af">   

6. After the lead data scientist approves the changes, the pull request is merged, and the main branch is updated accordingly.   

<img width="795" alt="Screenshot 2023-10-04 at 14 38 44" src="https://github.com/avoytkiv/azml-github_actions-cicd/assets/74664634/242e520a-8126-4841-995b-c2acc140f0f2">

Ideally, we don’t want to make the production data available in the experimentation (development) environment. Instead, data scientists will only have access to a small dataset which should behave similarly to the production dataset.

By reusing the training script, I can train the model in the production environment using the production data, simply by changing the data input.

The development environment is used for the inner loop:
- Data scientists train the model.
- The model is packaged and registered.

The staging environment is used for part of the outer loop:
- Test the code and model with linting and unit testing.
- Deploy the model to test the endpoint.

The production environment is used for another part of the outer loop:
- Deploy the model to the production endpoint. The production endpoint is integrated with the web application.
- Monitor the model and endpoint performance to trigger retraining when necessary.


### Deploy a model with GitHub Action

Using the Azure Machine Learning CLI (v2), I want to set up an automated workflow that will be triggered when a new model is registered. Once the workflow is triggered, the new registered model will be deployed to the production environment.

When logging a model with `mlflow.autologging()` during model training, the model is stored in the job output. Alternatively, I can store the model in an Azure Machine Learning datastore.

>[!Note]  
>When register the model as an MLflow type model, no need to provide a scoring script or environment to deploy the model.

To register the model, point to either a job's output, or to a location in an Azure Machine Learning datastore.

>[!Warning]
>Standard_DS1_v2 and Standard_F2s_v2 may be too small for bigger models and may
>lead to container termination due to insufficient memory, not enough space on >the disk, or probe failure as it takes too long to initiate the container.


Here is some testing data to use for the model:

```python
Pregnancies,PlasmaGlucose,DiastolicBloodPressure,TricepsThickness,SerumInsulin,BMI,DiabetesPedigree,Age
9,104,51,7,24,27.36983156,1.350472047,43
6,73,61,35,24,18.74367404,1.074147566,75
4,115,50,29,243,34.69215364,0.741159926,59
```   

>[!Note]   
>The merging conflicts should be resolved first. That will allow the workflow to run successfully.

## Useful commands

Create principal:  

```bash
az ad sp create-for-rbac --name "<service-principal-name>" --role contributor \
--scopes /subscriptions/<subscription-id>/resourceGroups/<your-resource-group-name> \
--json-auth
```

Get logs from building the image during deployment:  

```bash
az ml online-deployment get-logs -e <endpoint-name> -n <deployment-name> -l 100
```

## Useful resources

- [Verify your code locally](https://learn.microsoft.com/en-us/training/modules/source-control-for-machine-learning-projects/5-verify-your-code-locally)
- [Setting up linters in VS Code](https://py-vscode.readthedocs.io/en/latest/files/linting.html#:~:text=Setting%20Up%20Linters%20in%20VS%20Code&text=To%20set%20them%20up%3A,option%20Python%3ELinting%3AFlake8%20Enabled)
- [Testing with pytest](https://learn.microsoft.com/en-us/training/modules/test-python-with-pytest/)
- [Testing with Numpy](https://numpy.org/doc/stable/reference/testing.html)
- [Azure - Connect GitHub Actions to Azure](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure?tabs=azure-portal%2Clinux#use-the-azure-login-action-with-a-service-principal-secret)
- [Share models, components, and environments across workspaces with registries](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-share-models-pipelines-across-workspaces-with-registries?view=azureml-api-2&tabs=cli)
- [Best practices to organize Azure Machine Learning resources](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/ai-machine-learning-resource-organization)
- [How to deploy MLFLow models](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-mlflow-models?view=azureml-api-2&tabs=azureml)

