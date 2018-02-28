import sqlite3


class DBHelper:

    def __init__(self, dbname="servicebot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        tblstmt2 = "CREATE TABLE IF NOT EXISTS cases (ticket_no number, log_date text, owner text, subject text, detail text,assignee text, department text, owner_fname text, owner_lname text, owner_phn text, owner_email text, owner_loc text, priority number)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(tblstmt2)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def delete_chat(self,owner):
        #stmt = "UPDATE items SET description = '' WHERE owner = (?)"
        stmt = "DELETE FROM items WHERE owner = (?)"
        args = (owner,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_case(self,ticket_no):
        #stmt = "UPDATE items SET description = '' WHERE owner = (?)"
        stmt = "DELETE FROM cases WHERE ticket_no = (?)"
        args = (ticket_no,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_case_subject(self,ticket_no, text, chat, firstName, lastName, date_today):
        stmt = "INSERT into cases (ticket_no,log_date, owner, subject, owner_fname, owner_lname) values (?,?,?,?,?,?)"
        args = (ticket_no,date_today,chat,text,firstName,lastName)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_case_subject(self,ticket_no ,chat, date_today):
        stmt = "select * from cases where log_date = (?) and owner = (?) and ticket_no = (?)"
        args = (date_today,chat,ticket_no)
        result = [x for x in self.conn.execute(stmt, args)]
        #print(result)
        return result

    def get_case_department(self,ticket_no ,chat):
        stmt = "select department from cases where owner = (?) and ticket_no = (?)"
        args = (chat,ticket_no)
        result = [x for x in self.conn.execute(stmt, args)]
        #print(result)
        return result[0]

    def delete_invalid_cases(self,chat):
        stmt = "delete from cases where (subject is NULL or (owner_phn is null and owner_loc is null)) and owner = (?)"
        args = (chat,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def update_case_detail(self,text, chat, date_today,ticket_no,department):
        stmt = "update cases set detail = (?),department = (?) where owner = (?) and log_date = (?) and ticket_no = (?)"
        args = (text,department,chat,date_today,ticket_no)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def update_case_phn_loc(self,phn,loc, chat, date_today,assignee,ticket_no):
        stmt = "update cases set owner_phn = (?), owner_loc = (?), assignee = (?) where owner = (?) and log_date = (?) and ticket_no = (?)"
        args = (phn,loc,assignee,chat,date_today,ticket_no)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_pending_case(self,chat):
        stmt = "select * from cases where owner = (?)"
        args = (chat,)
        result = [x for x in self.conn.execute(stmt, args)]
        #print(result)
        return result

    def update_priority(self,chat,priority,ticket_no):
        stmt = "update cases set priority = (?) where owner = (?) and ticket_no = (?)"
        args = (priority,chat,ticket_no)
        self.conn.execute(stmt, args)
        self.conn.commit()
