from models.user import User

# why argon?
# https://research.redhat.com/blog/article/how-expensive-is-it-to-crack-a-password-derived-with-argon2-very/
from passlib.handlers.argon2 import argon2 as crypto

crypto.default_rounds = 25 # about 225 ms to work

async def user_count() -> int:
    return await User.count()


async def user_by_email(email):
    email = email.lower().strip()
    return await User.find_one(User.email == email)


async def create_user(name, email, password, profile_image_url, location):
    email = email.lower().strip()
    name = name.strip()
    password = password.strip()


    existing_user = user_by_email(email)
    if await existing_user:
        raise Exception("User already Exists")

    hash_password = crypto.encrypt(password)

    # if crypto.verify(password, user.hash_password) check password

    user = User(name=name, email=email, hash_password=hash_password, profile_image_url=profile_image_url, location=location)

    await user.save()
    return user