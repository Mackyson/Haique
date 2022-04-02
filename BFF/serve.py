from flask import Flask, render_template, request, make_response
from flask.wrappers import Response

import openapi_client
from openapi_client.api import default_api
from openapi_client.models import *

from openapi_client.model.inline_object import InlineObject
from openapi_client.model.inline_response201 import InlineResponse201
import requests as rq
import json

app = Flask(__name__)

configuration = openapi_client.Configuration(
    host = "http://api-server:8080"
)

@app.route("/")
@app.route("/top")
def get_top():
    with openapi_client.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)

        # example, this endpoint has no required or optional parameters
        try:
            # top
            api_response = api_instance.get_top()
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->get_top: %s\n" % e)
            return render_template("error.html",title="error",err=None)

        return render_template('top.html',title='top 30 Haikus', Haikus=api_response)

@app.route("/signup")
def get_signup():
    return render_template('signup.html',title='signup',err="")
@app.route("/signup",methods=["POST"])
def post_signup():
    with openapi_client.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        inline_object = InlineObject(
            name = request.form.get("name"),
            pw = request.form.get("password"),
        ) # InlineObject |  (optional)

        # example passing only required values which don't have defaults set
        # and optional values
        try:
            api_response = api_instance.post_signup(inline_object=inline_object)
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->post_signup: %s\n" % e)
            return render_template('signup.html',title='sign up',err="Already used name...")
        resp = make_response(render_template('signup_done.html',title='signup'))
        resp.set_cookie("session_id",api_response.session_id)
        return resp

@app.route("/signin")
def get_signin():
    return render_template('signin.html',title='signin',err="")
@app.route("/signin",methods=["POST"])
def post_signin():
    with openapi_client.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        inline_object1 = InlineObject1(
            name = request.form.get("name"),
            pw = request.form.get("password"),
        ) # InlineObject1 |  (optional)

        try:
            api_response = api_instance.post_signin(inline_object1=inline_object1)
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->post_signin: %s\n" % e)
            return render_template('signin.html',title='sign in',err="Wrong password or name")
        resp = make_response(render_template('signin_done.html',title='sign in'))
        resp.set_cookie("session_id",api_response.session_id)
        return resp

@app.route("/haiku/<haiku_id_str>")
def get_haiku(haiku_id_str=None):
   with openapi_client.ApiClient(configuration=configuration) as api_client:
       # Create an instance of the API class
       api_instance = default_api.DefaultApi(api_client)
       haiku_id = int(haiku_id_str) # int |

       # example passing only required values which don't have defaults set
       try:
           # get_haiku
           api_response = api_instance.get_haiku(haiku_id)
       except openapi_client.ApiException as e:
           print("Exception when calling DefaultApi->delete_haiku: %s\n" % e)
           resp = make_response(render_template("error.html",title="error",err=e.body))
           return resp

   return render_template('haiku_description.html',title='haiku description', response=api_response)

@app.route("/user/<user_id_str>")
def get_user(user_id_str=None):
   with openapi_client.ApiClient(configuration=configuration) as api_client:
       # Create an instance of the API class
       api_instance = default_api.DefaultApi(api_client)
       user_id = int(user_id_str) # int |

       # example passing only required values which don't have defaults set
       try:
           # user_info
           api_response = api_instance.get_user(user_id)
       except openapi_client.ApiException as e:
           print("Exception when calling DefaultApi->get_user: %s\n" % e)
           resp = make_response(render_template("error.html",title="error",err=e.body))
           return resp

   return render_template('user_description.html',title='user page', User=api_response)

@app.route("/subscribe/<user_id_str>",methods=["POST"])
def post_subscribe(user_id_str=None):
    with openapi_client.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        user_id = int(user_id_str) # int |
        inline_object3 = InlineObject3(
            session_id=request.cookies.get("session_id"),
        ) # InlineObject3 |  (optional)

        # example passing only required values which don't have defaults set
        try:
            api_instance.post_subscribe(user_id, inline_object3=inline_object3)
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->post_subscribe: %s\n" % e)
            return render_template('error.html',title='error',err=e.body)

    return render_template('subscribe_done.html',title='subscribe ok')
@app.route("/unsubscribe/<user_id_str>",methods=["POST"])
def post_unsubscribe(user_id_str=None):
    with openapi_client.ApiClient(configuration=configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        user_id = int(user_id_str) # int |
        inline_object4 = InlineObject4(
            session_id=request.cookies.get("session_id"),
        ) # InlineObject3 |  (optional)

        # example passing only required values which don't have defaults set
        try:
            api_instance.delete_subscribe(user_id, inline_object4=inline_object4)
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->post_subscribe: %s\n" % e)
            return render_template('error.html',title='error',err=e.body)

    return render_template('unsubscribe_done.html',title='subscribe ok')

@app.route("/post-haiku")
def get_post_haiku(): #地獄みたいな名前だが、post-haikuへのGETリクエストを捌くところです
    return render_template('post-haiku.html',title='post haiku',err="")
@app.route("/post-haiku",methods=["POST"])
def post_post_haiku():
    with openapi_client.ApiClient(configuration=configuration) as api_client:
        first=request.form.get("first")
        second=request.form.get("second")
        third=request.form.get("third")
        if  first=="" or second=="" or third=="" :
            return render_template('post-haiku.html',title='post haiku',err="Empty inputs are not allowed")

        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        inline_object2 = InlineObject2(
            session_id=request.cookies.get("session_id"),
            content=ApiPostHaikuContent(
                first=first,
                second=second,
                third=third,
            ),
        ) # InlineObject2 |  (optional)

        try:
            api_instance.post_haiku(inline_object2=inline_object2)
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->post_haiku: %s\n" % e)
            return render_template('error.html',title='error',err=e)
        return render_template('post-haiku_done.html',title='post haiku')

@app.route("/timeline")
def get_timeline():
        # # 以下のコード（Exampleコピペ）で、サーバにinline_object5の中身が全く届いていないので、openAPI generatorのバグを疑っている。
    # with openapi_client.ApiClient(configuration=configuration) as api_client:
    #     # Create an instance of the API class
    #     api_instance = default_api.DefaultApi(api_client)
    #     inline_object5 = InlineObject3(
    #         session_id="session_id_example",
    #     ) # InlineObject5 |  (optional)

    #     # example passing only required values which don't have defaults set
    #     # and optional values
    #     try:
    #         # timeline
    #         api_response = api_instance.get_timeline(inline_object5=inline_object5)
    #     except openapi_client.ApiException as e:
    #         print("Exception when calling DefaultApi->get_timeline: %s\n" % e)
    #         return render_template("session_error.html",title="session error")

    #     return render_template('timeline.html',title='timeline', Haikus=api_response)

    # 仕方がないので、timelineに関してはAd-hocに実装する。
    url = "http://api-server:8080/api/timeline"
    json_data = {"session_id": request.cookies.get("session_id")}
    r = rq.get(url,json=json_data)
    if r.status_code!=200:
        return render_template('error.html',title='error',err=r.text)
    else:
        return render_template('timeline.html',title='timeline', Haikus=r.json())
## おまじない
if __name__ == "__main__":
    app.run(debug=True,port=5000,host="0.0.0.0")
