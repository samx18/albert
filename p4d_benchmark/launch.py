import argparse
import logging
import sagemaker
from sagemaker.pytorch import PyTorch

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='run training')
    parser.add_argument('--model_type', type=str, default='albert_base')
    parser.add_argument('--platform', type=str, default='SM', help='SM(sagemaker) or EC2')
    parser.add_argument('--num_nodes', type=int, default=1, help='Number of nodes')
    parser.add_argument('--node_type', type=str, default='ml.p3.8xlarge', help='Node type')
    #parser.add_argument('--node_type', type=str, default='ml.p3dn.24xlarge', help='Node type')
    parser.add_argument('--bucket_name', type=str, default='sagemaker-us-east-1-967669495843')
    parser.add_argument('--output_dir', type=str, default='albert_finetune')
    parser.add_argument("--image_uri", type=str,
                        default='967669495843.dkr.ecr.us-east-1.amazonaws.com/albert-p4:latest')
    parser.add_argument('--role_name', type=str, default='arn:aws:iam::967669495843:role/service-role/AmazonSageMaker-ExecutionRole-20190812T143756')

    args = parser.parse_args()

    # initialization
    # role = args.role
    #role = 'arn:aws:iam::427566855058:role/yu-dev'
    role = args.role_name
    image_uri = args.image_uri
    output_dir_s3_addr = f's3://{args.bucket_name}/{args.output_dir}'

    # Start training job
    sess = sagemaker.Session()
    print(f"Starting albert training with {args.num_nodes} nodes.")
    hyperparameters = {"num_nodes": args.num_nodes,
                       "platform": args.platform
                       }
    # max_run = 86400 * 2 = 172800
    estimator = PyTorch(base_job_name=f"p4d-benchmark-{args.num_nodes}nodes",
                        source_dir=".",
                        entry_point="dist_train.py",
                        image_uri=image_uri,
                        role=role,
                        instance_count=args.num_nodes,
                        instance_type=args.node_type,
                        container_log_level=0,
                        debugger_hook_config=False,
                        hyperparameters=hyperparameters,
                        volume_size=200,
                        output_path=output_dir_s3_addr,
                        sagemaker_session=sess,
                        max_run=259200
                        )

    estimator.fit()
    print('end of the whole process')

if __name__ == "__main__":
    main()
