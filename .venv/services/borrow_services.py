from datetime import datetime

from models.borrow_records import BorrowRecord
from services.Book_service import BookService
from services.member_service import MemberService
from storage.json_handler import JSONHandler


class BorrowService:
    def __init__(self):
        self.book_service = BookService()
        self.member_service = MemberService()
        self.json_handler = JSONHandler()
        self.borrow_records = (self.json_handler.load_borrow_records())

    
    #saving borrow records
    def save_records(self):
        self.json_handler.save_borrow_records(self.borrow_records)
    
    #generate borrow id
    def generate_borrow_id(self):
        if len(self.borrow_records) == 0:
            return 1001
        ids = [record.borrow_id for record in self.borrow_records]
        return max(ids) + 1
    
    #get borrow records
    def get_record_by_id(self,borrow_id):
        for record in self.borrow_records:
            if record.borrow_id == borrow_id:
                return record
        return None
    
    #active borrow records
    def get_active_record(self,member_id,book_id):
        for record in self.borrow_records:
            if(
                record.member_id == member_id
                and record.book_id == book_id
                and record.status == "Borrowed"
            ):
                return record
        return None
    
    #display all borrow records
    def view_all_borrow_records(self):
        print("All borrowed books:")
        if len(self.borrow_records) == 0:
            print("No records available.")
            return
        
        for record in self.borrow_records:
            record.display()
    
    #borrowed books
    def total_records(self):
        return len(self.borrow_records)

    #actively borrowed
    def active_records(self):
        count = 0
        for record in self.borrow_records:
            if record.status == 'Borrowed':
                count += 1
        return count

    #returned books
    def returned_records(self):
        count = 0
        for record in self.borrow_records:
            if record.status == "Borrowed":
                count += 1
        return count
        

    def display_statistics(self):
        print("\nDetailed Library Statistics:")
        print(f"\nTotal records:{self.total_records()}")
        print(f"\nBooks issued:{self.active_records()}")
        print(f"\nBooks returned:{self.returned_records()}")
        
    #issue book
    def issue_book(self):
        print("Issue Book")
        try:
            member_id = int(input("enter the Id of the member issuing this book"))
            book_id = int(input("enter book id of the book you are borrowing"))
            member = self.member_service.get_member_by_id(member_id)
            if member is None:
                print("member not found")
                return
            if not member.active:
                print("member account is inactive")
            book = self.book_service.get_book_by_id(book_id)
            if book is None:
                print("Book not found")
                return
            if not book.is_available():
                print("Book is not available")
                return
            if member.has_book(book_id):
                print("Member has already borrowed this book")
                return
            member.borrow_book(book_id)
            self.member_service.save_member()
            borrow_record = BorrowRecord(
                borrow_id=self.generate_borrow_id(),
                member_id=member_id,
                book_id=book_id
            )
            print("Book issued successfully")
            print(f"Borrow ID: {borrow_record.borrow_id}")
            print(f"Due Date: {borrow_record.due_date}")
        except ValueError:
            print("Invalid input. Please enter the correct data types.")

    #return_book
    def return_book(self):
        print("return book")
        try:
            member_id = int(input("enter the member id of the book you are returning"))
            book_id = int(input("enter the book id of the book you are returning"))
            
            member = self.member_service.get_member_by_id(member_id)

            if member is None:
                print("member not found")
                return
            
            if not member.active:
                print("member account is inactive")
                return
            book = self.book_service.get_book_by_id(book_id)

            if book is None:
                print("book not found")
                return
            
            record = self.get_active_record(member_id, book_id)

            if record is None:
                print("borrow record not found")
                return

            record.mark_returned()

            success = self.book_service.return_book(book_id)
            if not success:
                print("Failed to return the book.")
                return
            member.return_book(book_id)
            self.member_service.save_member()
            self.save_records()

            print("Book returned successfully")
            if record.fine_amount > 0:
                print(f"Fine amount: {record.fine_amount}")

        except ValueError:
            print("Invalid input. Please enter a valid borrow ID.")

        except Exception as error:
            print(f"An error occurred while returning the book: {error}")
        
        
    #view active borrow records
    def view_active_records(self):
        print("Active Borrow Records")
        found = False
        for record in self.borrow_records:
            if record.status == "borrowed":
                record.display()
                found = True
        if not found:
            print("No Active Borrow Records")

    #view return records
    def view_returned_records(self):
        print("returned books")
        found = False
        for record in self.borrow_records:
            if record.status == "Returned":
                record.display()
                found = True
        if not found:
            print("no returned records")

    #search borrow records
    def search_records(self):
        try:
            borrow_id = int(input("enter the borrow id"))
            record = self.get_record_by_id(borrow_id)
            if record:
                record.display()
            else:
                print("record not found")
        except ValueError:
            print("invaild borrow id please enter a valid id")
    #view overdue books
    def view_overdue_books(self):
        print("Overdue Books:")
        found = False
        for record in self.borrow_records:
            if (
                record.status == "Borrowed"
                and record.is_overdue()
            ):
                record.calculate_fine()
                record.display()
                print(f"Current fine amount: {record.fine_amount}")
                found = True
        if not found:
            print("No overdue books found.")
        #calculate corrent fine amount
    def calculate_current_fine(self,record):
        if record.status == "Borrowed":
            return record.fine_amount()
        if not record.is_overdue():
            return 0
        today = datetime.now()
        due_date = datetime.strptime(record.due_date, "%Y-%m-%d")
        overdue_days = (today.date() - due_date.date()).days
        if overdue_days > 0:
            return overdue_days * 5
        return 0
    #view fine report
    def view_fine_report(self):
        found = False
        print("Fine Report:")
        total_fine = 0
        for record in self.borrow_records:
            fine = self.calculate_current_fine(record)
            if fine > 0:
                found = True
                print(f"Borrow ID: {record.borrow_id}")
                print(f"Member ID: {record.member_id}")
                print(f"Book ID: {record.book_id}")
                print(f"Due date: {record.due_date}")
                print(f"Fine amount: {fine}")
                print("-"*40)
                total_fine += fine
        if not found:
            print("No fines found.")
        print(f"Total fine amount: {total_fine}")
        #extend due date
    def extend_due_date(self):
        print("Extend due date")
        try:
            borrow_id = int(input("Enter the borrow ID to extend due date: "))
            extra_days = int(input("Enter the number of extra days to extend: "))
            if extra_days <= 0:
                print("Invalid number of days. Please enter a positive integer.")
                return
            if extra_days > 30:
                print("You can only extend the due date by a maximum of 30 days.")
                return
            record = self.get_record_by_id(borrow_id)
            if record is None:
                print("Borrow record not found.")
                return
            if record.status == "Returned":
                print("This book has already been returned")
                return
            old_due_date = record.due_date
            record.extend_due_date(extra_days)
            self.save_records()
            print(f"Due date extended successfully from {old_due_date} to {record.due_date}.")
        except ValueError:
            print("Invalid input. Please enter valid integers for borrow ID and extra days.")
        
    #search records by member
    def search_records_by_member(self):
        print("Member borrow history")
        try:
            member_id = int(input("Enter the member ID to view borrow history: "))
            member = self.member_service.get_member_by_id(member_id)
            if member is None:
                print("Member not found.")
                return
            found = False
            for record in self.borrow_records:
                if record.member_id == member_id:
                    record.display()
                    found = True
            if not found:
                print("No borrow records found for this member.")
        except ValueError:
            print("Invalid input. Please enter a valid member ID.")

    #search records by book
    def search_records_by_book(self):
        print("Book borrow history")
        try:
            book_id = int(input("Enter the book ID to view borrow history: "))
            book = self.book_service.get_book_by_id(book_id)
            if book is None:
                print("Book not found.")
                return
            found = False
            for record in self.borrow_records:
                if record.book_id == book_id:
                    record.display()
                    found = True
            if not found:
                print("No borrow records found for this book.")
        except ValueError:
            print("Invalid input. Please enter a valid book ID.")
    
    #member active boooks
    def get_member_active_books(self,member_id):
        active_books = []
        for record in self.borrow_records:
            if record.member_id == member_id and record.status == "Borrowed":
                active_books.append(record.book_id)
        return active_books
    #get book borrow count
    def get_book_borrow_count(self,book_id):
        count = 0
        for record in self.borrow_records:
            if record.book_id == book_id:
                count += 1
        return count
    
    #most borrowed books
    def most_borrowed_books(self):
        print("Most Borrowed Books:")
        if len(self.borrow_records) == 0:
            print("No borrow records available.")
            return
        borrow_count = {}
        for record in self.borrow_records:
            book_id = record.book_id
            if book_id not in borrow_count:
                borrow_count[book_id] = 0
            borrow_count[book_id] += 1
        sorted_books = sorted(
            borrow_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        for postion,(book_id,count) in enumerate(sorted_books, start = 1):
            book = self.book_service.get_book_by_id(book_id)
            if book:
                print(
                    f"{postion}."
                    f"{book.title}"
                    f"-> {count} borrow(s)"
                )
    #borrowing stats
    def detailed_stats(self):
        print("\nDetailed Borrowing Statistics:")
        total = len(self.borrow_records)
        active = 0
        returned = 0
        overdue = 0
        total_fines = 0.0
        for record in self.borrow_records:
            if record.status == "Borrowed":
                active += 1
                if record.is_overdue():
                    overdue += 1
                    total_fines += self.calculate_current_fine(record)
            elif record.status == "Returned":
                returned += 1
                total_fines += record.fine_amount
        
        print(f"Total borrow records: {total}")
        print(f"Active borrow records: {active}")
        print(f"Returned borrow records: {returned}")
        print(f"Overdue borrow records: {overdue}")
        print(f"Total fines collected: {total_fines:.2f}")
    
    #get borrow history
    def get_borrow_history(self):
        return self.borrow_records
    
    #get active borrow records
    def get_active_borrow_records(self):
        active_records = []
        for record in self.borrow_records:
            if record.status == "Borrowed":
                active_records.append(record)
        return active_records
    
    #get overdue records
    def get_overdue_borrow_records(self):
        overdue_records = []
        for record in self.borrow_records:
            if record.status == "borrowed" and record.is_overdue():
                overdue_records.append(record)
        return overdue_records