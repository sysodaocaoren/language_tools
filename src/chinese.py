from whoosh.fields import TEXT, SchemaClass
from jieba.analyse import ChineseAnalyzer


analyzer = ChineseAnalyzer()
class ArticleSchema(SchemaClass):
    title = TEXT(stored=True, analyzer=analyzer)
    content = TEXT(stored=True, analyzer=analyzer)
    author = TEXT(stored=True, analyzer=analyzer)