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
