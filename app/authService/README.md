build and deploy authService:
1. start Docker
2. login to AWS
    `aws login --profile tony-dev --region us-east-1`
3. login to AWS ECR
    ` aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 555146423685.dkr.ecr.us-east-1.amazonaws.com`

3. build the authService stack:
    `npm.cmd run build`

4. deploy the authService stack:
    `npm.cmd run deploy`