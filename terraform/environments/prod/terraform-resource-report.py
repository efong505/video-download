#!/usr/bin/env python3
"""
Terraform Resource Report Generator
Generates a nice HTML report of all Terraform-managed resources
"""

import subprocess
import json
import sys
from collections import defaultdict
from datetime import datetime

# Ensure UTF-8 output for emojis
sys.stdout.reconfigure(encoding='utf-8')

def run_terraform_command(command, cwd):
    """Run a terraform command and return output"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return None

def get_resource_list(terraform_dir):
    """Get list of all resources in Terraform state"""
    output = run_terraform_command("terraform state list", terraform_dir)
    if not output:
        return []
    return [line.strip() for line in output.split('\n') if line.strip()]

def get_resource_details(resource_address, terraform_dir):
    """Get details of a specific resource"""
    output = run_terraform_command(f'terraform state show -json "{resource_address}"', terraform_dir)
    if not output:
        return None
    try:
        return json.loads(output)
    except:
        return None

def categorize_resources(resources):
    """Group resources by type"""
    categorized = defaultdict(list)
    
    for resource in resources:
        # Handle module resources
        if resource.startswith('module.'):
            parts = resource.split('.')
            # module.email.aws_lambda_function.sender
            if len(parts) >= 3:
                resource_type = parts[2]  # aws_lambda_function
                categorized[resource_type].append(resource)
        else:
            # aws_s3_bucket.main
            parts = resource.split('.')
            if len(parts) >= 2:
                resource_type = parts[0]  # aws_s3_bucket
                categorized[resource_type].append(resource)
    
    return categorized

def get_resource_icon(resource_type):
    """Get emoji icon for resource type"""
    icons = {
        'aws_s3_bucket': '🪣',
        'aws_lambda_function': '⚡',
        'aws_dynamodb_table': '🗄️',
        'aws_iam_role': '🔐',
        'aws_api_gateway': '🌐',
        'aws_cloudfront': '☁️',
        'aws_sns_topic': '📢',
        'aws_sqs_queue': '📬',
        'aws_cloudwatch': '📊',
        'aws_route53': '🌍',
        'aws_acm_certificate': '🔒',
        'aws_lambda_layer': '📦',
        'aws_iam_policy': '📜',
        'aws_lambda_permission': '✅',
    }
    
    for key, icon in icons.items():
        if key in resource_type:
            return icon
    return '📄'

def get_resource_name(resource_type):
    """Get friendly name for resource type"""
    names = {
        'aws_s3_bucket': 'S3 Bucket',
        'aws_s3_bucket_versioning': 'S3 Versioning',
        'aws_s3_bucket_server_side_encryption_configuration': 'S3 Encryption',
        'aws_s3_bucket_cors_configuration': 'S3 CORS',
        'aws_s3_bucket_policy': 'S3 Bucket Policy',
        'aws_s3_bucket_public_access_block': 'S3 Public Access Block',
        'aws_lambda_function': 'Lambda Function',
        'aws_lambda_layer_version': 'Lambda Layer',
        'aws_lambda_permission': 'Lambda Permission',
        'aws_dynamodb_table': 'DynamoDB Table',
        'aws_iam_role': 'IAM Role',
        'aws_iam_role_policy_attachment': 'IAM Role Policy',
        'aws_iam_policy': 'IAM Policy',
        'aws_api_gateway_rest_api': 'API Gateway',
        'aws_api_gateway_resource': 'API Resource',
        'aws_api_gateway_method': 'API Method',
        'aws_api_gateway_integration': 'API Integration',
        'aws_api_gateway_deployment': 'API Deployment',
        'aws_cloudfront_distribution': 'CloudFront Distribution',
        'aws_cloudfront_origin_access_control': 'CloudFront OAC',
        'aws_sns_topic': 'SNS Topic',
        'aws_sns_topic_subscription': 'SNS Subscription',
        'aws_sqs_queue': 'SQS Queue',
        'aws_cloudwatch_log_group': 'CloudWatch Log Group',
        'aws_cloudwatch_metric_alarm': 'CloudWatch Alarm',
        'aws_cloudwatch_event_rule': 'EventBridge Rule',
        'aws_route53_zone': 'Route53 Zone',
        'aws_route53_record': 'Route53 Record',
        'aws_acm_certificate': 'ACM Certificate',
    }
    return names.get(resource_type, resource_type.replace('aws_', '').replace('_', ' ').title())

def generate_html_report(categorized, terraform_dir):
    """Generate HTML report"""
    
    total_resources = sum(len(resources) for resources in categorized.values())
    total_types = len(categorized)
    env_name = terraform_dir.split('\\')[-1]
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terraform Resources Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            color: #666;
            margin-top: 10px;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .resource-group {{
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            background: white;
        }}
        
        .resource-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            font-size: 1.3em;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .resource-count {{
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .resource-list {{
            padding: 0;
            list-style: none;
        }}
        
        .resource-item {{
            padding: 15px 20px;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            align-items: center;
            transition: background 0.2s ease;
        }}
        
        .resource-item:last-child {{
            border-bottom: none;
        }}
        
        .resource-item:hover {{
            background: #f8f9fa;
        }}
        
        .resource-module {{
            background: #fff3cd;
            color: #856404;
            padding: 3px 10px;
            border-radius: 5px;
            font-size: 0.85em;
            margin-left: 10px;
            font-weight: 600;
        }}
        
        .resource-name {{
            font-family: 'Courier New', monospace;
            color: #333;
            flex-grow: 1;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        .timestamp {{
            color: #999;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Terraform Resources Report</h1>
            <p>Infrastructure managed by Terraform</p>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_resources}</div>
                <div class="stat-label">Total Resources</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_types}</div>
                <div class="stat-label">Resource Types</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{env_name}</div>
                <div class="stat-label">Environment</div>
            </div>
        </div>
        
        <div class="content">
"""
    
    # Sort by resource count (descending)
    sorted_categories = sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True)
    
    for resource_type, resources in sorted_categories:
        icon = get_resource_icon(resource_type)
        friendly_name = get_resource_name(resource_type)
        
        html += f"""
            <div class="resource-group">
                <div class="resource-header">
                    <span>{icon} {friendly_name}</span>
                    <span class="resource-count">{len(resources)} resource{'s' if len(resources) > 1 else ''}</span>
                </div>
                <ul class="resource-list">
"""
        
        for resource in sorted(resources):
            # Check if it's a module resource
            if resource.startswith('module.'):
                parts = resource.split('.')
                module_name = parts[1]
                resource_display = '.'.join(parts[2:])
                html += f"""
                    <li class="resource-item">
                        <span class="resource-name">{resource_display}</span>
                        <span class="resource-module">module: {module_name}</span>
                    </li>
"""
            else:
                html += f"""
                    <li class="resource-item">
                        <span class="resource-name">{resource}</span>
                    </li>
"""
        
        html += """
                </ul>
            </div>
"""
    
    html += f"""
        </div>
        
        <div class="footer">
            <p>Terraform Directory: <strong>{terraform_dir}</strong></p>
            <p>Generated by Terraform Resource Report Generator</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    # Get Terraform directory from command line or use default
    if len(sys.argv) > 1:
        terraform_dir = sys.argv[1]
    else:
        terraform_dir = r"c:\Users\Ed\Documents\Programming\AWS\Downloader\terraform\environments\prod"
    
    print(f"📊 Generating Terraform resource report...")
    print(f"📁 Directory: {terraform_dir}\n")
    
    # Get resource list
    print("🔍 Fetching resource list...")
    resources = get_resource_list(terraform_dir)
    
    if not resources:
        print("❌ No resources found or error reading Terraform state")
        print("   Make sure you're in a Terraform directory with a valid state file")
        return
    
    print(f"✅ Found {len(resources)} resources\n")
    
    # Categorize resources
    print("📦 Categorizing resources...")
    categorized = categorize_resources(resources)
    
    # Generate HTML report
    print("📝 Generating HTML report...")
    html = generate_html_report(categorized, terraform_dir)
    
    # Save report
    output_file = "terraform-resources-report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Report generated: {output_file}")
    print(f"\n🌐 Open the file in your browser to view the report!")
    
    # Print summary to console
    print("\n" + "="*60)
    print("📊 RESOURCE SUMMARY")
    print("="*60)
    
    for resource_type, resources in sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True):
        icon = get_resource_icon(resource_type)
        friendly_name = get_resource_name(resource_type)
        print(f"{icon} {friendly_name}: {len(resources)}")
    
    print("="*60)
    print(f"Total: {len(get_resource_list(terraform_dir))} resources across {len(categorized)} types")
    print("="*60)

if __name__ == "__main__":
    main()
