from unittest import TestCase

from src.analyzer import create_analyzer_chain
from src.index import Index, Fields, Field, Document


class TestIndex(TestCase):

    def test_index_one(self):
        index = Index(fields=Fields([
            Field('main', create_analyzer_chain())
        ]))
        index.index_one(Document(id='1', doc={'main' : 'testando indexacao um documento'}))
        index.index_one(Document(id='2', doc={'main': 'testando indexacao outro documento'}))
        index.index_one(Document(id='3', doc={'main': 'abcde index'}))
        self.assertEqual(3, index.size())

    def test_index_many(self):
        index = Index(fields=Fields([
            Field('main', create_analyzer_chain())
        ]))
        index.index_many([Document(id='1', doc={'main' : 'testando indexacao um documento'}),
                          Document(id='2', doc={'main': 'testando indexacao outro documento'}),
                          Document(id='3', doc={'main': 'abcde index'})])
        self.assertEqual(3, index.size())

    def test_search(self):
        index = Index(fields=Fields([
            Field('main', create_analyzer_chain())
        ]))
        index.index_one(Document(id='1', doc={'main' : 'testando indexacao um documento'}))
        index.index_one(Document(id='2', doc={'main': 'testando indexacao outro documento'}))
        index.index_one(Document(id='3', doc={'main': 'abcde index'}))
        result = index.search('main', 'testando', 10)
        self.assertEqual(2, len(result))
