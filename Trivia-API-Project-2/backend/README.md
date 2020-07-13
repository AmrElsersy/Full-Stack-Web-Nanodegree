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
* GET /reports
- return all the reports that get reported by users
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


* GET /questions/id
- get the data of a specific question
- Request : 127.0.0.1:5000/questions/26
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

* GET /users/<int:id>/questions
- get the questions that asked to the user
- Request : 127.0.0.1:5000/users/25/questions
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


example : 
{
	"content" : "question .... ?",
	"asker_id": 12
}
return {
	
}

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

* GET /
- 
- Request :
``` 

```
- Request Arguments : 
- Response :
``` 

```

* GET /
- 
- Request :
``` 

```
- Request Arguments : 
- Response :
``` 

```




