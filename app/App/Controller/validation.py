import re 
import Levenshtein
from App.Controller import db_postgres_controller as db


class Valid:
    
    def __init__(self, username=None, fullname=None, password=None):
        self.username = username        
        self.fullname = fullname
        self.password = password
        

    def check_match_info(self):
        user_info = db.db.checkMatchUsernamePassword(self.username,self.password)
        
        if user_info != []:
            return user_info
        return "invalid" # Invalid username or password


    # check whether the username and password are valid
    def signin(self):        
        check_match_info = self.check_match_info()
        return check_match_info


    # Check username is valid or not
    def is_valid_username(self):
        if not self.username :
            return "empty_username" # username is empty
        # Check duplicate username
        check_exist_username = db.db.checkDuplicateUsername(self.username)

        if check_exist_username != None:
            return "duplicate_username"
        if len(self.username) > 20 or len(self.username) < 3:
            return "length_username"  # username length is must be less than 30 letters
        
        username_allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._0123456789")
        if not set(self.username).issubset(username_allowed_chars):
            return "char_username" # username chars is not valid
        return True
    
    
    # Check password is valid or not
    def is_valid_password(self):
        if not self.password :
            return "empty_password"
        
        sim = self.calculate_similarity(self.username , self.password)
        pass_pattern1 = re.compile(r".{8,50}") # The password must be between 8 and 50 characters long
        pass_pattern2 = re.compile(r"[A-Za-z]+") # The password must have english letter(s)
        
        if pass_pattern2.search(self.password) is None or pass_pattern1.fullmatch(self.password) is None:
            return "password_length"
        elif sim >= 75:
            return "used_info_in_password"
        return True

    
    # Used Levenshtein distance to calculate similarity between two strings
    def calculate_similarity(self,string1, string2):
        distance = Levenshtein.distance(string1, string2)
        max_length = max(len(string1), len(string2))
        
        similarity = 1 - (distance / max_length)
        return similarity * 100
    

    def check_fullname_persian(self):
        # Check whether the fullname contains only Persian letters and no numbers
        if re.match(r'^[\u0600-\u06FF\s]+$', self.fullname) and re.search("\d", self.fullname) is None:
            return True
        return "no_valid_fullname"


    # It checks whether the signup info are valid
    def signup(self):    
        check_valid_username = self.is_valid_username()
        if not check_valid_username:
            return check_valid_username
        
        check_valid_fullname = self.check_fullname_persian()
        if not check_valid_fullname :
            return check_valid_fullname
        
        check_valid_password = self.is_valid_password()
        return check_valid_password
        



