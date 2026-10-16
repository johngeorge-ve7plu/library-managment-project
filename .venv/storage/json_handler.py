import json
import os

from models.book import Book
from models.member import Member
from models.borrow_records import BorrowRecord

class JSONHandler:
    def __init__(self):
        self.data_directory = "data"
        self.books_file = os.path.join(self.data_directory, "books.json")
        self.members_file = os.path.join(self.data_directory, "members.json")
        self.borrow_records_file = os.path.join(self.data_directory, "borrow_records.json")

        self.initialize_storage()
    def initialize_storage(self): 
        #create the json file for books, members, and borrow records if they don't exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        files = [
            self.books_file,
            self.members_file,
            self.borrow_records_file
        ]
        for file in files:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    json.dump([], f, indent=4)
        
    def read_json(self, file_path):
        try:
            with open(file_path,"r", encoding="utf-8") as file:#utf stands for unicode transformation format 8 bit
                data = json.load(file)
                return data
        
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        
        except json.JSONDecodeError:
            print(f"invalid json found in file: {file_path}")
            return []
        except Exception as error:
            print(f"An error occurred while reading the file: {file_path}. Error: {error}")
            return []
    
    def write_json(self, file_path, data):
        try:
            with open(file_path, "w",encoding = "utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as error:
            print(f"An error occurred while writing to the file: {file_path}. Error: {error}")
    
    def clear_file(self, flie_path):
        self.write_json(flie_path, [])

    def file_exist(self, file_path):
        return os.path.exists(file_path)
    
    def get_record_count(self, file_path):
        data = self.read_json(file_path)
        return len(data)
    
    def display_storage_info(self):
        print("=" * 60)
        print("STORAGE INFORMATION")
        print("=" * 60)
        print(f"Books File           : {self.books_file}")
        print(f"Members File         : {self.members_file}")
        print(f"Borrow Records File  : {self.borrow_records_file}")
        print(f"books stored         :{self.get_record_count(self.books_file)}")
        print(f"members stored       :{self.get_record_count(self.members_file)}")
        print(f"borrow records stored:{self.get_record_count(self.borrow_records_file)}")
        print("=" * 60)
    

    # book operations
    def save_books(self,books):
        try:
            book_data = []
            for book in books:
                book_data.append(book.to_dict())
            self.write_json(self.books_file, book_data)
            return True
        except Exception as error:
            print(f"An error occurred while saving books: {error}")
            return False
    def load_books(self):
        try:
            data = self.read_json(self.books_file)
            books = []
            for item in data:
                books.append(Book.from_dict(item))
            return books
        except Exception as error:
            print(f"An error occurred while loading books: {error}")
            return []
    
    #member operations
    def save_members(self,members):
        try:
            member_data = []
            for member in members:
                member_data.append(member.to_dict())
            self.write_json(self.members_file, member_data)
            return True
        except Exception as error:
            print(f"An error occurred while saving members: {error}")
            return False
    def load_members(self):
        try:
            data = self.read_json(self.members_file)
            members = []
            for item in data:
                members.append(Member.from_dict(item))
            return members
        except Exception as error:
            print(f"An error occurred while loading members: {error}")
            return []
    
    #borrow records operations
    def save_borrow_records(self,borrow_records):
        try:
            borrow_data = []
            for record in borrow_records:
                borrow_data.append(record.to_dict())
            self.write_json(self.borrow_records_file, borrow_data)
            return True
        except Exception as error:
            print(f"An error occurred while saving borrow records: {error}")
            return False
    def load_borrow_records(self):
        try:
            data = self.read_json(self.borrow_records_file)
            borrow_records = []
            for item in data:
                borrow_records.append(BorrowRecord.from_dict(item))
            return borrow_records
        except Exception as error:
            print(f"An error occurred while loading borrow records: {error}")
            return []
        
    #load everything
    def load_all_data(self):
        return {
            "books": self.load_books(),
            "members": self.load_members(),
            "borrow_records": self.load_borrow_records()
        }
    #save everything
    def save_all_data(self,books,members,borrow_records):
        self.save_books(books)
        self.save_members(members)
        self.save_borrow_records(borrow_records)
        print("\n All data saved successfully.")

    #backup operations
    def create_backup(self):
        backup_directory = os.path.join(self.data_directory, "backup")
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)
        files = [
            self.books_file,
            self.members_file,
            self.borrow_records_file
        ]
        for file in files:
            file_name = os.path.basename(file)
            backup_file = os.path.join(backup_directory, file_name)
            data = self.read_json(file)
            self.write_json(backup_file, data)
            print("backup created successfully")
    #reset database
    def reset_database(self):
        self.clear_file(self.books_file)
        self.clear_file(self.members_file)
        self.clear_file(self.borrow_records_file)
        print("Database has been reset")
    #database statistics
    def database_statistics(self):
        return{
            "total_books": self.get_record_count(self.books_file),
            "total_members": self.get_record_count(self.members_file),
            "total_borrow_records": self.get_record_count(self.borrow_records_file)
        }
    ######################################################################
    #display database statistics
    def display_database_statistics(self):
        stats  = self.database_statistics()
        print("=" * 60)
        print("DATABASE STATISTICS")
        print("=" * 60)
        print(f"Total Books         : {stats['total_books']}")
        print(f"Total Members       : {stats['total_members']}")
        print(f"Total Borrow Records: {stats['total_borrow_records']}")
        print("=" * 60)
    # check storage status
    def storaage_exists(self):
        return(
            self.file_exist(self.books_file) and
            self.file_exist(self.members_file) and
            self.file_exist(self.borrow_records_file)
        )
    #export all data
    def export_all_data(self):
        return{
            "books":self.read_json(self.books_file),
            "members":self.read_json(self.members_file),
            "borrow_records":self.read_json(self.borrow_records_file)
        }
    #import all data
    def import_all_data(self, data):
        self.write_json(self.books_file, data.get("books", []))
        self.write_json(self.members_file, data.get("members", []))
        self.write_json(self.borrow_records_file, data.get("borrow_records", []))
        print("All data imported successfully.")