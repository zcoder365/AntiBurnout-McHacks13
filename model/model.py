import bcrypt
import model.database.database as db

def verify_user(email, password):
    # find user in database
    user = db.user_by_email(email)
    user_saved_pw = user['password']
    
    # check their password
    if bcrypt.checkpw(password.encode('utf-8'), user_saved_pw.encode('utf-8')):
        return True
    else:
        return False