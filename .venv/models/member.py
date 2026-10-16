from datetime import datetime

class Member:
    def __init__(
        self,
        member_id: int,
        name: str,
        phone: str,
        email: str,
        address: str,
        membership_type: str = "Standard",
        active: bool = True,
    ):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.membership_type = membership_type
        self.active = active
        self.borrowed_books = []
        self.joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def borrow_book(self, book_id: int):
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
            return True
        return False
    
    def return_book(self, book_id: int):
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False
    
    def has_book(self, book_id: int):
        return book_id in self.borrowed_books
    
    def update_details(
        self,
        name=None,
        phone=None,
        email=None,
        address=None,
        membership_type=None,
    ):        
    
        if name:
            self.name = name
        if phone:
            self.phone = phone
        if email:
            self.email = email
        if address:
            self.address = address
        if membership_type:
            self.membership_type = membership_type
    
    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def display(self):
        """
        Displays book information.
        """
        print("=" * 60)
        print("MEMBER DETAILS")
        print("=" * 60)
        print(f"Member ID        : {self.member_id}")
        print(f"Name             : {self.name}")
        print(f"Phone            : {self.phone}")
        print(f"Email            : {self.email}")
        print(f"Address          : {self.address}")
        print(f"Membership Type  : {self.membership_type}")
        print(f"Status           : {'Active' if self.active else 'Inactive'}")
        print(f"Books Borrowed   : {len(self.borrowed_books)}")
        print(f"Borrowed Book IDs: {self.borrowed_books}")
        print(f"Joined Date      : {self.joined_date}")
        print("=" * 60)

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "membership_type": self.membership_type,
            "active": self.active,
            "borrowed_books": self.borrowed_books,
            "join_date": self.joined_date
        }
    
    @classmethod

    def from_dict(cls, data):
        member = cls(
            member_id = data["member_id"],
            name = data["name"],
            phone = data["phone"],
            email = data["email"],
            address = data["address"],
            membership_type=data.get("membership_type", "Standard"),
            active=data.get("active", True),
        )
        member.borrowed_books = data.get("borrowed_books", [])
        member.joined_date = data.get(
            "joined_date",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return member

    def __str__(self):
        return (
            f"{self.member_id} | "
            f"{self.name} | "
            f"{self.membership_type} | "
            f"Borrowed Books: {len(self.borrowed_books)}"
        )
    def __repr__(self):
        return (
            f"Member(member_id={self.member_id}, "
            f"name={self.name}, "
            f"membership_type={self.membership_type}, "
            f"borrowed_books={len(self.borrowed_books)})"
        )