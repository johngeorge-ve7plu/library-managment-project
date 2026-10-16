class SearchingAlgorithms:
    #liner search
    @staticmethod
    def linear_search_by_id(books,book_id):
        comparisons = 0
        for book in books:
            comparisons += 1
            if book.book_id == book_id:
                return book, comparisons
        return None,comparisons
    #linear search by title
    @staticmethod
    def linear_search_by_title(books,title):
        results = []
        comparisons = 0
        for book in books:
            comparisons += 1
            if title in book.title.lower():
                results.append(book)
        return results, comparisons
    
    #linear search by author
    @staticmethod
    def linear_search_by_author(books,author):
        results = []
        comparisons = 0
        for book in books:
            comparisons += 1
            if author in book.author.lower():
                results.append(book)
        return results, comparisons
    #binary search by ID
    @staticmethod
    def binary_search_by_id(books, book_id):
        left = 0
        right = len(books) - 1
        comparisons = 0
        while left <= right:
            mid = (left + right) // 2
            comparisons += 1
            middle_id = books[mid].book_id
            if middle_id == book_id:
                return books[mid], comparisons
            elif middle_id < book_id:
                left = mid + 1
            else:
                right = mid - 1
        return None, comparisons
    
    #binary search by title
    @staticmethod
    def binary_search_by_title(books, title):
        left = 0
        right = len(books) - 1
        comparisons = 0
        target = title.strip().lower()
        while left <= right:
            mid = (left + right) // 2
            comparisons += 1
            middle_title = books[mid].title.lower()
            if middle_title == target:
                return books[mid], comparisons
            elif middle_title < target:
                left = mid + 1
            else:
                right = mid - 1
        return None, comparisons
    #search all books by catagory
    @staticmethod
    def search_books_by_category(books, category):
        results = []
        comparisons = 0
        catagory = category.strip().lower()
        for book in books:
            comparisons += 1
            if book.category.lower() == catagory:
                results.append(book)
        return results, comparisons
    #general keyword search
    @staticmethod
    def keyword_search(books, keyword):
        results = []
        comparisons = 0
        keyword = keyword.strip().lower()
        for book in books:
            comparisons += 1
            if (
                keyword in book.title.lower() or
                keyword in book.author.lower() or
                keyword in book.category.lower()
            ):
                results.append(book)
        return results, comparisons
    #display search results
    @staticmethod
    def display_search_results(results):    
        if not results:
            print("No books found.")
            return
        print(f"\n{len(results)}book(s) found.")
        print("-" * 60)
        for i,book in enumerate(results, start=1):
            print(f"\nresult {i}:")
            book.display()
    
    #compare linear vs binary search
    @staticmethod
    def compare_search_algorithms(books,book_id):
        linear_book, linear_comparisons = (SearchingAlgorithms.linear_search_by_id(books, book_id))
        sorted_books = sorted(books, key=lambda book: book.book_id)
        binary_book, binary_comparisons = (SearchingAlgorithms.binary_search_by_id(sorted_books, book_id))

        print("\nSearch comparisons")
        print(f"Book ID: {book_id}")
        print(
            f"Linear search:"
            f"{"found"if linear_book else "not found"}"
        )
        print(f"Linear search comparisons: {linear_comparisons}")
        print(f"Binary search comparisons: {binary_comparisons}")
        print("Binary search:")
        print(f'{"found" if binary_book else "not found"}')
        return{
            "linear_search": linear_book,
            "linear_comparisons": linear_comparisons,
            "binary_search": binary_book,
            "binary_comparisons": binary_comparisons
        }