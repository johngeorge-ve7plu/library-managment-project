class LibraryConstants:
    #borrowing
    DEFAULT_BORROWING_DAYS = 14
    FINE_PER_DAY = 5.0
    MAX_BOOKS_PER_MEMBER = 5

    #book status
    BOOK_AVAILBLE = "Available"
    BOOK_UNALAILABLE = "Unavailable"

    #borrow status
    BORROWED = "Borrowed"
    RETURNED = "Returned"
    OVERDUE = "Overdue"

    #member status
    ACTIVE = "Active"
    INACTIVE = "Inactive"

    #date format
    DATE_FORMAT = "%Y-%m-%d"

    #defult values
    DEFAULT_BOOK_COPIES = 1
    DEFAULT_MEMBER_STATUS = ACTIVE
    DEFAULT_BORROW_STATUS = BORROWED
    DEFAULT_FINE = 0.0

    #file paths
    BOOKS_FILE = "data/books.json"
    MEMBERS_FILE = "data/members.json"
    BORROW_RECORDS_FILE = "data/borrow_records.json"

    #search options
    SEARCH_BY_ID = "id"
    SEARCH_BY_TITLE = "title"
    SEARCH_BY_AUTHOR = "author"
    SEARCH_BY_CATEGORY = "category"

    #sort options
    SORT_BY_ID = "id"
    SORT_BY_TITLE = "title"
    SORT_BY_YEAR = "year"
    SORT_BY_AUTHOR = "author"
    SORT_BY_CATEGORY = "category"

    #allowed_values
ALLOWED_BORROWED_STATUSES = [
    LibraryConstants.BORROWED,
    LibraryConstants.RETURNED,
    LibraryConstants.OVERDUE
    ]

ALLOWED_MEMBER_STATUSES = [
    LibraryConstants.ACTIVE,
    LibraryConstants.INACTIVE
    ]
ALLOWED_SEARCH_FIELDS = [
    LibraryConstants.SEARCH_BY_ID,
    LibraryConstants.SEARCH_BY_TITLE,
    LibraryConstants.SEARCH_BY_AUTHOR,
    LibraryConstants.SEARCH_BY_CATEGORY
]
ALLOWED_SORT_FIELDS = [
    LibraryConstants.SORT_BY_ID,
    LibraryConstants.SORT_BY_TITLE,
    LibraryConstants.SORT_BY_YEAR,
    LibraryConstants.SORT_BY_AUTHOR,
    LibraryConstants.SORT_BY_CATEGORY
]


