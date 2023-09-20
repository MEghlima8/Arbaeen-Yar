from App import config
from flask import Flask, request, render_template, session
from App.Controller import web_process
from App.Controller import db_postgres_controller as db
from App.Controller.user_controller import Manager, User
import math
from App.Controller.validation import Valid
import csv
import os
import uuid


app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


def get_items_from_offset(page,all_items):
    offset = (page - 1) * 8  # There are 8 requests per page
    items = all_items[offset: offset + 8]
    count_all_pages = math.ceil(len(all_items) / 8) # Get count of all pages: if all_req = 25 then return 3
    return items,count_all_pages


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/edit-user-info', methods=['POST'])
def edit_user_info():
    j_body_data = request.get_json()
    valid = Valid(username=j_body_data['username'], fullname=j_body_data['fullname'],
                  password=j_body_data['password'])
    res_valid = valid.signup(accept_none_val=True)
    
    if res_valid:
        user = User(username=j_body_data['username'], fullname=j_body_data['fullname'],
                    password=j_body_data['password'])
        user.edit_info(j_body_data['uuid'])
        resp = {"result": "User info edited successfully", "status-code":200}
    else:
        resp = {"result": res_valid, "status-code":400}
        
    return resp
        


@app.route('/add-new-user-to-karavan', methods=['POST'])    
def add_new_user_to_karavan():
    try:
        # Save excel file in temp folder
        excel_file = request.files['UsersExcelFile']
        filename = uuid.uuid4().hex + '.csv'
        path = os.path.join(config.configs["UPLOAD_TEMP_FILE"], filename)
        excel_file.save(path)
        
        karavan_uuid = request.form['karavan_uuid']
        res_add_users = []
        status_code = 201   # As default, all users are valid
        
        with open(path, 'r') as file:    
            # Read excel file
            csvreader = csv.reader(file)
            users = []  # Append just valid users
            
            for row in csvreader:
                
                # To check there are three columns
                try:
                    # Validate signup info
                    valid = Valid(row[0], row[1],row[2])  # row[0]:username, row[1]:fullname, row[2]:password
                except:
                    resp = {"result": "need three columns: username, fullname, password", "status-code":422}
                    return resp
                    
                check_user_info = valid.signup()
                
                if check_user_info != True:
                    error = web_process.convert_add_user_error_to_persian(check_user_info)
                    res_add_users.append([row[0], row[1], row[2], error])
                    status_code = 202
                else:
                    users.append([row[0],row[1], row[2]])    # example => ['username', 'fullname', 'password']
                    res_add_users.append([row[0], row[1], row[2], 'ثبت شد'])
        
        # Add status column to excel file to return to user
        with open(path, 'w') as file:
            writer = csv.writer(file)
            for user in res_add_users:
                writer.writerow(user)
                
        for username in users:
            o_user = User(username[1], username[0], username[2])  # Send fullname, username, password
            o_user.signup(karavan_uuid)
        resp = {"result": "Users added successfully", "status-code":status_code, "path_result_excel":path}
        
    except:
        j_body_data = request.get_json()
        fullname = j_body_data['fullname']
        username = j_body_data['username'] 
        password = j_body_data['password'] 
        
        # Validate signup info       
        valid = Valid(username, fullname, password)
        check_user_info = valid.signup()
        
        if check_user_info == True :
            o_user = User(fullname, username, password)
            o_user.signup(j_body_data['karavan_uuid'])
            resp = {"result": "User added successfully", "status-code":201}
        else:
            resp = {"result": check_user_info, "status-code":400}
                    
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


@app.route('/get-karavan-users-info', methods=['POST'])
def get_karavan_users_info():
    j_body_data = request.get_json()
    res = db.db.getAllKaravanUsersInfo(j_body_data['karavan_uuid'], j_body_data['search_value'])

    page_items,count_all_pages = get_items_from_offset(j_body_data['page_index'],res)
    result = {"status-code":200 , "result":page_items,
              "count_pages":count_all_pages, "active_page":j_body_data["karavan_uuid"]
              }
    return result 


@app.route('/get-souvenir-photos', methods=['POST'])
def get_souvenir_photos():
    j_body_data = request.get_json()
    
    res = db.db.getKaravanRequestInfo(j_body_data['karavan_uuid'], '/souvenir-photo', j_body_data['search_value'])
    res = web_process.handleResultByTime(res,j_body_data['time'])
    res = web_process.handleResultByEvent(res,j_body_data['event'])
    
    page_items,count_all_pages = get_items_from_offset(j_body_data['page_index'],res)
    result = {"status-code":200 , "result":page_items,
              "count_pages":count_all_pages, "active_page":j_body_data["karavan_uuid"]
              }
    return result 


@app.route('/get-registered-locations', methods=['POST'])
def get_registered_locations():
    j_body_data = request.get_json()
    res = db.db.getKaravanRequestInfo(j_body_data['karavan_uuid'], '/send-my-location', j_body_data['search_value'])
    res = web_process.handleResultByTime(res,j_body_data['time'])

    if j_body_data['page_index'] =='all':   # Retrieve all, not just one page
        if res == []:
            result = {"status-code":204 , "result":'Without registered location'}
        else:
            result = {"status-code":200 , "result":res}
        return result
        
    page_items,count_all_pages = get_items_from_offset(j_body_data['page_index'],res)
    if page_items == []:
        result = {"status-code":204 , "result":'Without registered location'}
    else:
        result = {"status-code":200 , "result":page_items,
                  "count_pages":count_all_pages, "active_page":j_body_data["karavan_uuid"]
                  }
    return result 


@app.route('/get-user-all-locations', methods=['POST'])
def get_user_all_locations():
    j_body_data = request.get_json()
    res = db.db.getUserLocations(j_body_data['user_uuid'])
    res = web_process.handleResultByTime(res,j_body_data['time'])
    if res == []:
        result = {"status-code":204 , "result":'Without registered location'}
    else:
        result = {"status-code":200 , "result":res}

    return result


# Signin user
@app.route('/signin-manager' ,methods=['POST'])
def signin_manager():
    
    j_body_data = request.get_json()
    s_username = j_body_data['username']
    s_password = j_body_data['password']
    o_manager = Manager(username = s_username , password = s_password)
    o_manager = o_manager.signin()
    
    if o_manager == 'true':
        fullname = db.db.getManagerFullname(s_username)[0]
        session['username'] = s_username
        session['logged_in'] = True
        resp = {"result":"signed in " , "status-code":200, "fullname":fullname}
                
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