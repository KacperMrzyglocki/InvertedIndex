import nltk
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import json
import requests

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

def fetch_text_from_url(url):
    """
    Funkcja pobierająca tekst ze strony internetowej.
    
    Args:
    url (str): URL do strony z tekstem, który chcemy pobrać.
    
    Returns:
    str: Zawartość tekstu ze strony.
    """
    try:
        # Wysyłanie żądania GET do podanego URL
        response = requests.get(url)
        response.raise_for_status()  # Sprawdzanie, czy żądanie zakończyło się sukcesem
        
        # Zwróć zawartość jako tekst
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Błąd przy próbie pobrania tekstu: {e}")
        return None

def read_books_from_json(input_file="books.json"):
    """
    Funkcja odczytująca zapisane książki z pliku JSON.
    
    Args:
    input_file (str): Nazwa pliku, który chcemy odczytać (domyślnie 'books.json').
    
    Returns:
    list: Lista książek z pliku JSON.
    """
    try:
        # Otwórz i wczytaj dane z pliku JSON
        with open(input_file, 'r', encoding='utf-8') as file:
            books = json.load(file)

        # Zwróć odczytane książki
        print(f"Odczytano {len(books)} książek z pliku {input_file}")
        return books

    except FileNotFoundError:
        print(f"Plik {input_file} nie został znaleziony.")
        return []
    except json.JSONDecodeError:
        print(f"Wystąpił problem z dekodowaniem pliku {input_file}.")
        return []

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(int))
    
    def add_document(self, doc_id, text):
        words = text.lower().split() #Split the text to words
        for word in words:
            word = ''.join([ch for ch in word if ch not in punctuation]) #Remove punctuation
            if word not in stop_words:
                lemma = lemmatizer.lemmatize(word)  #Lemmatize words
                self.index[lemma][doc_id] += 1  #Add the word occurence to the dictionary
 
    def search(self, query):
        query = lemmatizer.lemmatize(query.lower())  #Lemmatize words
        return dict(self.index.get(query, {}))
    
#Test
books = read_books_from_json()
index = InvertedIndex()
for book in books:
    url = book.get("url")
    text = fetch_text_from_url(url)
    index.add_document(book.get("id"),text)

#Result
print(index.search("Frankenstein"))
print(index.search("Contents"))
print(index.search("Title"))
