#installation
npm install -g aws-cdk
#bootstrap
cdk bootstrap aws://<account-id>/<region>
#this will create a stack in the account with the name CDKToolkit
#you will need the right permissions to create the stack
