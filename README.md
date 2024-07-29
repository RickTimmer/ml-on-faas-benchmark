# ML on FaaS

## Prerequisites
Before you begin, ensure you have the following:

- AWS Account
- Basic understanding of AWS services
- Appropriate permissions to create IAM roles and policies
- AWS elastic container registry
- Authenticated AWS CLI locally
- A terraform backend for the state

### How to setup the IAM

To create an IAM user with the correct permissions you have to follow a couple of steps:

1. Sign in to the AWS Console via your browser
2. Navigate to IAM -> Users
3. Create a new user
4. Click the "Add permissions" dropdown and select "Create inline policy"
5. Change Visual mode to JSON
6. Add the following in the policy and save it

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": [
				"iam:*",
				"sns:*",
				"s3:*",
				"logs:*",
				"lambda:*",
				"ecs:*",
				"ec2:*",
				"ecr:*"
			],
			"Resource": "*"
		}
	]
}
```

7. Now you have a user with the correct permissions

### How to setup the ECR

To create a repository for the images follow these steps:

1. Sign in to the AWS Console via your browser
2. Navigate to ECR (Elastic Container Registry)
3. Create a new repository
4. Select private and give it a name
5. Now you have a repository that we will use later.

### How to authenticate AWS CLI

To get access to the CLI on your account do the following:

1. Install the AWS CLI
2. Sign in to the AWS Console via your browser
3. Head to the user we made before in the IAM settings
4. Create access keys for that user
5. In your local terminal use `aws configure` with the access defails for the user
6. Now you are be able to continue

### How to create a Terraform backend for the state

1. Sign in to the AWS Console via your browser
2. Navigate to S3
3. Create a new bucket
4. Add the configuration of that bucket to `artifacts/main.tf`


## Running the project

Before running the project you need to setup and understand a few things

### Configuration

Configurations are made in the `.env` file in the root of the project. The comments describe the expected values.

### Shell scripts

For running the project it contains a number of shell scripts which are all prefixed with a number:

- `0_destroy_infrastructure.sh` -> Cleans up the terraform setup
- `1_build_images.sh` -> Builds all images that will be used
- `2_init_terraform.sh` -> Initialized terraform, only has to be ran once
- `3_create_infrastructure.sh` -> Uses the artifacts to create all cloud resources
- `4_run_experiments.sh` -> Starts a container that publishes tasks to be ran by the cloud functions
- `5_get_logs.sh` -> Pulls all relevant logs locally so we can process them later
- `6_preprocess.sh` -> Reads the local logs and puts them in a usable CSV format

### Pickling the models

Most of the functions expect a pickled model to be present. For this you can use the scripts in `model_training`. Simply run the script of one and the pickled model should appear in the directory.

### Testing workflow

If you want to test some functions this could be your workflow.

1. Choose the things you want to benchmark and put them in the `.env` file (e.g. `k-means,pca`)
2. Choose the other variables such as memory and batch size, for these we use the `sentiment.csv` dataset
3. Build the images using script `1`
4. Initialize terraform if that hasn't been doen yet using script `2`
5. Create the infrastructure using script `3`
6. Run the experiments with script `4`
7. If those are done, pull the logs with `5`
8. Preprocess using script `6`
9. Do you analysis on the output

## Extending the project

There are a couple of ways to extend the project.

### Add another algorithm

1. Navigate to the `functions` directory
2. Identify which algorithm resembles your new one most code wise
3. Copy that folder
4. Change the `config.py` with the new name
5. Change the `handler.py` with your code, only change the implementation of the `handler` and `initializer` functions
6. Check if the `requirements.txt` file is still correct
7. If required, make a script that trains the model, pickles it, and saves it in the directory of your new function.
8. Done, you should be able to use this in the `.env` file with the directory name you used, make sure you rebuild the images after adding it to the `.env` file using script `1`

### Adding a dataset

Adding a dataset it slightly more involved.

1. Add your dataset to the `datasets` directory
2. In `artifacts/bucket.tf` add your dataset just like the ones that are already in there
3. In the `experiments/src/main.go` change the function `getDataset` to also account for your new dataset key
4. Done, use the dataset in the `.env` file and make sure to build the images again with `1` so the new `experiments` image is available
5. 