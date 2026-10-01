"""Professional Python module demonstrating best practices."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Final

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger: Final = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class User:
    """Represents a user with validation."""

    name: str
    email: str
    age: int = field(default=0)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Name must not be empty.")
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email!r}")
        if self.age < 0:
            raise ValueError("Age must be non-negative.")

    @property
    def is_adult(self) -> bool:
        return self.age >= 18

    def greet(self) -> str:
        return f"Hello, {self.name}!"


class UserService:
    """In-memory user store with CRUD operations."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def add(self, user: User) -> None:
        if user.email in self._users:
            raise ValueError(f"User already exists: {user.email}")
        self._users[user.email] = user
        logger.info("Added user: %s", user.name)

    def get(self, email: str) -> User | None:
        return self._users.get(email)

    def remove(self, email: str) -> bool:
        removed = self._users.pop(email, None) is not None
        if removed:
            logger.info("Removed user with email: %s", email)
        return removed

    def list_all(self) -> list[User]:
        return list(self._users.values())

    def __len__(self) -> int:
        return len(self._users)


def main() -> None:
    service = UserService()

    alice = User(name="Alice", email="alice@example.com", age=30)
    bob = User(name="Bob", email="bob@example.com", age=17)

    service.add(alice)
    service.add(bob)

    for user in service.list_all():
        status = "adult" if user.is_adult else "minor"
        logger.info("%s is %s | %s", user.name, status, user.greet())

    logger.info("Total users: %d", len(service))


if __name__ == "__main__":
    main()
