# CS 467 Capstone Project
**Authors:** Jada Young, Eric Riemer, Robert Behring

Initialize required packages using:  
```$ pip install -r requirements.txt```

## GCP Functions Usage
These are instructions for using the custom GCP client library functions [gcp_storage]  
### Authenticate Google Cloud Client Libraries for Local Dev Environments

1. Install and initialize the Google Cloud CLI
    - Instructions: https://cloud.google.com/sdk/docs/install  

2. Create a credential file by entering the following command:  
`gcloud auth application-default login`  
Your browser will open and promt you to login. The system then saves a credential file on your system. Please note the file path in case in needed in the future. 

3. The client libraries and ADC will recognize the location of the credential file and use this to authenticate access to services. If the system has issues recognizing where the file is located, you may also place the file path of the credential file in the .env variable `GOOGLE_APPLICATION_CREDENTIALS` [See Environment Variables].


More about Application Default Credentials: https://cloud.google.com/docs/authentication/application-default-credentials#personal  
  
  Source: https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev



### Environment Variables (TBD)
The following .env file structure should be used:
```
# GCP variables
GOOGLE_APPLICATION_CREDENTIALS=my-app-credentials
GCP_PROJECT_ID=my-project-id
SERVICE_ACCOUNT_FILE=path/to/serviceAccountCredentials
STORAGE_BUCKET_NAME=my_storage_bucket_name
```

### Sample Usage
```python
# Load bucket_name env variable
STORAGE_BUCKET_NAME = os.getenv("STORAGE_BUCKET_NAME")
# Initialize GCP storage client
storage = GCPStorage()

# Prints the name of all buckets
storage.print_buckets()
# Prints the name of objects stored in the bucket 
storage.view_a_bucket(STORAGE_BUCKET_NAME)
# Uploads a given file to a given bucket
storage.upload_to_bucket(STORAGE_BUCKET_NAME, "random_ookla_1000.json")
```


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
    - "MinRTValue"

The current local time is used for the generated data, generally `"TestStartTime"` and `"TestEndTime"` will be identical. 
