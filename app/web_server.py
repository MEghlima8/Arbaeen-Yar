from App import config
from flask import Flask, request, render_template, session
from App.Controller import web_process
from App.Controller import db_postgres_controller as db
from App.Controller.user_controller import Manager, User
import random
import string

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @app.route('/on-click-search-bar-request', methods=['POST'])
# def on_click_search_bar_request():
#     j_body_data = request.get_json()
#     uuid = j_body_data['search_bar_val']
#     return web_process.find_req_for_request(uuid)

# @app.route('/on-click-search-bar-user', methods=['POST'])
# def on_click_search_bar_user():
#     j_body_data = request.get_json()
#     val = j_body_data['search_bar_val']
#     return web_process.find_req_for_user(val)


# @app.route('/get-user-locations', methods = ['POST'])
# def get_user_locations():
#     j_body_data = request.get_json()
#     user_uuid = j_body_data['user_uuid']
#     return web_process.getUserLocations(user_uuid)


@app.route('/add-new-user-to-karavan', methods=['POST'])    
def add_new_user_to_karavan():
    j_body_data = request.get_json()
    user_password = ''.join(random.choice(string.ascii_letters) for _ in range(12))
    o_user = User(j_body_data['fullname'], j_body_data['username'], user_password)
    res_add_user = o_user.signup(session['username'])
    
    # res_add_user = web_process.addNewUserToKaravan(user_fullname, user_username, manager_username)
    if res_add_user['status'] == 'True':
        resp = {"result": "User added successfully", "status-code":201}
    else:
        resp = {"result": res_add_user, "status-code":400}
    print('resp: ',resp)
    return resp

    
@app.route('/add-new-karavan', methods = ['POST'])   
def add_new_karavan():
    j_body_data = request.get_json()
    new_karavan_name = j_body_data['new_karavan_name']
    manager_username = session['username']
    res_add_karavan = web_process.createNewKaravan(new_karavan_name,manager_username)
    if res_add_karavan == 'true':
        resp = {"result": "Karavan created successfully", "status-code":200}
    else:
        resp = {"result": "Invalid name", "status-code":400}
    return resp


@app.route('/get-karavans-name', methods=['POST'])
def get_karavans_name():
    username = session['username']
    manager_uuid = db.db.getUserUUID(username)
    o_manager = db.db.getKaravansInfo(manager_uuid)
    resp = {"result":o_manager , "status-code":200}
    return resp


# Signin user
@app.route('/signin-manager' ,methods=['POST'])
def signin_manager():
    
    j_body_data = request.get_json()
    s_username = j_body_data['username']
    s_password = j_body_data['password']
    o_manager = Manager(username = s_username , password = s_password)
    o_manager = o_manager.signin()
    
    if o_manager == 'true':
        session['username'] = s_username
        session['logged_in'] = True
        resp = {"result":"signed in " , "status-code":200}
                
    elif o_manager == 'invalid':
        resp = {"result":o_manager , "status-code":400}
    return resp

        

# Signup user
@app.route('/signup-manager', methods=['POST'])
def signup_manager():
    # Retrieve data from the body and header
    body_data = request.get_json()
    
    o_manager = Manager(body_data['username'] , body_data['fullname'] , body_data['password'])
    user = o_manager.signup()
    
    if user["status"] == "True":
        res = {"result":"signup was successfully" , "status-code":201 }
    else:
        res = {"result":user["result"] , "status-code":400}
    return res


def main():
    app.run(host=config.configs['HOST'], port=config.configs['PORT'])