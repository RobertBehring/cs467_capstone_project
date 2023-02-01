# CS 467 Capstone Project
**Authors:** Jada Young, Eric Riemer, Robert Behring

## GCP Functions Usage
These are instructions for using the custom GCP client library functions [gcp_storage]
### Authenticate Google Cloud Client Libraries for Local Dev Environments
Source: https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev

1. Install and initialize the Google Cloud CLI
    - Instructions: https://cloud.google.com/sdk/docs/install 

2. Create a credential file by entering the following command:
`gcloud auth application-default login`

The client libraries and ADC will recognize the location of the credential file and use this to authenticate access to services.


More about Application Default Credentials: https://cloud.google.com/docs/authentication/application-default-credentials#personal


### Environment Variables (TBD)
The following .env file structure should be used:

## data_maker program Usage
These are instructions for using the custom program [data_maker.py] to produce randomized data sets for both Ookla and Mlab JSONs.

### USAGE:
```python
python data_maker.py [-p] [-h] [-ookla NUM] [-mlab NUM]
```
> -p (Optional parameter)         :: Prints data to STDOUT <br>
> -h (Optional parameter)         :: Displays help message <br>
> -ookla NUM (Optional parameter) :: Set flag to output Ookla JSON, NUM is number of JSON output <br>
> -mlab NUM (Optional parameter)  :: Set flag to output Mlab JSON, NUM is number of JSON output <br>

### Notes

If the `-p` flag is not set, then the data will be output as JSON files in the same directory where the program resides. The following are parameters that are randomized:
- Ookla
    - "TestStartTime"
    - "TestEndTime"
    - "DownloadValue"
    - "UploadValue"
    - "Ping"
    - "BytesSent"
    - "BytesReceived"
- Mlab
    - "TestStartTime"
    - "TestEndTime"
    - "DownloadValue"
    - "UploadValue"
    - "MinRTTValue"

The current local time is used for the generated data, generally `"TestStartTime"` and `"TestEndTime"` will be identical. 
