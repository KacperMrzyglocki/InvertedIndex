import nltk
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import json
import pickle
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Download necessary NLTK resources if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize NLTK resources
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)
lemmatizer = WordNetLemmatizer()
lock = Lock()  # Create a lock for thread-safe operations

def fetch_text_from_url(url):
    """Fetch text from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching text: {e}")
        return None

def read_books_from_json(input_file="books.json"):
    """Read books from a JSON file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            books = json.load(file)
        print(f"Read {len(books)} books from {input_file}")
        return books
    except FileNotFoundError:
        print(f"File {input_file} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {input_file}.")
        return []

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(int))
    
    def add_document(self, doc_id, text):
        words = nltk.word_tokenize(text.lower())  # Tokenize text
        for word in words:
            word = ''.join([ch for ch in word if ch not in punctuation])  # Remove punctuation
            if word and word not in stop_words:
                with lock:  # Ensure thread-safe lemmatization
                    lemma = lemmatizer.lemmatize(word)  # Lemmatize word
                self.index[lemma][doc_id] += 1  # Add occurrence

    def search(self, query):
        query = lemmatizer.lemmatize(query.lower())
        return dict(self.index.get(query, {}))
    
    def serialize(self, output_file="inverted_index.pkl"):
        """Serialize the inverted index to a Pickle file."""
        # Convert defaultdict to a regular dict before pickling
        index_as_dict = {key: dict(value) for key, value in self.index.items()}
        with open(output_file, 'wb') as file:
            pickle.dump(index_as_dict, file)
        print(f"Inverted index serialized to {output_file}.")

    @classmethod
    def deserialize(cls, input_file="inverted_index.pkl"):
        """Deserialize the inverted index from a Pickle file."""
        try:
            with open(input_file, 'rb') as file:
                index_data = pickle.load(file)
            inverted_index = cls()
            # Convert back to defaultdict after loading
            inverted_index.index = defaultdict(lambda: defaultdict(int), {key: defaultdict(int, value) for key, value in index_data.items()})
            print(f"Inverted index deserialized from {input_file}.")
            return inverted_index
        except FileNotFoundError:
            print(f"File {input_file} not found.")
            return cls()
        except pickle.UnpicklingError:
            print(f"Error unpickling {input_file}.")
            return cls()

def process_book(book):
    """Process a book to add its text to the inverted index."""
    url = book.get("url")
    text = fetch_text_from_url(url)
    if text:
        index.add_document(book.get("id"), text)

# Main function to build the inverted index
def build_inverted_index(books):
    global index
    index = InvertedIndex()  # Initialize the inverted index

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_book, book) for book in books]
        for future in futures:
            future.result()  # Ensure all threads complete

# Run the program
if __name__ == "__main__":
    # Pre-load WordNet to prevent threading issues
    nltk.data.find('corpora/wordnet.zip')

    books = read_books_from_json()
    build_inverted_index(books)

    # Serialize the index
    index.serialize()

