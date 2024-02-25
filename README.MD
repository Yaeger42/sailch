# Challenge
# Requirements
- Docker
- Python 3.11 or above
- An AWS Account
- A verified email in AWS SES
- An AWS Account with a user that has access to the following:
 - Lambda Invocation and creation, Sending messages in SES and creating Roles in IAM as well as policies
## How to run local tests:
- To run the tests localy, build the docker image with:
```bash
docker build docker build . -t lambda-tests -f Dockerfile-tests
```
- Run the image:
```bash
docker run lambda-tests
```
And check the output, it should be something like this:
```bash
============================= test session starts ==============================
platform linux -- Python 3.11.8, pytest-8.0.1, pluggy-1.4.0
rootdir: /usr/src/app
collected 2 items

tests/test_email_build.py .
tests/test_github.py .

============================== 2 passed in 0.16s ===============================
```

## How to test it locally

- Modify `src/lambda_function.py` and change `send_email("projectdcd@gmail.com", "projectdcd@gmail.com", body_email)` those emails for your email
- Now, let's build the docker image
```bash
docker build --platform linux/amd64 -t local-lambda:test .
```
- Run the image:
```bash
docker run --platform linux/amd64 -d -v ~/.aws-lambda-rie:/aws-lambda -p 9000:8080 \
    -e AWS_SECRET_ACCESS_KEY=ENV_VARIABLE_VALUE_1 \
    -e AWS_ACCESS_KEY_ID=ENV_VARIABLE_VALUE_2 \
    --entrypoint /aws-lambda/aws-lambda-rie \
    local-lambda:test \
        /usr/local/bin/python -m awslambdaric lambda_function.lambda_handler
```
- Replace `ENV_VARIABLE_VALUE_1` and `ENV_VARIABLE_VALUE_2` with their values from your account.

- Once it's running, send a curl to:
```bash
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```
If everything went okay you should get a response like this: `null` and an email in your inbox, otherwise, check the docker logs

## Deploying with terraform
In order to do this, first navigate to the folder `src`. 
After that, make a directory called `package` with `mkdir package`.
<br>
Install the requirements:
```bash
pip install --target ./package -r requirements.txt
```
cd back into `src` and run:
```bash
zip deployment-package.zip lambda_function.py github.py email.py __init__.py
```
Once that's done go into `terraform/` and run
`terraform init` 
<br>
After that: `terraform plan` <br>
And then `terraform apply` and follow the instructions in the terminal
and voilá, Lambda deployed.

# Extra
While this is ready for production, I'd add a couple of changes to it if was to run in a MUCH bigger scale:
- Divide it into 3 lambdas
- The first Lambda would gather the data from github's API and trigger the second lambda
- The second lambda would send the data to a SQS queue and once processed it would send it into another Lambda
- The third lambda would receive the message from SQS and send it through SNS as well as making a record in Dynamodb, where it would store the emails
In this way the segregation of roles would be more precise but also it would also make sure that every email is processed and in case there's one missing, retry it.
