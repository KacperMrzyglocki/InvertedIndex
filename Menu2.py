import crawler
import invertedIndexParallelPickle as ii
import nltk
import time

ex = 0
while ex != 1:
    print('1. Update books')
    print('2. Search books')
    print('3. Exit')
    x = int(input('?>'))
    
    if x == 1:
        print('Key words (Enter for None)')
        query = input('?>')
        print('Language (Enter for None, example: en)')
        language = input('?>')
        
        if query == '':
            query = None
        author = None
        title = None
        if language == '':
            language = None
        
        # Fetch books
        crawler.fetch_books_from_gutendex(query, author, title, language)
        nltk.data.find('corpora/wordnet.zip')
        books = ii.read_books_from_json()
        
        # Benchmark using time.time()
        num_runs = 5
        total_time = 0
        for _ in range(num_runs):
            start_time = time.time()
            ii.build_inverted_index(books)
            end_time = time.time()
            total_time += (end_time - start_time)
        
        avg_time = total_time / num_runs
        print(f'Indexing completed. Average time over {num_runs} runs: {avg_time:.4f} seconds.')
        
        # Serialize the inverted index
        ii.index.serialize()
    
    elif x == 2:
        p = 0
        while p == 0:
            num_runs = 5
            total_time = 0
            print('Key word')
            key = input('?>')
            for _ in range(num_runs):
                start_time = time.time()
                deserialized_index = ii.InvertedIndex.deserialize()
                if key == '':
                    print('This prompt cannot be empty')
                else:
                    print(deserialized_index.search(key))
                    p += 1
                end_time = time.time()
                total_time += (end_time - start_time)
        
            avg_time = total_time / num_runs
            print(f'Indexing completed. Average time over {num_runs} runs: {avg_time:.4f} seconds.')
        
    
    elif x == 3:
        ex = 1
