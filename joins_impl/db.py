from dataclasses import dataclass
import enum
from typing import Any, Iterator, TypeVar
from pydantic import BaseModel
from frozendict import frozendict

class TableName(str, enum):
    BOOK = 'books'
    PUBLISHER = 'publishers'

class JoinType(str, enum):
    INNER = 'inner'
    LEFT = 'left'
    RIGHT = 'right'


class DBRecord(BaseModel):

    @classmethod
    def new(cls, **fields):
        return cls(**fields)


class PublisherRecord(DBRecord):
    id: int
    name: str


class BookRecord(DBRecord):
    id: int
    name: str
    price: float
    publisher_id: int


_TRecord = BookRecord | PublisherRecord
_TMappingData = TypeVar(
    '_TMappingData',
    bound=tuple[
        _TRecord,
        list[_TRecord],
        Iterator[int, None, None]
    ]
)


class DataBase:

    def __init__(self):
        self._books_table: list[BookRecord] = []
        self._publishers_table: list[PublisherRecord] = []
        self._books_id_seq = iter(range(1, 1_000_000))
        self._publishers_id_seq = iter(range(1, 1_000_000))
        self._adjacency_map = frozendict(
            {
                TableName.BOOK: (BookRecord, self._books_table, self._books_id_seq),
                TableName.PUBLISHER: (PublisherRecord, self._publishers_table, self._publishers_id_seq)
            }
        )

    def _get_mapping(self, tb_name: TableName) -> _TMappingData:
        if not (mapping := self._adjacency_map.get(tb_name)):
            raise ValueError(f'Invalid mapping for {tb_name}')

        return mapping

    def create(self, table_name: TableName, **fields):
        record_type, table, table_seq = self._get_mapping(table_name)
        if 'id' not in fields:
            fields['id'] = next(table_seq)
        record = record_type.new(**fields)
        table.append(record)

    def select(self, *table_names, **kwargs):
        tables_cnt = len(table_names)
        if tables_cnt <= 0 or tables_cnt > 2:
            raise ValueError(
                "Tables count must be 1 or 2, not more, not less"
            )

        if tables_cnt == 1:
            return self._select_from_one(table_names[0])

        left, right = table_names
        join_type = kwargs.get('join_type') or JoinType.INNER

        return self._select_with_join(left, right, join_type=join_type)

    def _select_from_one(self, table_name: TableName):
        _, table, _ = self._get_mapping(table_name)

        return [item.dict() for item in table]

    def _select_with_join(self, left: TableName, right: TableName, join_type: JoinType):
        match join_type:
            case JoinType.INNER:
                return self._join_inner(left, right)
            case JoinType.LEFT:
                return self._join_outer(left, right)
            case JoinType.RIGHT:
                return self._join_outer(right, left)

    # def _join_inner(self, left: TableName, right: TableName):
    #     _, left_tb, _ = self._get_mapping(left)
    #     _, right_tb, _ = self._get_mapping(right)
    #
    #     result = []
    #     for i in left:
    #         for j in right:
    #             if i.



    def _join_outer(self, left: TableName, right: TableName):
        pass