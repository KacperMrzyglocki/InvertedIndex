import crawler
import invertedIndexParallelPickle as ii
import nltk

ex=0
while(ex!=1):
    print('1.Update books')
    print('2.Search books')
    print('3.Exit')
    x=int(input('?>'))
    if(x==1):
        print('Key words(Enter for None)')
        query=input('?>')
        print('Language(Enter for None, example: en)')
        language=input('?>')
        if(query==''):
            query=None
        author=None
        title=None
        if(language==''):
            language=None
        crawler.fetch_books_from_gutendex(query, author, title, language)
        nltk.data.find('corpora/wordnet.zip')
        books = ii.read_books_from_json()
        ii.build_inverted_index(books)
        ii.index.serialize()
    if(x==2):
        p=0
        while(p==0):
            deserialized_index = ii.InvertedIndex.deserialize()
            print('Key word')
            key=input('?>')
            if(key==''):
                print('This prompt cannot be empty')
            else:
                print(deserialized_index.search(key))
                p+=1
    if(x==3):
        ex=1


