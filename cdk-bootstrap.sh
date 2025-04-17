#installation
npm install -g aws-cdk
#bootstrap
cdk bootstrap aws://<account-id>/<region>
#this will create a stack in the account with the name CDKToolkit
#you will need the right permissions to create the stack
cdk init 
#this will create a new cdk project in the current directory
cd init sample-app --language=python
#this will create a new cdk project in the current directory with the name sample-app
#and the language python
#you can also use other languages like java, csharp, typescript, etc    
cdk synth
#this will create a cloudformation template in the cdk.out directory
#you can also use cdk synth --no-staging to create the template without staging

cdk deploy
#this will deploy the stack to the account

cdk destroy
#this will destroy the stack in the account
# do not delete the CDKToolkit stack