#installation
npm install -g aws-cdk
#bootstrap
cdk bootstrap aws://<account-id>/<region>
#this will create a stack in the account with the name CDKToolkit
#you will need the right permissions to create the stack
cdk init 
#this will create a new cdk project in the current directory
cd init sample-app --language=pythonP
#this will create a new cdk project in the current directory with the name sample-app
#and the language python
#you can also use other languages like java, csharp, typescript, etc
