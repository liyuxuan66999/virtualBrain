# Auth Service Infra

This CloudFormation stack creates the auth service Lambda execution role, CloudWatch
logs permission, and the Lambda function that runs the ECR container image.

Deploy or update the stack:
Under VirtualBrainV1 root folder execute:

```powershell
aws cloudformation deploy `
  --stack-name virtualbrain-auth-service `
  --template-file infra/auth-service.yaml `
  --capabilities CAPABILITY_NAMED_IAM `
  --parameter-overrides `
    ImageUri=555146423685.dkr.ecr.us-east-1.amazonaws.com/virtualbrain-auth-service:latest `
    JwtSecret=dev-secret-only `
    DatabaseUrl=sqlite:///./virtualbrain.db `
  --region us-east-1
```

Invoke the deployed Lambda with the local test event:

```powershell
aws lambda invoke `
  --function-name virtualbrain-auth-service `
  --payload fileb://app/authService/event.json `
  response.json `
  --region us-east-1

Get-Content response.json
```

For real deployments, replace `JwtSecret` and `DatabaseUrl` with non-local values.
