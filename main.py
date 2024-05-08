import datetime
from typing import Optional

import pydantic


class Item(pydantic.BaseModel):
    item_id: int
    name: Optional[str] = "Jane Doe"
    created_date: datetime.datetime
    pages_visited: list[int]
    price: float


def main():
    data = {"item_id": 1,
            "name": "Karthik",
            "created_date": "2021-01-01T00:00:00",
            "pages_visited": [1, 2, 3],
            "price": 10.0}

    item = Item(**data)
    print(item)

if __name__ == '__main__':
    main()
