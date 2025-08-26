from .models import User_info

def user_info_processor(request):
    if request.user.is_authenticated:
        try:
            return {"user_info": User_info.objects.get(user= request.user)}
        except User_info.DoesNotExist:
            return {"user_info": None}
        
    return {"user_info": None}