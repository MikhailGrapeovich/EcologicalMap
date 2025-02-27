from fastapi import HTTPException, status

IncorrectUsernameOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password or username.")
IncorrectPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password.")
SamePasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="New password can`t be the same as the current one.")
UserInactiveException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is inactive.")
UserNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
AuthErrorException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials.")
ErrorNoPrivilegesException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges.")



