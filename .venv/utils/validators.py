from datetime import datetime
import re


class Validators:
    @staticmethod
    def validate_required(value, field_name = "Value"):
        if value is None:
            return False, f"{field_name} is required."
        value = str(value).strip()
        if not value:
            return False, f"{field_name} cannot be empty."
        return True, ""
    
    @staticmethod
    def validate_integer(value, field_name = "Value", minimum = None, maximum = None):
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            return False, f"{field_name} must be an integer."
        
        if minimum is not None and int_value < minimum:
            return False, f"{field_name} must be at least {minimum}."
        
        if maximum is not None and int_value > maximum:
            return False, f"{field_name} must not exceed {maximum}."
        
        return True, ""
    
    @staticmethod
    def validate_positive_integer(value, field_name = "Value"):
        return Validators.validate_integer(value, field_name, minimum=1)
    
    @staticmethod
    def validate_non_negitive_integer(value, field_name = "Value"):
        return Validators.validate_integer(value, field_name, minimum = 0)
    

    @staticmethod
    def validate_float(value, field_name = "Value", minimum = None, maximum = None):
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            return False, f"{field_name} must be a number."
        
        if minimum is not None and float_value < minimum:
            return False, f"{field_name} must be at least {minimum}."
        
        if maximum is not None and float_value > maximum:
            return False, f"{field_name} must not exceed {maximum}."
        
        return True, ""
    
    @staticmethod
    def validate_name(name):
        if not name or not name.strip():
            return False, "Name cannot be empty."
        
        name = str(name).strip()
        if len(name) < 2:
            return False, "Name must be at least 2 characters long."
        if len(name) > 100:
            return False, "Name must not exceed 100 characters."
        pattern = r"^[A-Za-z][A-Za-z .'-]*$"
        if not re.fullmatch(pattern, name):
            return False, "Name contains invalid characters."
        return True, ""
    

    @staticmethod
    def validate_email(email):
        if not email or not email.strip():
            return False, "Email cannot be empty."
        
        email = str(email).strip()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.fullmatch(pattern, email):
            return False, "Invalid email format."
        return True, ""
    
    @staticmethod
    def validate_phone(phone):
        if not phone:
            return False, "Phone number cannot be empty."
        phone = str(phone).strip()
        phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        pattern = r"^[6-9][0-9]{9}$"
        if not re.fullmatch(pattern, phone):
            return False, "Invalid phone number format."
        return True, ""
    
    @staticmethod
    def validate_book_title(title):
        if not title or not str(title).strip():
            return False, "Book title cannot be empty."
        title = str(title).strip()
        if len(title) < 2:
            return False, "Book title must be at least 2 characters long."
        if len(title) > 200:
            return False, "Book title must not exceed 200 characters."
        return True, ""

    @staticmethod
    def validate_author(author):
        if not author or not str(author).strip():
            return False, "Author name cannot be empty."
        author = str(author).strip()
        if len(author) < 2:
            return False, "Author name must be at least 2 characters long."
        if len(author) > 100:
            return False, "Author name must not exceed 100 characters."
        pattern = r"^[A-Za-z][A-Za-z .'-]*$"
        if not re.fullmatch(pattern, author):
            return False, "Author name contains invalid characters."
        return True, ""

    @staticmethod
    def validate_year(year,minimum_year = 1000, maximum_year = None):
        if maximum_year is None:
            maximum_year = datetime.now().year
        valid, message = Validators.validate_integer(year, "Year", minimum_year, maximum_year)    
        return valid,message

    @staticmethod
    def validate_category(category):
        if not category or not str(category).strip():
            return False, "Category cannot be empty."
        category = str(category).strip()
        if len(category) < 2:
            return False, "Category must be at least 2 characters long."
        if len(category) > 100:
            return False, "Category must not exceed 100 characters."
        return True, ""

    @staticmethod
    def validate_book_copies(copies):
        return Validators.validate_positive_integer(copies, "Number of copies")

    @staticmethod
    def validate_book_id(book_id):
        return Validators.validate_positive_integer(book_id, "Book ID")

    @staticmethod
    def validate_member_id(member_id):
        return Validators.validate_positive_integer(member_id, "Member ID")

    @staticmethod
    def validate_borrow_id(borrow_id):
        return Validators.validate_positive_integer(borrow_id, "Borrow ID")
    
    @staticmethod
    def validate_date(date_string, date_format = "%Y-%m-%d"):
        if not date_string:
            return False, "Date cannot be empty."
        try:
            datetime.strptime(date_string, date_format)
        except ValueError:
            return False, f"Date must be in the format {date_format}."
        return True, ""
    
    @staticmethod
    def validate_date_not_in_future(date_string, date_format = "%Y-%m-%d"):
        valid,message = Validators.validate_date(date_string, date_format)
        if not valid:
            return False,message
        date_value = datetime.strptime(date_string, date_format).date()
        today = datetime.now().date()
        if date_value > today:
            return False, "Date cannot be in the future."
        return True, ""
    
    @staticmethod
    def validate_status(status, allowed_statuses):
        if not status:
            return False, "Status cannot be empty."

        if status not in allowed_statuses:
            return False, f"Status must be one of {', '.join(allowed_statuses)}."
        return True, ""
    
    @staticmethod
    def validate_yes_no(value):
        if not value:
            return False, "Please enter yes or no"
        value = str(value).strip().lower()
        if value not in ["yes","no","y","n"]:
            return False, "Please enter yes or no"
        return True, ""
    
    @staticmethod
    def validate_password(password):
        if not password:
            return False, "Password cannot be empty."
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if len(password) > 100:
            return False, "Password must not exceed 100 characters."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one digit."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character."
        return True, ""
    
    @staticmethod
    def validate_search_text(value,field_name = "Search Text"):
        if not value or not str(value).strip():
            return False, f"{field_name} cannot be empty."
        value = str(value).strip()
        if len(value) < 1:
            return False, f"{field_name} must be at least 1 character long."
        if len(value) > 50:
            return False, f"{field_name} must not exceed 50 characters long."
        return True, ""
    
    @staticmethod
    def validate_book_data(book_id,title,author,publication_year,catagory,total_copies):
        error = []
        valid, message = Validators.validate_book_id(book_id)
        if not valid:
            error.append(message)
        
        valid, message = Validators.validate_book_title(title)
        if not valid:
            error.append(message)
        
        valid, message = Validators.validate_author(author)
        if not valid:
            error.append(message)
        
        valid, message = Validators.validate_year(publication_year)
        if not valid:
            error.append(message)
        
        valid, message = Validators.validate_category(catagory)
        if not valid:
            error.append(message)

        valid, message = Validators.validate_book_copies(total_copies)
        if not valid:
            error.append(message)
        
        return len(error) == 0, error
    
    @staticmethod
    def validate_member_data(member_id,name,email,phone):
        error = []
        valid, message = Validators.validate_member_id(member_id)
        if not valid:
            error.append(message)
        
        valid, message = Validators.validate_name(name)
        if not valid:
            error.append(message)
        
        valid, message = Validators.validate_email(email)
        if not valid:
            error.append(message)
        
        valid, message = Validators.validate_phone(phone)
        if not valid:
            error.append(message)
        
        return len(error) == 0, error





