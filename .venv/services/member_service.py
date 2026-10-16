from models.member import Member
from storage.json_handler import JSONHandler

class MemberService:
    def __init__(self):
        self.json_handler = JSONHandler()
        self.member = self.json_handler.load_members()

    def save_member(self):
        self.json_handler.save_members(self.member)

    def generate_member_id(self):
        if len(self.member) == 0:
            return 1001
        ids = [member.member_id for member in self.member]
        return max(ids) + 1
    
    def member_exists(self,member_id):
        for member in self.member:
            if member.member_id == member_id:
                return True
        return False
    
    def get_member_by_id(self, member_id): 
        for member in self.member:
            if member.member_id == member_id:
                return member
        return None
    
    def add_member(self):
        print("Adding a new Member:")
        try:
            member_id = int(input("enter member id: "))
            if self.member_exists(member_id):
                print(f"Book with ID {member_id} already exists.")
                return
            name = input("Enter member name: ").strip()
            address = input("Enter member adress: ")
            phone = int(input("Enter member phone number: ").strip())
            email = input("Enter member email: ")
            membership_type = input("Enter member type: ").strip()
            if membership_type == "":
                membership_type = "Regular"
            new_member = Member(
                member_id=member_id,
                name=name,
                address=address,
                phone=phone,
                email=email,
                membership_type=membership_type
            )
            self.member.append(new_member)
            self.save_member()
            print(f"Book '{name}' added successfully with ID {member_id}.")
        except ValueError:
            print("Invalid input. Please enter the correct data types.")
        except Exception as error:
            print(f"An error occurred while adding the book: {error}")


    def view_all_member(self):
        print("All Members:")
        if len(self.member) == 0:
            print("No members available.")
            return
        
        for index,member in enumerate(self.member,start=1):
            print(f"\nMember {index}:")
            member.display()

    def view_member(self):
        try:
            member_id = int(input("Enter the member ID to view: "))
            member = self.get_member_by_id(member_id)
            if member:
                print(f"\nDetails of member ID {member_id}:")
                member.display()
            else:
                print(f"No member found with ID {member_id}.")
        except ValueError:
            print("Invalid input. Please enter a valid member ID.")

    def total_members(self):
        return len(self.member)
    
    def active_members(self):
        count = 0
        for member in self.member:
            if member.active:
                count += 1
        return count
    
    def display_stats(self):
        print("\Member Statistics:")
        print(f"Total number of members: {self.total_members()}")
        print(f"Total number of active members: {self.active_members()}")
    
    def delete_member(self,member_id):
        print("Delete Member:")
        try:
            member_id = int(input("Enter Member ID to delete: "))
            member = self.get_member_by_id(member_id)
            if member is None:
                print(f"No member found with ID {member_id}.")
                return
            if len(member.borrowed_books):
                print("can't delete, member still has borrowed books.")
                return
            confirm = input(f"Are you sure you want to delete '{member_id}'? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return
            self.member.remove(member)
            self.save_member()
            print(f"Book ID {member_id} deleted successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid member ID.")

    def search_member_by_id(self,member_id):
        print("Search Member by ID:")
        try:
            member_id = int(input("Enter member id:"))
            members = self.get_member_by_id(member_id)
            if members:
                print("\nMember found:")
                members.display()
            else:
                print(f"No member found with ID {member_id}.")
        except ValueError:
            print("Invalid input. Please enter a valid member ID.")

    def search_member_by_name(self,name):
        print("search member by name")
        names = input("Enter member name: ").strip().lower()
        found = False
        for member in self.member:
            if name in member.lower():
                member.display()
                found = True
        if not found:
            print(f"No members found with name '{name}'.")

    def update_member(self,member_id):
        print("update member details")
        try:
            member_id = int(input("Enter member id to update: "))
            member = self.get_member_by_id(member_id)
            if member is None:
                print(f"No member found with ID {member_id}.")
                return
            print("\nleave blank if you don't want to update a field.\n")
            name = input(f"Name ({member.name}): ").strip()
            address = input(f"Address ({member.address}): ").strip()
            phone = input(f"Phone ({member.phone}): ").strip()
            email = input(f"Email ({member.Email}): ").strip()
            membership = input(f"Membership type ({member.membership_type}): ").strip()
            if name:
                member.name = name
            if address:
                member.address = address
            if phone:
                member.phone = phone
            if email:
                member.email = email
            if membership:
                member.membership_type = membership
            
            self.save_member()
            print(f"Member ID {member_id} updated successfully.")
        except ValueError:
            print("Invalid input. Please enter the correct data types.")
        
    def activate_member(self,member_id):
        try:
            member = int(input("Enter member id to activate: "))
            member = self.get_member_by_id(member_id)
            if member:
                member.active()
                self.save_member()
                print(f"Member ID {member_id} activated successfully.")
            else:
                print("member not found")
        except ValueError:
            print("Invalid input. Please enter a valid member ID.")

    def deactivate_member(self,member_id):
        try:
            member = int(input("enter member ID to be deactivated: "))
            member = self.get_member_by_id(member_id)
            if member:
                if len(member.borrowed_books)> 0:
                    print("can not deactivate")
                    print("member still has borrowed books")
                    return
                member.deactivate()
                self.save_member()
            else:
                print("member not found")
        except ValueError:
            print("Invalid input. Please enter a valid member ID")

    def view_borrowed_books(self,member_id):
        try:
            member_id = int(input("enter member id to view books of"))
            member = self.get_member_by_id(member_id)
            if member is None:
                print("member not found")
                return
            print(f"\n borrowed books of member {member.name}: ")
            print("-"*30)
            if len(member.borrowed_books) == 0:
                print("no borrowed books")
                return
            for book_id in member.borrowed_books:
                print(book_id)
        except ValueError:
            print("invalid input. Please enter a valid input")