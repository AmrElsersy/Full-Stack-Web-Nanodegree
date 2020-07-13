# Asky Website
#### Asky Project is a Question Based Website 
#### that allow people to ask each other questions and follow other users and report bad questions.
#### like ask-fm

## Getting Started
* Base URL : this app can be run localy with base URL http://127.0.0.1:5000/ 
## Error Handling
* Sample 
```
      "success" : False,
      "error" : 404,
      "message" : "Error Not Found"
```
* Error types
- 404 Unfound 
- 400 Bad Request
- 422 Not Proceesable
- 401 Not Authenticated
- 403 Not Authorized


## Endpoits
### Note : All categories requires Access Token
### Tokens :
### All endpoints is tested on Postman
####


* GET /questions/<id>
- get the data of a specific question
- Request : GET 127.0.0.1:5000/questions/26
``` 
```
- Request Arguments : None
- Response :
``` 
{
    "question": {
        "answer": " a computer engineer student",
        "content": "how are you sersy? ",
        "id": 26,
        "is_answered": false,
        "reacts": 3,
        "user_id": 25
    }
}
```

* DELETE /questions/<id>
- get the data of a specific question
- Request : DELETE 127.0.0.1:5000/questions/33
- Response :
``` 
{
	"success": True
}
```

* PATCH /questions/<id>
- get the data of a specific question
- Request : PATCH 127.0.0.1:5000/questions/26
```
{
	"answer" : "answer to question",
	"reacts" : 3
}
```
- Response :
``` 
{
"success": True,
"question": {
        "answer": " answer to question",
        "content": "how are you sersy? ",
        "id": 26,
        "is_answered": false,
        "reacts": 3,
        "user_id": 25
    }
}
```

* GET /questions/<int:id>/replys
- get the replys of the question ( reply is another question but is a child of queistion with <id>)
- Request : GET 127.0.0.1:5000/questions/100/replys
- Request Arguments : 
- Response :
``` 
{
    "reply": [
        {
            "answer": null,
            "content": "test_reply",
            "id": 42,
            "is_answered": false,
            "reacts": 0,
            "user_id": 25
        }
    ],
    "success": true
}
```

* POST /questions/<int:id>/replys
- add another question as a reply (continue asking) to that question (like in ask-fm)
- Request : POST 127.0.0.1:5000/questions/100/replys
- Request Arguments : reply:string contains the question reply, asker_id is the id of the user that is asking
```
{
	"reply" : "continue asking... reply ???",
	"asker_id" : 101
}
```
- Response : id : is the id of the added reply question
``` 
{
    "id": 153,
    "success": true
}
```



===================================
* GET /users/<int:id>
- get the user info like name, picture
- Request : GET 127.0.0.1:5000/users/28
- Request Arguments :  None
- Response :
``` 
{
    "questions": [],
    "success": true,
    "user": {
        "id": 28,
        "name": "sersy",
        "picture": null
    }
}
```

* PATCH /users/<int:id>
- get the user info like name, picture
- Request : PATCH 127.0.0.1:5000/users/28
- Request Arguments :  
```
{
	"name" : "mahmoud sersy",
	"picture": "link to his picture"
}
```
- Response :
``` 
{
    "success": true,
    "user": {
        "id": 28,
	"name" : "mahmoud sersy",
	"picture": "link to his picture"
    }
}
```

* GET users/<int:id>/asked_questions
- get the questions that the user asked
- Request : GET 127.0.0.1:5000/users/28/asked_questions
- Response :
``` 
{
	"questions": [
		{
			"content": "test question",
			"answer": "test answer",
			"user_id": 25
			"id" : 100
			"reacts" : 3
		}
	]
}
```



* GET /users/<int:id>/questions
- get the questions that asked to the user
- Request : GET 127.0.0.1:5000/users/25/questions
- Response 
```
{
    "questions": [
        {
            "answer": null,
            "content": "test_reply",
            "id": 42,
            "is_answered": false,
            "reacts": 0,
            "user_id": 25
        },
        {
            "answer": " a computer engineer student",
            "content": "how are you sersy? ",
            "id": 26,
            "is_answered": false,
            "reacts": 3,
            "user_id": 25
        },
        {
            "answer": null,
            "content": "hey amr , iam user_not ray2, how are you ?",
            "id": 33,
            "is_answered": false,
            "reacts": 0,
            "user_id": 25
        },
        {
            "answer": "test_answer",
            "content": "test_question",
            "id": 100,
            "is_answered": true,
            "reacts": 3,
            "user_id": 25
        },
        {
            "answer": null,
            "content": "is that project excellent or very goog ?",
            "id": 28,
            "is_answered": false,
            "reacts": 0,
            "user_id": 25
        }
    ],
    "success": true
}
```


* POST /users/<int:id>/questions
- ask question to the user
- Request : POST 127.0.0.1:5000/users/28/questions
``` 
{
	"id": 28,
	"question": "question body ???"
}
```
- Response : id : 300 is a random number represents the id is created in db and attatched to that question
``` 
{
	"success" : True,
	"id" 300
}
```


* GET /users/<int:id>/followers
- get the followers that the user with <id> follows
- Request : GET 127.0.0.1:5000/users/28/followers
- Response :
```
{
	"followers" : [
		{
			"id": 25,
			"name": "amr"
		}	
	]
}
```

* POST users/<id>/followers 
- make user of <id> (specified in the url) to follow a user with id (specified in json body)
- Request : POST users/100/followers
``` 
{"id" : 100}
```
- Response :
``` 
{
	"followed": 100,
	"success": True
}
```


=========================================

* GET /reports
- return all the reports that get reported by users (only for admin)
- Request : GET 127.0.0.1:5000/reports
``` 
```
- Response :
``` 
{
    "reports": [
        {
            "id": 7,
            "question_id": 33,
            "user_id": 25
        },
        {
            "id": 100,
            "question_id": 100,
            "user_id": 100
        }
    ],
    "success": true
}
```

* POST /reports 
- report a bad question to the admin (only for user)
- Request : POST 127.0.0.1:5000/reports
``` 
{
	"user_id": 25,
	"question_id": 42
}
```
- Response :
``` 
{
    "report": {
        "id": 41,
        "question_id": 42,
        "user_id": 25
    },
    "success": true
}
```



* GET /reports/<int:id>
- return a specific report that get reported by users (only for admin)
- Request : GET 127.0.0.1:5000/reports/7
- Response :
``` 
{
    "report":
        {
            "id": 7,
            "question_id": 33,
            "user_id": 25
        },
    "success": true
}
```

* DELETE /reports/<int:id>
- Delete a report (only for admin)
- Request : DELETE 127.0.0.1:5000/reports/200
- Response :
``` 
{
	"deleted_report": 200,
	"success": true
}
```



