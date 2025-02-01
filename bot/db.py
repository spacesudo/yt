import sqlite3


class User:
    def __init__(self, dbname = "users.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)


    def setup(self):
        statement1 = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, chatid INTEGER UNIQUE, currency TEXT DEFAULT 'ETH' , wallet TEXT DEFAULT '0X123456' , network TEXT DEFAULT 'ETH' )"
        self.conn.execute(statement1)
        self.conn.commit()


    def add_user(self, username_):
        statement = "INSERT OR IGNORE INTO users (chatid) VALUES (?)"
        args = (username_,)
        self.conn.execute(statement, args)
        self.conn.commit()
    

    def update_network(self, amount, userid):
        statement = "UPDATE users SET network = ? WHERE chatid = ?"
        args = (amount, userid)
        self.conn.execute(statement, args)
        self.conn.commit()
        
        
        
    def get_network(self, owner):
        statement = "SELECT network FROM users WHERE chatid = ?"
        args = (owner,)
        cursor = self.conn.execute(statement, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    
    
    def get_wallet(self, owner):
        statement = "SELECT wallet FROM users WHERE chatid = ?"
        args = (owner,)
        cursor = self.conn.execute(statement, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    
    
    def update_wallet(self, amount, userid):
        statement = "UPDATE users SET wallet = ? WHERE chatid = ?"
        args = (amount, userid)
        self.conn.execute(statement, args)
        self.conn.commit()
    
    
    def get_currency(self, owner):
        statement = "SELECT currency FROM users WHERE chatid = ?"
        args = (owner,)
        cursor = self.conn.execute(statement, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    
    
    def update_currency(self, amount, userid):
        statement = "UPDATE users SET currency = ? WHERE chatid = ?"
        args = (amount, userid)
        self.conn.execute(statement, args)
        self.conn.commit()


    def get_users(self):
        statement = "SELECT chatid FROM users"
        return [x[0] for x in self.conn.execute(statement)]


class Mortage:
    
    def __init__(self, dbname="mortages.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        
    def setup(self):
        statement = "CREATE TABLE IF NOT EXISTS mortages (owner TEXT, percentage INTEGER NULL, time INTEGER NULL, contract_address TEXT)"
        self.conn.execute(statement)
        self.conn.commit()
        
    def add_mortage(self, owner, contract_address, percentage = None, time = None):
        try:
            statement = "INSERT INTO mortages (owner, percentage, time , contract_address) VALUES (?, ?, ?, ?)"
            args = (owner, percentage, time , contract_address)
            self.conn.execute(statement, args)
            self.conn.commit()
        except Exception as e:
            return e
    
    def retrieve_last_ca(self, owner):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT contract_address FROM mortages WHERE owner = ? ORDER BY ROWID DESC LIMIT 1''', (owner,))
            last_ca = cursor.fetchone()
            if last_ca:
                return last_ca[0]
            else:
                return None
        except Exception as e:
            return e
        
    def retrieve_last_percentage(self, owner):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT percentage FROM mortages WHERE owner = ? ORDER BY ROWID DESC LIMIT 1''', (owner,))
            last_percentage = cursor.fetchone()
            if last_percentage:
                return last_percentage[0]
            else:
                return None
        except Exception as e:
            return e
        
        
    def retrieve_last_time(self, owner):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT time FROM mortages WHERE owner = ? ORDER BY ROWID DESC LIMIT 1''', (owner,))
            last_percentage = cursor.fetchone()
            if last_percentage:
                return last_percentage[0]
            else:
                return None
        except Exception as e:
            return e

    def update_mortage(self, owner, contract_address, percentage, time):
        try:
            statement = "UPDATE mortages SET percentage=?, time =? WHERE owner=? AND contract_address=?"
            args = (percentage, time , owner, contract_address)
            self.conn.execute(statement, args)
            self.conn.commit()
            return "mortage updated successfully"
        except Exception as e:
            return e

    def get_all_mortages(self, owner):
        statement = "SELECT owner, percentage, time , contract_address FROM mortages WHERE owner = (?)"
        args = (owner,)
        return [x for x in self.conn.execute(statement, args)]


class Referrals:
    
    def __init__(self, dbname = "referrals.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)


    def setup(self):
        statement1 = """CREATE TABLE IF NOT EXISTS referrals (id INTEGER PRIMARY KEY, chatid INTEGER UNIQUE, referrals INTEGER DEFAULT 0)"""
                            
        self.conn.execute(statement1)
        self.conn.commit()


    def add_user(self, username_, referrer):
        statement = "INSERT OR IGNORE INTO referrals (chatid, referrer) VALUES (?, ?, ?)"
        args = (username_, referrer)
        self.conn.execute(statement, args)
        self.conn.commit()
        
        
    def update_referrals(self, amount, userid):
        statement = "UPDATE referrals SET referrals = ? WHERE chatid = ?"
        args = (amount, userid)
        self.conn.execute(statement, args)
        self.conn.commit()
        
        
        
    def get_referrals(self, owner):
        statement = "SELECT referrals FROM referrals WHERE chatid = ?"
        args = (owner,)
        cursor = self.conn.execute(statement, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    
    
    
    def get_users(self):
        statement = "SELECT chatid, wallet, referrer, referrals, referrals_vol, trading_vol FROM referrals"
        return [x for x in self.conn.execute(statement)]