"""
# =============================================================
# SIMPLE TESTING
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("VALIDATORS TEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # Name
    # ---------------------------------------------------------

    valid, message = Validators.validate_name(
        "John Doe"
    )

    print(
        f"\nName: {valid}"
    )

    if message:
        print(message)

    # ---------------------------------------------------------
    # Email
    # ---------------------------------------------------------

    valid, message = Validators.validate_email(
        "john@example.com"
    )

    print(
        f"Email: {valid}"
    )

    if message:
        print(message)

    # ---------------------------------------------------------
    # Phone
    # ---------------------------------------------------------

    valid, message = Validators.validate_phone(
        "9876543210"
    )

    print(
        f"Phone: {valid}"
    )

    if message:
        print(message)

    # ---------------------------------------------------------
    # Book ID
    # ---------------------------------------------------------

    valid, message = Validators.validate_book_id(
        101
    )

    print(
        f"Book ID: {valid}"
    )

    if message:
        print(message)

    # ---------------------------------------------------------
    # Year
    # ---------------------------------------------------------

    valid, message = Validators.validate_year(
        2024
    )

    print(
        f"Year: {valid}"
    )

    if message:
        print(message)

    # ---------------------------------------------------------
    # Date
    # ---------------------------------------------------------

    valid, message = Validators.validate_date(
        "2026-09-23"
    )

    print(
        f"Date: {valid}"
    )

    if message:
        print(message)

    # ---------------------------------------------------------
    # Complete Book Validation
    # ---------------------------------------------------------

    valid, errors = Validators.validate_book_data(
        101,
        "Python Programming",
        "John Smith",
        2024,
        "Programming",
        5
    )

    print(
        f"\nComplete Book Validation: {valid}"
    )

    if errors:

        for error in errors:
            print(
                f"- {error}"
            )

    # ---------------------------------------------------------
    # Complete Member Validation
    # ---------------------------------------------------------

    valid, errors = Validators.validate_member_data(
        1,
        "John Doe",
        "john@example.com",
        "9876543210"
    )

    print(
        f"\nComplete Member Validation: {valid}"
    )

    if errors:

        for error in errors:
            print(
                f"- {error}"
            )

    print("\n")
    print("=" * 60)
    print("VALIDATOR TEST COMPLETED")
    print("=" * 60)"""