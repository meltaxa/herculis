# Herculis

Use AWS Lambda to fetch your Sungrow Solar metrics and send these to the PVOutput website.

## Installation

Install serverless

```
npm install serverless
```

Setup your AWS Profile

```
export AWS_PROFILE=default && export AWS_REGION=us-west-1
```

In AWS, create a Parameter Store key called "sungrow_time" and set the value
to "nil".

Edit serverless.yml and update the following API credentials.

For PVOutput, you can find these under Settings.

For Sungrow Solarinfo Bank, you will need to traverse the website to discover
your Device ID, User ID and Plant ID. Start at 
http://www.solarinfobank.com/user/allplants and click on your Plant Name and 
then click edit. Each time noting the URL.

```
pvo_key: XXXXXXXX
pvo_systemid: XXXXXXXX
sgDeviceId: XXXXXXXX
sgPlantId: XXXXXXXX
sgUserId: XXXXXXXX
```

Deploy Herculis

```
serverless deploy 
```
