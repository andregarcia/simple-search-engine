from collections import defaultdict
from typing import List, Set


class Field:

    def __init__(self, name: str, index_analyzer, query_analyzer=None):
        self.name = name
        self.index_analyzer = index_analyzer
        self.query_analyzer = query_analyzer or index_analyzer


class Fields:

    def __init__(self, fields: List[Field]):
        self.d = dict([(x.name, x) for x in fields])

    def get(self, name):
        return self.d.get(name)


class DocumentId:

    def __init__(self, id):
        self.id = id

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, DocumentId):
            return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)



class Document:

    def __init__(self, id, doc):
        self.id = id if isinstance(id, DocumentId) else DocumentId(id)
        self.doc = doc

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Document):
            return self.id == other.id
        elif isinstance(other, DocumentId):
            return self.id == other
        else:
            return self.id == DocumentId(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def get_hash(id):
        return hash(id)


class IndexDocumentIds:

    def __init__(self, document_ids: Set[DocumentId] = None):
        self.document_ids = document_ids or set()

    def add(self, document_id: DocumentId):
        self.document_ids.add(document_id)

    def and_operator(self, other):
        return IndexDocumentIds(self.document_ids.intersection(other.document_ids))

    def __contains__(self, document_id: DocumentId):
        return document_id in self.document_ids

    def __len__(self):
        return len(self.document_ids)

    def __iter__(self):
        return self.document_ids.__iter__()


class IndexDocuments:

    def __init__(self):
        self.documents = {}

    def add(self, document: Document):
        self.documents[document.id] = document

    def get(self, id: DocumentId):
        return self.documents.get(id)

    def get_many(self, document_ids: IndexDocumentIds):
        result = []
        for document_id in document_ids:
            doc = self.get(document_id)
            if doc:
                result.append(doc)
        return result

    def __contains__(self, document: Document):
        return document.id in self.documents

    def __len__(self):
        return len(self.documents)


class IndexTokenDocumentIdsMappings:

    def __init__(self):
        self.d = defaultdict(lambda: IndexDocumentIds())

    def get(self, token):
        return self.d.get(token)

    def add(self, tokens, document: Document):
        for token in tokens:
            index_documents = self.d[token]
            index_documents.add(document.id)


class Index:

    def __init__(self, fields: Fields):
        self.fields = fields
        self.index = defaultdict(lambda: IndexTokenDocumentIdsMappings()) # mapping: field -> IndexTokenDocumentsMappings
        self.documents = IndexDocuments()

    def index_one(self, document: Document):
        for field, field_value in document.doc.items():
            field = self.fields.get(field)
            if field:
                index_token_documents_mapping = self.index[field.name]
                index_analyzer = field.index_analyzer
                tokens = index_analyzer.apply(field_value)
                index_token_documents_mapping.add(tokens, document)
        self.documents.add(document)

    def index_many(self, documents: List[Document]):
        for document in documents:
            self.index_one(document)

    def search(self, field_name, text, size) -> List:
        field = self.fields.get(field_name)
        if field:
            tokens = field.query_analyzer.apply(text)
            document_ids_sets = []
            for token in tokens:
                document_ids = self.__search_doc_ids_given_token(field_name, token)
                document_ids_sets.append(document_ids)
            if document_ids_sets:
                resulting_intersection = document_ids_sets[0]
                for other_set in document_ids_sets[1:]:
                    if other_set:
                        resulting_intersection = resulting_intersection.and_operator(other_set)
                if size:
                    resulting_intersection = list(resulting_intersection)[:size]
                return self.documents.get_many(resulting_intersection)
        return []

    def __search_doc_ids_given_token(self, field_name, token) -> IndexDocumentIds:
        index_token_documents_mapping = self.index.get(field_name)
        if index_token_documents_mapping:
            documents_set = index_token_documents_mapping.get(token)
            return documents_set
        return IndexDocumentIds()

    def size(self):
        return len(self.documents)
