import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import httpx
import jwt
from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel, ValidationError

# JWT 설정
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# GitHub OAuth2 설정
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "your_github_client_id")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "your_github_client_secret")
GITHUB_REDIRECT_URI = os.getenv(
    "GITHUB_REDIRECT_URI", "http://localhost:8000/auth/callback"
)
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"

# GitHub 사용자 정보를 저장하는 간단한 DB (실제로는 데이터베이스 사용 권장)
users_db = {}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    name: str | None = None
    avatar_url: str | None = None
    github_id: int | None = None


class GitHubUser(BaseModel):
    login: str
    id: int
    email: str | None = None
    name: str | None = None
    avatar_url: str | None = None


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=GITHUB_AUTHORIZE_URL,
    tokenUrl="/auth/callback",
)

app = FastAPI(swagger_ui_oauth2_redirect_url="/auth/callback")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def exchangeGithubCode(code: str) -> str:
    """GitHub authorization code를 access token으로 교환"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
        )
        data = response.json()
        if "access_token" not in data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get access token from GitHub",
            )
        return data["access_token"]


async def getGithubUser(access_token: str) -> GitHubUser:
    """GitHub access token으로 사용자 정보 가져오기"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GITHUB_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to get user info from GitHub",
            )
        user_data = response.json()
        return GitHubUser(**user_data)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (jwt.InvalidTokenError, ValidationError):
        raise credentials_exception

    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/auth/callback")
async def authCallback(code: Annotated[str, Form()]):
    """GitHub OAuth2 콜백 - authorization code를 받아서 JWT 토큰 생성"""
    try:
        # GitHub access token 획득
        github_access_token = await exchangeGithubCode(code)

        # GitHub 사용자 정보 가져오기
        github_user = await getGithubUser(github_access_token)

        # 사용자 정보를 DB에 저장 (또는 업데이트)
        user = User(
            username=github_user.login,
            email=github_user.email,
            name=github_user.name,
            avatar_url=github_user.avatar_url,
            github_id=github_user.id,
        )
        users_db[github_user.login] = user.model_dump()

        # JWT 토큰 생성
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": github_user.login},
            expires_delta=access_token_expires,
        )

        return Token(access_token=access_token, token_type="bearer")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}",
        )


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/status/")
async def read_system_status():
    return {"status": "ok"}
