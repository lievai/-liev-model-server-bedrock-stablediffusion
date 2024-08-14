# Liev Model Server - Amazon Bedrock - Stable Diffusion

Liev Model Servers are meant to abstract prompt complexity in LLM Prompting.


```
                                __________________________________
                                |                                |
| The Liev Dispatcher |-------> | Liev Model Server Bedrock - SD | -----> Amazon Bedrock
                                |________________________________|


```

## Installation

### IAM Permissions

#### User
1) Create a service user on IAM
2) The user must have a policy that allows Bedrock operations. See below example:

```
{
    "Statement": [
        {
            "Action": [
                "bedrock:GetAgentVersion",
                "bedrock:ListDataSources",
                "bedrock:GetFoundationModelAvailability",
                "bedrock:GetKnowledgeBase",
                "bedrock:GetModelInvocationLoggingConfiguration",
                "bedrock:ListTagsForResource",
                "bedrock:ListKnowledgeBases",
                "bedrock:GetAgent",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:GetDataSource",
                "bedrock:ListModelCustomizationJobs",
                "bedrock:ListAgents",
                "bedrock:ListAgentVersions",
                "bedrock:ListCustomModels",
                "bedrock:ListAgentKnowledgeBases",
                "bedrock:GetCustomModel",
                "bedrock:GetUseCaseForModelAccess",
                "bedrock:InvokeModel",
                "bedrock:GetAgentAlias",
                "bedrock:ListFoundationModelAgreementOffers",
                "bedrock:QueryKnowledgeBase",
                "bedrock:GetIngestionJob",
                "bedrock:ListIngestionJobs",
                "bedrock:GetModelCustomizationJob",
                "bedrock:GetAgentActionGroup",
                "bedrock:GetAgentKnowledgeBase",
                "bedrock:InvokeAgent",
                "bedrock:ListAgentActionGroups",
                "bedrock:ListProvisionedModelThroughputs",
                "bedrock:GetFoundationModel",
                "bedrock:GetProvisionedModelThroughput",
                "bedrock:ListFoundationModels",
                "bedrock:ListAgentAliases"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ],
    "Version": "2012-10-17"
}
```

3) You will need to generate access keys for the created user.
For more information about creting AWS Access Keys, see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html

### Model Access

Model access is enablement is needed for the model server to work.
1) Access Amazon Bedrock in AWS Console
2) In the left menu, go to Bedrock configurations > Model access
3) Search for Stability AI > SDXL 1.0. Click on "Available to request". Perform the following steps  - you'll need to read and agree with the EULA.

### Environment Variables

| Variable  | Description |Values | Default |
| ------------- |-------------|-------------|-------------|
| LOG_LEVEL     | Python logging level |CRITICAL, ERROR, WARNING, INFO, DEBUG      |INFO    |
| LIEV_USERNAME     | Username used for HTTP Basic Auth | User defined value | - |
| LIEV_PASSWORD     | Password user for HTTP Basic Auth     | User defined value | - |
| AWS_ACCESS_KEY_ID     | AWS IAM Access Key ID     | User defined value. Must be provided | - |
| AWS_SECRET_ACCESS_KEY     | AWS IAM Secret Access Key. Must be provided     | User defined value | - |
| AWS_REGION_NAME    | AWS Region     | User defined value. Eg. us-east1. Must be provided | - |
| BEDROCK_MODELID     | Bedrock Model Id    | Check AWS Documentation for possible values  | stability.stable-diffusion-xl-v1 |

# Running

#### Simple standalone - You may create a venv in you preferred way
```
$ pip install -r requirements.txt
$ start_model.sh
```

#### Docker - There is a Dockerfile for image building
```
$ docker build -t liev-bedrock-stablediffusion-model-server .
$ docker run -e <Envs> -d liev-bedrock-stablediffusion-model-server 
```

# Credits

- Adriano Lima and Cleber Marques (Inmetrics)
