class LibraryReport:
    def __init__(self, Book_service, member_service, borrow_service):
        self.book_service = Book_service
        self.member_service = member_service
        self.borrow_service = borrow_service

    def generate_summary(self):
        books = self.book_service.books
        members = self.member_service.member
        records = self.borrow_service.borrow_records        
        total_titles = len(books)
        total_members = len(members)

        total_copies = 0
        available_copies = 0
        borrowed_copies = 0
        for book in books:
            total_copies += book.total_copies
            available_copies += book.available_copies
            borrowed_copies += (book.total_copies - book.available_copies)
        active_members = 0
        for member in members:
            if member.active:
                active_members += 1
        active_borrowings = 0
        returned_books = 0
        for record in records:
            if not record.returned:
                active_borrowings += 1
            else:
                returned_books += 1
        
        return {
            "total_titles": total_titles,
            "total_copies": total_copies,
            "available_copies": available_copies,
            "borrowed_copies": borrowed_copies,
            "total_members": total_members,
            "active_members": active_members,
            "active_borrowings": active_borrowings,
            "returned_books": returned_books
        }

    def display_summary(self):
        summary = self.generate_summary()
        print("\n Library Summary Report")
        print("-"*50)
        print(f"Total Titles: {summary['total_titles']}")
        print(f"Total Copies: {summary['total_copies']}")
        print(f"Available Copies: {summary['available_copies']}")
        print(f"Borrowed Copies: {summary['borrowed_copies']}")
        print(f"Total Members: {summary['total_members']}")
        print(f"Active Members: {summary['active_members']}")
        print(f"Active Borrowings: {summary['active_borrowings']}")
        print(f"Returned Books: {summary['returned_books']}")
        print("-"*50)

    def catagory_report(self):
        catagories = {}
        for book in self.book_service.books:
            catagory = book.catagory
            if catagory not in catagories:
                catagories[catagory] = 0
            catagories[catagory] += 1
        print("catagory_report")
        if not catagories:
            print("No books found.")
            return
        for catagory, count in catagories.items():
            print(f"{catagory: <25}: {count}")

    def member_report(self):
        print("member report")
        members = self.member_service.member
        if not members:
            print("No members found.")
            return
        for member in members:
            borrowed_count = len(member.borrowed_books)
            status = "Active" if member.active else "Inactive"
            print(f"Member ID{member.member_id}")
            print(f"Name: {member.name}")
            print(f"Books held: {borrowed_count}")
            print(f"Status: {status}")  
            

    def overdue_report(self):
        print("overdue report")
        overdue_records = (self.borrow_service.get_overdue_records())
        if not overdue_records:
            print("No overdue records found.")
            return
        total_fine = 0
        for record in overdue_records:
            fine = (self.borrow_service.calculate_fine(record))
            total_fine += fine
            print(f"Record ID: {record.record_id}")
            print(f"Member ID: {record.member_id}")
            print(f"Book ID: {record.book_id}")
            print(f"Due Date: {record.due_date.strftime('%Y-%m-%d')}")
            print(f"Fine: ${fine:.2f}")
            print("Total Fine: ${total_fine:.2f}")

    def availibilty_report(self):
        print("availbility report")
        available_books = self.book_service.get_available_books()
        if not available_books:
            print("No available books found.")
            return
        for book in available_books:
            if book.total_copies == 0:
                percentage = 0
            else:
                percentage = (book.available_copies / book.total_copies) * 100
            print(f"Title: {book.title}")
            print(f"Total Copies: {book.total_copies}")
            print(f"Available Copies: {book.available_copies}")
            print(f"Availability Percentage: {percentage:.2f}%")
            print("-"*50)

        

    def borrowing_report(self):
        print("borrowing report")
        records = self.borrow_service.borrow_records
        if not records:
            print("No borrowing records found.")
            return
        total = len(records)
        active = 0
        returned = 0
        overdue = 0
        for record in records:
            if record.status == "borrowed":
                active += 1
                if record.is_overdue():
                    overdue += 1
            elif record.status == "returned":
                returned += 1

            print(f"total transactions: {total}")
            print(f"currently borrowed: {active}")
            print(f"returned books: {returned}")
            print(f"overdue books: {overdue}")

    def member_borrowing_analysis(self):
        print("member borrowing analysis")
        borrowing_counts = {}
        for record in self.borrow_service.borrow_records:
            member_id = record.member_id
            if member_id not in borrowing_counts:
                borrowing_counts[member_id] = 0
            borrowing_counts[member_id] += 1
        if not borrowing_counts:
            print("No borrowing records found.")
            return
        for member_id, count in borrowing_counts.items():
            member = (self.member_service.get_member_by_id(member_id))
            if member:
                print(f"Member ID: {member_id}")
                print(f"Name: {member.name}")
                print(f"Total Borrowed Books: {count}")
                print("-"*50)


    def book_borrowing_analysis(self):
        print("book borrowing analysis")
        borrowing_counts = {}
        for record in self.borrow_service.borrow_records:
            book_id = record.book_id
            if book_id not in borrowing_counts:
                borrowing_counts[book_id] = 0
            borrowing_counts[book_id] += 1
        if not borrowing_counts:
            print("No borrowing records found.")
            return
        for book_id, count in borrowing_counts.items():
            book = (self.book_service.get_book_by_id(book_id))
            if book:
                print(f"Book ID: {book_id}")
                print(f"Title: {book.title}")
                print(f"Total Times Borrowed: {count}")
                print("-"*50)


    def find_report(self):
        total_fines = 0
        returned_fines = 0
        outstanding_fines = 0
        for record in self.borrow_service.borrow_records:
            if record.status == "Returned":
                returned_fines += record.fine_amount
            else:
                outstanding_fines += self.borrow_service.calculate_fine(record)
        total_fines = (returned_fines + outstanding_fines)
        print("find report")
        print(f"Collected Fines: ${returned_fines:.2f}")
        print(f"Outstanding Fines: ${outstanding_fines:.2f}")
        print(f"Total Fines: ${total_fines:.2f}")    

    def generate_complete_report(self):
        print("Generating complete report...")
        self.display_summary()
        self.catagory_report()
        self.member_report()
        self.overdue_report()
        self.availibilty_report()
        self.borrowing_report()
        self.member_borrowing_analysis()
        self.book_borrowing_analysis()
        self.find_report()

