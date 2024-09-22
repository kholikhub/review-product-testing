from functools import wraps
from flask_login import current_user

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(current_user.role,role)
            if current_user.is_authenticated and current_user.role == role:
                return func(*args, **kwargs)
            else:
                return { "message": "Unauthorized" }, 403
            
            # Case 2 : Admin has more power than User
            # Role yg login Admin, dia bisa akses semua
            
            # if current_user.is_authenticated and role == 'Admin' and current_user.role == 'Admin':
            #     return func(*args, **kwargs)
            # elif current_user.is_authenticated and current_user.role == 'Admin' and role == 'User':
            #     return func(*args, **kwargs)
            # # Role yg akses User, kalo require User, dia lolos
            # elif current_user.is_authenticated and role == 'User' and current_user.role == 'User':
            #     return func(*args, **kwargs)
            # # Role yg akses User, kalo require Admin, dia gagal
            # else:
            #     return { "message": "Unauthorized" }, 403
        return wrapper
    return decorator