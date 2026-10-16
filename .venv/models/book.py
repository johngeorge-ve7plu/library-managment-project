from datetime import datetime

class Book():
    def __init__(
            self,
            book_id:int,
            title:str,
            author:str,
            publication_year:int,
            catagory:str,
            total_copies:int
        ):
    
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.catagory = catagory
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    

    def issue_book(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False
    def return_book(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False
    def update_book(self, title:str=None, author:str=None, publication_year:int=None, catagory:str=None, total_copies:int=None):
        if title:
            self.title = title
        if author:
            self.author = author
        if publication_year:
            self.publication_year = publication_year
        if catagory:
            self.catagory = catagory
        if total_copies is not None:
            borrowed_copies = self.total_copies - self.available_copies
            self.total_copies = total_copies
            self.available_copies = max(0, total_copies - borrowed_copies)
    def is_available(self):
        return self.available_copies > 0
    
    def display(self):
        """
        Displays book information.
        """
        print("-" * 60)
        print(f"Book ID          : {self.book_id}")
        print(f"Title            : {self.title}")
        print(f"Author           : {self.author}")
        print(f"Publication Year : {self.publication_year}")
        print(f"Category         : {self.catagory}")
        print(f"Available Copies : {self.available_copies}")
        print(f"Total Copies     : {self.total_copies}")
        print("-" * 60)
    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "category": self.catagory,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "created_at": self.created_at
        }
    @classmethod
    def from_dict(cls,data):
        book = cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["publication_year"],
            data["category"],
            data["total_copies"]
        )
        book.available_copies = data["available_copies"]
        book.created_at = data["created_at"]
        return book
    def __str__(self):
        return (
            f"{self.book_id} | "
            f"{self.title} | "
            f"{self.author} | "
            f"Available: {self.available_copies}/{self.total_copies}"
        )   
    def __repr__(self):
        return self.__str__()