# Mini Terraform Practice Project

## Overview
A hands-on Terraform tutorial that recreates the key concepts from your main platform in a minimal, cost-free environment. Perfect for practicing Terraform workflows without affecting production.

## What You'll Learn
1. **Module Creation**: Build reusable Terraform modules
2. **Resource Import**: Import existing AWS resources into Terraform
3. **State Management**: Understand terraform.tfstate
4. **Variables & Outputs**: Pass data between modules
5. **Lifecycle Management**: Create, update, destroy resources
6. **Best Practices**: ignore_changes, placeholder patterns

## Project Structure
```
MiniPracticeProject/
├── README.md                    # This file
├── TUTORIAL.md                  # Step-by-step walkthrough
├── CONCEPTS.md                  # Terraform concepts explained
├── terraform/
│   ├── modules/
│   │   ├── s3-practice/         # S3 bucket module
│   │   ├── dynamodb-practice/   # DynamoDB table module
│   │   ├── lambda-practice/     # Lambda function module
│   │   ├── cloudwatch-practice/ # CloudWatch log group module
│   │   └── sns-practice/        # SNS topic module
│   └── environments/
│       └── practice/
│           ├── main.tf          # Main configuration
│           ├── variables.tf     # Input variables
│           ├── outputs.tf       # Output values
│           └── terraform.tfvars # Variable values
└── lambda/
    └── hello-world/
        └── index.py             # Simple Lambda function

```

## Resources Created (All Free Tier)
- **1 S3 Bucket**: practice-terraform-learning-[random]
- **1 DynamoDB Table**: PracticeTable (on-demand billing)
- **1 Lambda Function**: hello-world-practice
- **1 CloudWatch Log Group**: /aws/lambda/hello-world-practice
- **1 SNS Topic**: practice-alerts

**Estimated Cost**: $0.00 (within AWS free tier)

## Prerequisites
- AWS CLI configured (`aws configure`)
- Terraform installed
- PowerShell 7+
- AWS account with free tier available

## Quick Start
```powershell
# Navigate to practice environment
cd MiniPracticeProject/terraform/environments/practice

# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Create resources
terraform apply

# Destroy everything when done
terraform destroy
```

## Learning Path
1. Read `CONCEPTS.md` - Understand Terraform fundamentals
2. Follow `TUTORIAL.md` - Step-by-step implementation
3. Practice the full cycle 3-5 times
4. Experiment with modifications

## Safety Features
- All resources tagged with `Environment = "practice"`
- Unique random suffixes prevent naming conflicts
- No production data involved
- Complete teardown in 1 command

## Time Estimate
- First run: 45-60 minutes
- Subsequent practice: 15-20 minutes
- Teardown: 2-3 minutes

## Next Steps After Mastery
Once comfortable with this mini project:
1. Add more complex resources (API Gateway, CloudFront)
2. Practice importing existing resources
3. Create your own modules
4. Apply learnings to production infrastructure
