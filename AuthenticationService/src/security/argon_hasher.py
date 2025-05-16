from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class ArgonHasher:
    def __init__(self, ph: PasswordHasher = PasswordHasher()) -> None:
        self.ph = ph

    async def hash_password(self,
                            password: str,
        ) -> str:
        return self.ph.hash(password=password)

    async def verify_password(self,
                              plain_password: str,
                              hashed_password: str,
        ) -> bool:
        try:
            return self.ph.verify(password=plain_password, hash=hashed_password)
        except VerifyMismatchError:
            raise ValueError
