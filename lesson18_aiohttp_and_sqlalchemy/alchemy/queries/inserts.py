import dataclasses
import logging
import sys

import sqlalchemy.exc
from models.user_models import User
from sqlalchemy import select

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)


formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d %(levelname)s [%(name)s:%(funcName)s:%(lineno)s] "
    "%(processName)s[%(threadName)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(hdlr=handler)
logger.setLevel(level="DEBUG")


@dataclasses.dataclass
class InsertSuccess:
    created_user_id: int
    message: str


@dataclasses.dataclass
class InsertConflict:
    persisted_user: User
    message: str


@dataclasses.dataclass
class InsertResult:
    success: InsertSuccess | None = None
    conflict: InsertConflict | None = None


async def insert_new_user(session, new_user: User) -> InsertResult:
    """
    SQLAlchemy provides functionality to INSERT new data
    without executing INSERT query directly, but via the
    'unit of work' pattern: Instance of Mapped class can
    be attached to the current Session via 'add() / add_all() '
    Session's methods, then the data should be flushed
    (automatically, if *session.autoflush = True* OR there is a need to call of
    *session.flush()* directly.
    After this, the data will be INSERTED into the appropriate DB table

    """
    user_info = f"User(name={new_user.name}, age={new_user.age})"

    async with session:
        # start new Transaction using 'begin()' context manager
        # to avoid making 'commit / rollback' directly later
        async with session.begin():
            try:
                # create SAVEPOINT for Transaction
                async with session.begin_nested():
                    session.add(new_user)
                    result = InsertResult(
                        success=InsertSuccess(
                            created_user_id=new_user.id,
                            message=f"{user_info} successfully created!",
                        )
                    )
            except sqlalchemy.exc.IntegrityError:
                # Transaction state will be ROLLED BACK to the SAVEPOINT
                logger.debug(
                    f"User(name={new_user.name}, age={new_user.age}) " f"already exist!"
                )

                persisted_user = await session.execute(
                    select(User).where(
                        User.name == new_user.name, User.age == new_user.age
                    )
                )
                result = InsertResult(
                    conflict=InsertConflict(
                        persisted_user=persisted_user,
                        message=f"{user_info} already exist!",
                    )
                )

        return result
