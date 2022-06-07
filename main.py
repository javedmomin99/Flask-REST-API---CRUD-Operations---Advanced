#Install POSTMAN API App for Testing the Code :
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

task_dict = {
    1 : {"task" : "Write Hello World Program",
         "summary" : "Write the Code using Python."},
    2: {"task": "Write Flask API Program",
        "summary": "Write the Flask API Code using Python."},
    3:  {"task": "Write REST API Program",
        "summary": "Write the REST API Code using Python."}
}

#To Write a Task to a Server [POST REQUEST] ---> Need a Request Parser --> ReqParse() is Required.

tasks_post_args = reqparse.RequestParser()

tasks_post_args.add_argument("task", type = str, help="Task is required",required = True)
# required = True means It is compulsory to add a task.
# help  means what to accept and expect from user

tasks_post_args.add_argument("summary", type = str,help="Summary is required", required = True)
# required = True means It is compulsory to add a task.
# help  means what to accept and expect from user

# add_argument accepts 2 arguments here "task" & "summary"

tasks_put_args = reqparse.RequestParser()

tasks_put_args.add_argument("task", type = str) #update is optional,so dont require required=True & user knows what to update, so no need of help here.

tasks_put_args.add_argument("summary", type = str) #update is optional,so dont require required=True & user knows what to update, so no need of help here.


class Welcome(Resource):
    def get(self):
        return "Welcome!!"

class ToDoList(Resource):
    def get(self):             #Should Not pass any parameter as below API doesnt have any...
        return task_dict

class ToDO(Resource):
    def get(self, todo_task):
        return task_dict[todo_task]
# Here, it will return api.add_resource(toDO,'/todos/<int:todo_task>')  --->Ex: api.add_resource(toDO,'/todos/1')
# i.e, return task_dict[0]    ---> Return 1st Dictionary
# Here, it will return api.add_resource(toDO,'/todos/<int:todo_task>')  --->Ex: api.add_resource(toDO,'/todos/2')
# i.e, return task_dict[0]    ---> Return 2nd Dictionary
    def post(self, todo_task):
        args = tasks_post_args.parse_args()  #Using Function parse_args for Posting.
        # Check if the task already exists or not:
        if todo_task in task_dict:   #Show an Error if already Task Exist.
            #Since we already have 3 Task Listed, if we try to append task on 1st, 2nd or 3rd, it will throw an error.
            # http: // 127.0.0.1: 5000 / todos / 1  ..Will Throw an Error
            # http: // 127.0.0.1: 5000 / todos / 2  ..Will Throw an Error
            # http: // 127.0.0.1: 5000 / todos / 3  ..Will Throw an Error
            abort(409,message = "Task already Exists.")
        task_dict[todo_task] = {"task":args["task"],"summary":args["summary"]}  #Appending to Dict if Task <int:todo_task> is Not Repeated
        #args["task"] & args["summary"] are used since we are passing a new argument for "tasks" & "summary".
        # In Simple Words, args["task"]  --> New Argument for Task &
        # In Simple Words, args["summary"]  --> New Argument for Summary
        return task_dict[todo_task]
        # Write 'http://127.0.0.1:5000/todos/4' in POSTMAN API App :
        # Go in Body ---> Raw --> Change Text to JSON
        # In the Blank Space, Write your 4th Task, which contains keys as "task" : " " & "summary" : " "
        # Ex : {
        #     "task" : "Learn Python",
        #     "summary" : "Learn Python and its various Libraries."
        # }
        # SELECT "GET" for Posting on Middle Left of App
        # Click on SEND Button on Right
        # Now use GET Method and cross verify the same--> http: // 127.0.0.1: 5000 / todos /

    def put(self,todo_task):
        args = tasks_put_args.parse_args()  #Using Function parse_args for Put.
        if todo_task not in task_dict:   #Show an Error if Task doesn't Exist.
        #Since we already have 3 Task Listed, user can update only 3 for below shown..
        # http: // 127.0.0.1: 5000 / todos / 1  ..Will Not Throw an Error
        # http: // 127.0.0.1: 5000 / todos / 2  ..Will Not Throw an Error
        # http: // 127.0.0.1: 5000 / todos / 3  ..Will Not Throw an Error
            abort(409, message = "Task Doesn't Exists, Cannot Update.")
        if args["task"]:  #Dont Use elif otherwise if we want to change both, it will not execute it.
            task_dict[todo_task]["task"] = args["task"] # Ex : task_dict[todo_task]["task"]---> In task_dict[1]["task"] --> Update the new task as new argumented "task" for the specified index number, thats why used args["task"]
        if args["summary"]:  #Dont Use elif otherwise if we want to change both, it will not execute it.
            task_dict[todo_task]["summary"] = args["summary"]  # Ex : task_dict[todo_task]["summary"]---> In task_dict[1]["summary"] --> Update the new summary as new argumented "summary" for the specified index number, thats why used args["summary"]
        return task_dict[todo_task]    #Ex :task_dict[todo_task]-->task_dict[1]..This it will return, i.e., Updated Data.
    #SELECT http://127.0.0.1:5000/todos/<int:todo_task>, Ex : http://127.0.0.1:5000/todos/1 which you want to update
    #Select PUT in Postman API
    #Click on Send Request

    def delete(self, todo_task):
        if todo_task in task_dict:
            del task_dict[todo_task]  #del fuction is used for deleting
            return task_dict
        else:
            abort(409, message="Task Doesn't Exists, Cannot Delete.")
    #SELECT http://127.0.0.1:5000/todos/<int:todo_task>, Ex : http://127.0.0.1:5000/todos/4 which you want to delete
    #Select Delete in Postman API
    #Click on Send Request

api.add_resource(Welcome,'/')

api.add_resource(ToDoList,'/todos/')  #Should Not pass any parameter in toDO_List class as this doesnt have any...

api.add_resource(ToDO,'/todos/<int:todo_task>')  #Class defined should always contain the same name. Here, <int:todo_task>'---> todo_task is the parameter which we call.

if __name__ == "__main__":
    app.run(debug=True)

# Youtube Video for Reference - Building a RESTFUL API with Python and Flask
# Youtuber --> Programming Knowledge
# Run Via Terminal Directly --> Terminal --> python main.py
