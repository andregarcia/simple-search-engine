from src.analyzer import create_analyzer_chain
from src.index import Index, Fields, Field


class IndexSingleton:

    __INSTANCE = None

    @classmethod
    def get_instance(cls) -> Index:
        if not cls.__INSTANCE:
            fields = ['main',
                      'id']
            field_objects = [Field(field_name, create_analyzer_chain()) for field_name in fields]
            cls.__INSTANCE = Index(Fields(field_objects))
        return cls.__INSTANCE
