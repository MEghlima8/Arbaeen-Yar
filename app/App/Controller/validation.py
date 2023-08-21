import re

def check_fullname_persian(fullname):
    # Check whether the fullname contains only Persian letters and no numbers
    if re.match(r'^[\u0600-\u06FF\s]+$', fullname) and re.search("\d", fullname) is None:
        return True
    return False
