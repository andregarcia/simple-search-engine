
import os
import pathlib
import re

import nltk
nltk.download('stopwords')

import unidecode



def create_analyzer_chain():
    lower_case2 = Lowercase(None)
    stemmer = Stemmer(lower_case2)
    strip_accents = StripAccents(stemmer)
    stopwords = Stopwords(strip_accents)
    lower_case = Lowercase(stopwords)
    tokenizer = Tokenizer(lower_case)
    return tokenizer


class Ngram:

    def __init__(self, max_ngram_size, next):
        self.next = next
        self.max_ngram_size = max_ngram_size

    def apply(self, tokens):
        ngrams = []
        for n in range(1, self.max_ngram_size+1):
            for i in range(len(tokens)-n+1):
                current_ngram = []
                for c in range(n):
                    current_ngram.append(tokens[i+c])
                ngrams.append(' '.join(current_ngram))
        if self.next:
            return self.next.apply(ngrams)
        return ngrams


class TokenTaggerBlacklist:

    def __init__(self):
        file1 = os.path.join(pathlib.Path(__file__).parent.absolute(), '../../resources/token_tagger_blacklist.txt')
        self.terms = self.read_file(file1)
        file2 = os.path.join(pathlib.Path(__file__).parent.absolute(), '../../resources/website_token_tagger_blacklist.txt')
        self.website_terms = self.read_file(file2)

    def read_file(self, file):
        lines = set()
        with open(file, 'r') as f:
            for line in f:
                if not line or not line.strip() or line.strip().startswith('#'):
                    continue
                term = line.lower().strip()
                lines.add(term)
        return lines

    def is_website_blacklisted(self, term):
        return term in self.website_terms

    def is_blacklisted(self, term):
        return term in self.terms


class Tokenizer:

    def __init__(self, next):
        self.next = next

    def apply(self, text):
        result = text.split()
        if self.next:
            return self.next.apply(result)
        return result


class Stopwords:

    def __init__(self, next):
        self.next = next
        self.stopwords = set(nltk.corpus.stopwords.words('portuguese'))

    def apply(self, tokens):
        tokens = [token for token in tokens if token not in self.stopwords]
        if self.next:
            return self.next.apply(tokens)
        return tokens


class StripAccents:

    def __init__(self, next):
        self.next = next

    def apply(self, tokens):
        tokens = [unidecode.unidecode(token) for token in tokens]
        if self.next:
            return self.next.apply(tokens)
        return tokens


class Lowercase:

    def __init__(self, next):
        self.next = next

    def apply(self, tokens):
        tokens = [token.lower() for token in tokens]
        if self.next:
            return self.next.apply(tokens)
        return tokens


class Stemmer:

    def __init__(self, next):
        self.next = next

    def apply(self, tokens):
        tokens = [self.__stem(token) for token in tokens]
        if self.next:
            return self.next.apply(tokens)
        return tokens

    def __stem(self, token):
        token = re.sub('res$', '', token)   # plural
        token = re.sub('s$', '', token)     # plural
        token = re.sub('r$', '', token)     # verbo
        token = re.sub('[ao]$', '', token)  # genero
        token = re.sub('ue$', '', token)    # imperativo terminado em 'gar'
        token = re.sub('e$', '', token)     # imperativo
        return token

