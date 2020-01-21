# StudentActions
Before using any of these functions it is expected a user already called addUser and addUserCPIs.
## AddUser
 The AddUser GET request adds users to the database it is most likely called first from the frontend.

## addUserCPIs
  The addUserCPIs POST request adds all the CPI's from the user calling it. The function expects a json body with the parameter: courseId e.g:
```
{
    "courseId" : "4998"
}
```

## requestStudentExperts

The requestStudentExperts POST request adds a record to the database with the CPI where was clicked by the user. The button is now manually added using a TamperMonkey script located at: https://github.com/Nudge-Crew/TamperMonkeyScript
  
## getStudentExpertRequest

The getStudentExpertRequests GET request gets the students experts requests and returns this.

# Working with gcloud

In this project the gcloud package is used in the terminal.

## Adding a function

To add a function create a new file in app/functions, in this file create a function. In main.py import this new function and comment the other functions(only the uncommented will be uploaded to gcloud). If you want to be able to test it locally also add it to the dev.py functions array. 

## Uploading/updating a function

To upload a function to gcloud make use the following command:
```
gcloud functions deploy <function name> --runtime python37 --trigger-http --project nudge-crew --set-env-vars DATABASE_URI="dbname=postgres user=postgres password=<db password> host=/cloudsql/nudge-crew:europe-west4:hizmet" --region europe-west1

```
Make sure that the function you want to upload is uncommented in main.py
