from fastapi import APIRouter , HTTPException , Depends , BackgroundTasks
from pydantic import EmailStr

#file imports
from app.schemas.user import UserRegister , LoginUserRequest , LoginUserResponse , ChangePassword , UserUpdate, RefreshTokenRequest
from app.services.user import UserServices 
from app.models.role import Role
from beanie import PydanticObjectId
from app.services.email import Mail
from app.models.user import User
from app.utils.deps import get_current_user

router = APIRouter(
    prefix="/api/auth",
    tags =['Authentication']
)


@router.post("/register")
async def register(user_data : UserRegister , background_tasks: BackgroundTasks):
    try :
        new_user =  await UserServices.register(user_data  , background_tasks)

        return {
            "message" : "user created successfully",
            "details" : new_user
        }
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/login" , response_model=LoginUserResponse)
async def login_user(request : LoginUserRequest):
    try:
        token = await UserServices.user_login(
            request.email,
            request.password
        )

        if not token:
            raise HTTPException(
                status_code= 401,
                detail="invalid email or password (access token)"
            )
        
        return LoginUserResponse(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            token_type= "bearer"
        )
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):

    try:
        result = await UserServices.refresh_token(request.refresh_token)

        return result

    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.delete("/log-out")
async def logout_user(current_user : User = Depends(get_current_user)):
    try:
        return await UserServices.logout(str(current_user.id))
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/send-otp")
async def send_otp(email : EmailStr , backgroundtask : BackgroundTasks):
    try:
        replacements , emailData = await UserServices.send_otp(email=email , type=None)

        if not replacements and not emailData:
            raise HTTPException(
                status_code = 404,
                detail="Data not found"           
            )
        backgroundtask.add_task(Mail , emailData , replacements , "sendotp.html")

        return {
            "message" : "OTP Sent !!!",
            "email" : email
        }
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/forget-password")
async def forget_password(email : EmailStr , backgroundtask : BackgroundTasks):
    try:

        replacements , emailData = await UserServices.send_otp(email , type="forget_password")

        if not replacements and not emailData:
            raise HTTPException(status_code=404, detail="Data not found")
        
        backgroundtask.add_task(Mail , emailData , replacements , "email.html")

        return {
            "message" : "Forget OTP Sent on you email Please check !!!",
            "email" : email
        }
        
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/reset-password")
async def reset_password(email : EmailStr  , otp : str , password : str):
    try:
        return await UserServices.reset_password(email ,  otp , password)
    
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/change-password")
async def change_password( user_data : ChangePassword, current_user : User = Depends(get_current_user)):
    try:
        return await UserServices.change_password(user_data.userId ,user_data.old_password , user_data.new_password , current_user)
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/send-verify-email-otp")
async def sent_verify_otp(email : EmailStr , backgroundtask : BackgroundTasks):
    try:
        replacements , emailData = await UserServices.send_otp(email , type="email_verify")

        if not replacements and not emailData:
            raise HTTPException(status_code=404, detail="Data not found")
        
        backgroundtask.add_task(Mail , emailData , replacements , "email.html")

        return {
            "message" : "verify Email OTP Sent on you email Please check !!!",
            "email" : email
        }
        
    
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/verified-email")
async def verify_email( email : EmailStr , otp : str):
    try:
        return await UserServices.verify_email(email , otp)
    except HTTPException:
        raise
    except Exception as e :
        print(f"failed to respones : {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.get("/profile")
async def profile_user(current_user : User = Depends(get_current_user)):
    try:
        user_dict = current_user.model_dump()
        user_dict["id"] = str(current_user.id)
        
        fname = user_dict.get("fname") or ""
        lname = user_dict.get("lname") or ""
        user_dict["name"] = f"{fname} {lname}".strip() or user_dict.get("email")
        
        role_id = user_dict.get("roleId")
        if role_id:
            try:
                role = await Role.get(PydanticObjectId(role_id))
                if role:
                    user_dict["role"] = role.name
            except Exception:
                pass
                
        return user_dict
    except HTTPException:
        raise
    except Exception as e:
        raise

@router.put("/profile-update")
async def profile_update( user_data : UserUpdate , current_user : User = Depends(get_current_user)):
    try:
        return await UserServices.profile_update(user_data , current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise  

