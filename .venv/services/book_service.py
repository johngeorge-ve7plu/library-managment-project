from models.book import Book
from storage.json_handler import JSONHandler

from algorithms.searching import SearchingAlgorithms
from algorithms.sorting import SortingAlgorithms

from utils.constants import LibraryConstants
from utils.validators import Validators

class BookService:
    def __init__(self):
        self.json_handler = JSONHandler()
        self.books = self.json_handler.load_books()

    def save_books(self):
        self.json_handler.save_books(self.books)
    
    def generate_book_id(self):
        if len(self.books) == 0:
            return 1001
        ids = []
        for book in self.books:
            ids.append(book.book_id)
        return max(ids) + 1
    
    def book_exists(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return True
        return False
    
    def get_book_by_id(self,book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None
    
    #add books
    def add_book(self, title, author, publication_year, category, copies = 1):
        print("Adding a new book:")
        try:
            if not title or not title.strip():
                print("Title cannot be empty.")
                return
            if not author or not author.strip():
                print("Author cannot be empty.")
                return
            publication_year = int(publication_year)
            if not publication_year or not publication_year.strip():
                print("Publication year cannot be empty.")
                return
            if not category or not category.strip():
                print("Category cannot be empty.")
                return
            copies = int(copies)
            if copies <= 0:
                print("Number of copies must be a positive integer.")
                return
            

            book_id = self.generate_book_id()
            book = Book(
                book_id=book_id,
                title=title.strip(),
                author=author.strip(),
                publication_year=publication_year,
                catagory=category.strip(),
                total_copies=copies,
                )
            self.books.append(book)
            self.save_books()
            print(f"Book '{title}' added successfully with ID {book_id}.")
            return book
        except ValueError:
            print("Invalid input. Please enter the correct data types.")
            return None
        except TypeError:
            print("Invalid input. Please enter the correct data types.")
            return None
        except Exception as error:
            print(f"An error occurred while adding the book: {error}")
            return None

    def view_all_books(self):
        print("All Books:")
        if len(self.books) == 0:
            print("No books available.")
            return
        
        for index,book in enumerate(self.books,start=1):
            print(f"\nBook {index}:")
            book.display()

    def veiw_book(self):
        try:
            book_id = int(input("Enter the book ID to view: "))
            book = self.get_book_by_id(book_id)
            if book:
                print(f"\nDetails of Book ID {book_id}:")
                book.display()
            else:
                print(f"No book found with ID {book_id}.")
        except ValueError:
            print("Invalid input. Please enter a valid book ID.")
    
    def total_books_count(self):
        return len(self.books)
    
    def total_availble_books(self):
        total_available = 0
        for book in self.books:
            total_available += book.total_copies
        return total_available
    
    def display_stats(self):
        print("\nLibrary Statistics:")
        print(f"Total number of books: {self.total_books_count()}")
        print(f"Total number of available copies: {self.total_availble_books()}")
    #search book by id
    def search_book_by_id(self):
        try:
            book_id = int(book_id)
            result,comparisons = (
                SearchingAlgorithms.linear_search_by_id(self.books, book_id)
            )
            if result is None:
                print(f"No book found with id {book_id}")
                print(f"comparisons made during search: {comparisons}")
                return None
            print()
            print(f"Book found with id {book_id}:")
            result.display()
            print(f"comparisons made during search: {comparisons}")
            return result
        except ValueError:
            print("Invalid input. Please enter a valid book ID.")
            return None
        except Exception as error:
            print(f"An error occurred while searching for the book: {error}")
            return None
    #search book by title
    def search_book_by_title(self):
        if not title or not title.strip():
            print("Title cannot be empty.")
            return []
        title = title.strip().lower()
        try:
            results,comparisons = (
                    SearchingAlgorithms.linear_search_by_id(self.books, title)
                )
            if not results:
                print(f"No books found with title '{title}'.")
                print(f"Comparisons made during search: {comparisons}")
                return []
            print()
            print(f"found {len(results)} book(s) with title '{title}':")
            for book in results:
                book.display()
            print(f"Comparisons made during search: {comparisons}")
            return results
        except Exception as error:
            print(f"An error occurred while searching for books by title: {error}")
            return []
    # search book by author
    def search_book_by_author(self):
        if not author or not author.strip():
            print("Author cannot be empty.")
            return []
        author = author.strip().lower()
        try:
            results,comparisons = (
                    SearchingAlgorithms.linear_search_by_id(self.books, author)
                )
            if not results:
                print(f"No books found by author '{author}'.")
                print(f"Comparisons made during search: {comparisons}")
                return []
            print()
            print(f"found {len(results)} book(s) by author '{author}':")
            for book in results:
                book.display()
            print(f"Comparisons made during search: {comparisons}")
            return results
        except Exception as error:
            print(f"An error occurred while searching for books by author: {error}")
            return []
    # updating book

def update_book(self):
    try:
        book_id = int(input("Enter book id to update: "))
        book = self.get_book_by_id(book_id)
        if book is None:
            print(f"No book found with ID {book_id}.")
            return
        
        print()
        print(f"Current details of Book ID {book_id}:")
        book.display()
        print()
        print("Press enter to keep existing value.")

        title = input(f"Title ({book.title}): ").strip()
        author = input(f"Author ({book.author}): ").strip()
        publication_year = input(f"Publication year({book.publication_year}): ").strip()
        category = input(f"Catagory({book.catagory}): ").strip()
        copies = input(f"Total copies({book.total_copies}): ").strip()
        if title:
            book.title = title
        if author:
            book.author = author
        if publication_year:
            book.publication_year = publication_year
        if category:
            book.catagory = category
        if copies:
            total = int(copies)
            borrowed = book.total_copies - book.available_copies
            if total < borrowed:
                print(f"Cannot set total copies to {total}. There are {borrowed} copies currently borrowed.")
                return
            book.total_copies = total
            book.available_copies = max(0, total - borrowed)
        self.save_books()
        print()
        print(f"Book ID {book_id} updated successfully.")
    except ValueError:
        print("Invalid input. Please enter the correct data types.")

    def delete_book(self):
        try:
            book_id = int(input("Enter book ID to delete: "))
            book = self.get_book_by_id(book_id)
            if book is None:
                print(f"No book found with ID {book_id}.")
                return
            print()
            print(f"Details of book to be deleted:")
            book.display()
            conform = input(f"Are you sure you want to delete '{book.title}'? (y/n): ").strip().lower()
            if conform != 'yes':
                print("Deletion cancelled.")
                return
            self.books.remove(book)
            self.save_books()
            print(f"Book ID {book_id} deleted successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid book ID.")
        except Exception as error:
            print(f"An error occurred while deleting the book: {error}")

    def issue_book(self,book_id):
        book = self.get_book_by_id(book_id)
        if book is None:
            return False
        if book.issue_book():
            self.save_books()
            return True
        return False
    
    def return_book(self,book_id):
        book = self.get_book_by_id(book_id)
        if book is None:
            return False
        if book.return_book():
            self.save_books()
            return True
        return False
    # sort book by title
    def sort_books_by_title(self):
        if len(self.books) == 0:
            print("No books available to sort.")
            return
        m = len(self.books)
        for i in range(m):
            for j in range(0, m-i-1):
                if self.books[j].title.lower() > self.books[j+1].title.lower():
                    self.books[j], self.books[j+1] = self.books[j+1], self.books[j]
        print("Books sorted by title successfully.")
    
    def sort_books_by_year(self):
        if len(self.books) == 0:
            print("No books available to sort.")
            return
        m = len(self.books)
        for i in range(m):
            minumum_index = i
            for j in range(i+1,m):
                if self.books[j].publication_year < self.books[minumum_index].publication_year:
                    minumum_index = j
            self.books[i], self.books[minumum_index] = self.books[minumum_index], self.books[i]
        print("Books sorted by publication year successfully.")
    
    def display_books_by_catagory(self):
        catagories = input("enter catagory to display books: ").strip().lower()
        found = False
        for book in self.books:
            if catagories in book.catagory.lower():
                book.display()
                found = True
        if not found:
            print(f"No books found in catagory '{catagories}'.")
    
    def availible_books(self):
        print("Available Books:")
        found = False
        for book in self.books:
            if book.is_available():
                book.display()
                found = True
        if not found:
            print("No available books at the moment.")
    
    def unavailable_books(self):
        print("Unavailable Books:")
        found = False
        for book in self.books:
            if not book.is_available():
                book.display()
                found = True
        if not found:
            print("All books are currently available.")
    #low stock books
    def low_stock_books(self,threshold=2):
        print("Low Stock Books:")
        found = False
        for book in self.books:
            if book.available_copies <= threshold:
                book.display()
                found = True
        if not found:
            print(f"No books with available copies less than or equal to {threshold}.")
    
    def total_books_borrowed(self):
        total_borrowed = 0
        for book in self.books:
            total_borrowed += (book.total_copies - book.available_copies)
        return total_borrowed
    def search_by_keyword(self):
        keyword = input("Enter a keyword to search for books: ").strip().lower()
        found = False
        for book in self.books:
            if (
                keyword in book.title.lower() or
                keyword in book.author.lower() or
                keyword in book.catagory.lower()
            ):
                book.display()
                found = True
        if not found:
            print(f"No books found with keyword '{keyword}'.")
    
    def detailed_stats(self):

        print("\nDetailed Library Statistics:")
        print(f"Total number of books: {len(self.books)}")
        print(f"Total number of available copies: {self.total_availble_books()}")
        print(f"Total number of borrowed copies: {self.total_books_borrowed()}")
        category_counts = {}
        for book in self.books:
            category_counts[book.catagory] = (category_counts.get(book.catagory, 0)+ 1)
        print("Books by Category:")
        print("-"*30)
        for catagory, count in category_counts.items():
            print(f"{category}: {count}")
        print("-"*30)
    def clear_library(self):
        confirm = input("Are you sure you want to clear the entire library? This action cannot be undone. (yes/no): ").strip().upper()
        if confirm != "YES":
            print("Library clearing cancelled.")
            return
        self.books.clear()
        self.save_books()
        print("Library cleared successfully.")