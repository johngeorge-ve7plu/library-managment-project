from datetime import datetime,timedelta
class BorrowRecord:
    defult_borrow_days = 14
    def __init__(
        self,
        borrow_id: int,
        member_id: int,
        book_id: int,
        issue_date: str = None,
        due_date: str = None,
        return_date: str = None,
        status: str = "Borrowed",
        fine_amount: float = 0.0
        ):
        self.borrow_id = borrow_id
        self.member_id = member_id
        self.book_id = book_id
        if issue_date:
            self.issue_date = issue_date
        else:
            self.issue_date = datetime.now().strftime("%Y-%m-%d")
        
        if due_date:
            self.due_date = due_date
        else:
            due = datetime.strptime(self.issue_date, "%Y-%m-%d") + timedelta(days=self.defult_borrow_days)
            self.due_date = due.strftime("%Y-%m-%d")
        self.return_date = return_date
        self.status = status
        self.fine_amount = fine_amount

    def mark_returned(self):
        if self.status == "Returned":
            return False
        self.return_date = datetime.now().strftime("%Y-%m-%d")
        self.status = "Returned"
        self.calculate_fine()
        return True
    
    def calculate_fine(self,fine_per_day=5):
        if self.return_date is None:
            return 0
        due = datetime.strptime(self.due_date, "%Y-%m-%d")
        returned = datetime.strptime(self.return_date, "%Y-%m-%d")
        overdue_days = (returned - due).days
        if overdue_days > 0:
            self.fine_amount = overdue_days * fine_per_day
        else:
            self.fine_amount = 0.0
        return self.fine_amount
    def is_overdue(self):
        if self.status == "Returned":
            return False
        today = datetime.now()
        due = datetime.strptime(self.due_date, "%Y-%m-%d")
        return today > due
    def remaining_days(self):
        if self.status == "Returned":
            return 0
        today = datetime.now()
        due = datetime.strptime(self.due_date, "%Y-%m-%d")
        remaining = (due - today).days
        return max(remaining, 0)
    
    def extend_due_date(self,extra_days:int):
        due = datetime.strptime(self.due_date, "%Y-%m-%d")
        due += timedelta(days=extra_days)
        self.due_date = due.strftime("%Y-%m-%d")
    

    def reset_fine(self):
        self.fine_amount = 0.0
    def update_status(self, status:str):
        self.status = status
    def get_summary(self):
        return (
            f"borrow_id: {self.borrow_id} | "
            f"member_id: {self.member_id} | "
            f"book_id: {self.book_id} | "
            f"status: {self.status} | "
        )
    def to_dict(self):
        return {
            "borrow_id": self.borrow_id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "issue_date": self.issue_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status,
            "fine_amount": self.fine_amount
        }
    @classmethod
    def from_dict(cls, data):
        record = cls(
            borrow_id=data["borrow_id"],
            member_id=data["member_id"],
            book_id=data["book_id"],
            issue_date=data["issue_date"],
            due_date=data["due_date"],
            return_date=data["return_date"],
            status=data["status", "Borrowed"],
            fine_amount=data["fine_amount", 0.0]
        )
        return record
    
    def __str__(self):
        return (
            f"borrow_id:{self.borrow_id} | "
            f"member_id:{self.member_id} | "
            f"book_id:{self.book_id} | "
            f"status:{self.status} | "
            f"fine_amount:{self.fine_amount:.2f} | "
        )
    def __repr__(self):
        return (
            f"BorrowRecord("
            f"borrow_id={self.borrow_id},"
            f"member_id={self.member_id},"
            f"book_id={self.book_id},"
            f"issue_date={self.issue_date},"
            f"due_date={self.due_date},"
            f"return_date={self.return_date},"
            f"status={self.status},"
            f"fine_amount={self.fine_amount})"
        )