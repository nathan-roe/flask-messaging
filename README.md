# Flask Messaging

This is a messaging API written using Python, Flask, SQLAlchemy and Flask-RESTful.

### Endpoints

> **Auth**
> - Sign Up:
>     - Used to create a UserProfile instance as well as handles password hashing, account verification emailing, and related token creation.
>         - Request Type: POST
>         - Expected POST Data:
>         ```json
>         {
>             "name_first": "str",
>             "name_last": "str",
>             "email": "str",
>             "password": "str"
>         }
>         ```
>         - Endpoint: ```/```
> - Verify Email:
>     - Used to verify an email through token authentication.
>         - Request Type: POST
>         ```json
>         {
>             "token": "str"
>         }
>         ```
>         - Endpoint: ```/verify-email```
> - Resend Email:
>     - Used to resend the email used for token authentication.
>         - Request Type: POST
>         - Expected POST Data:
>         ```json
>         {
>             "email": "str"
>         }
>         ```
>         - Endpoint: ```/resend-email```
> - Sign In:
>     - Used to sign in a user given a valid email and password.
>         - Request Type: POST
>         - Expected POST Data:
>         ```json
>         {
>             "email": "str",
>             "password": "str"
>         }
>         ```
>         - Endpoint: ```/signin```

> **Messaging**
> - Send Message Request:
>     - Used to send a message request from the current user to a specified contact based on user id. Creates a UserMessageRelationship instance used to store and handle messages.
>         - Request Type: POST
>         - Expected POST Data:
>         ```json
>         {}
>         ```
>         - Endpoint: ```/messages/request/<int:id>```
> - Accept Message Request:
>     - Used to accept a message request and updates the UserMessageRelationship ```status``` field to ```CONNECTED```
>         - Request Type: POST
>         - Expected POST Data:
>         ```json
>         {}
>         ```
>         - Endpoint: ```/messages/accept/<int:id>```
> - Decline Message Request:
>     - Used to decline a message request and updates the UserMessageRelationship ```status``` field to ```DECLINED```
>         - Request Type: POST
>         - Expected POST Data:
>         ```json
>         {}
>         ```
>         - Endpoint: ```/messages/decline/<int:id>```
> - Send Message:
>     - Used to send a message to a specified contact with a UserMessageRelationship status of ```CONNECTED```.
>         - Request Type: POST
>         - Expected POST Data:
>         ```json
>         {
>         "message": "str"
>         }
>         ```
>         - Endpoint: ```/messages/<int:id>```
> - Get Messages By Group:
>     - Used to retrieve messages specific to a UserMessageRelationship instance and queried using the related contacts UserProfile id.
>         - Request Type: GET
>         - Endpoint: ```/messages/<int:id>```
> - Get Related Message Groups:
>     - Used to retrieve UserMessageRelationship instances relavent to the current user's UserProfile.
>         - Request Type: GET
>         - Endpoint: ```/messages/groups```

--- 

### Interacting with the API

The Postman collection used to call the API has been included in the project directory, and can be imported to interact with the API with minimal setup.

The following code is used within the Sign In endpoint's test to automatically update/set an ```auth_token``` environment variable that is used within the Postman collection:
```javascript
pm.environment.set('auth_token', pm.response.json().token)
pm.test(pm.environment.get('auth_token'))
```