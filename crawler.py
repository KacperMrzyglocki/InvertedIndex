import requests
import json

def encoder(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj

def fetch_books_from_gutendex(query=None, author=None, title=None, language="en", output_file="books.json"):
    """
    Funkcja pobierająca książki z API Gutendex.
    
    Args:
    query (str): Ogólne zapytanie wyszukujące książki według słów kluczowych (opcjonalne).
    author (str): Filtruj książki według nazwiska autora (opcjonalne).
    title (str): Filtruj książki według tytułu (opcjonalne).
    language (str): Filtruj książki według języka (domyślnie 'en').
    limit (int): Liczba książek do pobrania (domyślnie 5).
    
    Returns:
    list: Lista słowników z informacjami o książkach.
    """
    base_url = "https://gutendex.com/books"
    params = {
        "search": query,
        "author": author,
        "title": title,
        "languages": language
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Sprawdza, czy żądanie zakończyło się sukcesem
        books_data = response.json()
        books = books_data.get("results", [])

        filtered_books = []
        for book in books:
            book_info = {
                "id": book.get("id"),
                "title": book.get("title"),
                "authors": ', '.join([author['name'] for author in book.get('authors', [])]),
                "languages": ', '.join(book.get("languages", [])),
                "url": book.get("formats", {}).get("text/plain; charset=us-ascii", "Brak URL")
            }
            filtered_books.append(book_info)

        # Zapisz dane do pliku JSON
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(filtered_books, file, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"Błąd przy próbie pobrania danych z API: {e}")
        return []

# Przykład użycia
books = fetch_books_from_gutendex(query=None, author=None, title=None, language="en")
