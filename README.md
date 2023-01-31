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
