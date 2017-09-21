# Herculis

Use AWS Lambda to fetch your Sungrow Solar metrics and send these to the PVOutput website.

Herculis downloads the Sungrow metrics from the [SolarInfo Bank](http://www.solarinfobank.com/):

![alt tag](docs/sungrow_pic.png)

And uploads the relevant data to [PVOutput.org](https://pvoutput.org):

![alt tag](docs/pvoutput_pic.png)

## Prequisites

Your Sungrow inverter is registered to their SolarInfo Bank site. 

An [AWS account](https://aws.amazon.com). Herculis is an AWS Lamdba function. 
If this will be your only Lambda function, you will remain within the 
[AWS Free Tier](https://aws.amazon.com/lambda/pricing/). There will be nominal 
charges (a few cents per month) for Amazon S3 and data transfers.

To deploy the AWS Lamdba function, the [Serverless](https://serverless.com/framework/docs/providers/aws/guide/installation/) framework is used.

## Installation

1. Download or clone this repository to your local workstation.

### Serverless Framework

2. To ease the setup and configuration of this Lamdba, Serverless is used to 
deploy the code and it's dependancies.

   On your local workstation, install [serverless](https://serverless.com/framework/docs/providers/aws/guide/installation/).

   ```
   npm install serverless
   ```

3. Setup your AWS Profile as per [Serverless guidelines](https://serverless.com/framework/docs/providers/aws/guide/credentials/).

4. Edit serverless.yml and update the following API credentials.

   ```
   # PVOutput API settings, see https://pvoutput.org/account.jsp
   pvo_key: XXXXXXXX
   pvo_systemid: XXXXXXXX
   # Sungrow settings
   sgDeviceId: XXXXXXXX
   sgUnitId: XXXXXXXX
   ```

   For PVOutput, you can find these under [Settings](https://pvoutput.org/account.jsp).

   For Sungrow's Solarinfo Bank, you will need to traverse their website to 
   discover your Device ID and User ID. Following these instructions if you are
   using the Google Chrome web browser.

   In Chrome, login to Sungrow's SolarInfo Bank site at 
   [http://www.solarinfobank.com](http://www.solarinfobank.com). 

   Enable Developer Tools (under View and Developer menus). 

   Click on the Network tab and ensure recording is enabled.

   Navigate to Device Data on Sungrow's site.

   In the Developer Tools window, look for the Name that
   looks like `?unitId=123456&deviceId=123456`. For example: 

   ```
   http://www.solarinfobank.com/plant/devicestructtree/12345?unitid=54321&deviceid=123456789.
   ```

   In the above example, the sgUnitId will be the number after 
   uitid, in this case 54321.

   The sgDeviceId in this case is 123456789.

### Deployment

5. Deploy Herculis:

   From your local workstation, deploy Herculis to AWS:

   ```
   serverless deploy 
   ```

6. Now browse to your [PVOutput.org](https://pvoutput.org/) system.

## Acknowledgements

The python interface to PV Output API was forked from [sungrow2pvoutput](https://github.com/kronicd/sungrow2pvoutput).
