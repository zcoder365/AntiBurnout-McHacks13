from werkzeug.security import check_password_hash
import model.database.database as db

def verify_user(email, password):
    # find user in database
    user = db.user_by_email(email)
    user_saved_pw = user['password_hash']
    
    # check their password using werkzeug
    if check_password_hash(user_saved_pw, password):
        return True
    else:
        return False