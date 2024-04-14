from whoosh.qparser import QueryParser
from whoosh.index import open_dir

ix = open_dir("indexdir", indexname='article_index')
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("十娘")
    results = searcher.search(query)
    for result in results:
        print(result)