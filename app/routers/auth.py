from fastapi import APIRouter , HTTPException , status

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/register" , 
            status_code=status.HTTP_201_CREATED )
async def  register(
    username : str ,
    password : str
):
    try:
        return {
            "username" : username,
            "password"  : password
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Failed to response : {str(e)}")
        raise HTTPException(status_code=500 ,
                            detail="Internal Server Error")


