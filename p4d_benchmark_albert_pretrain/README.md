Login to ECR
`aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-1.amazonaws.com`

Build

`bash push_dlc_sagemaker.sh albert-pretrain-p4 latest 967669495843`

Push to ECR

`bash push_dlc_sagemaker.sh albert-pretrain-p4 latest 967669495843`

Copy Training data to S3

`aws s3 cp s3://xxxxxx/albert-pretrain s3://xxxxx/pretrain_data/ --recursive`

Launch Training job

`python launch.py --num_nodes=1`


`python launch.py --num_nodes=1 --node_type='ml.p3.8xlarge' --max_steps=6000`