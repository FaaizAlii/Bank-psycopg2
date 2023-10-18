import random
import psycopg2 as pg2
from config import config


class User:
    @staticmethod
    def menu():
        print("\npress 1 to create account")
        print("press 2 to show details")
        print("press 3 to Delete account")
        print("press 4 to Deposit")
        print("press 5 to Withdraw")
        print("press 6 to Transfer")
        print("press 9 to Show all accounts")
        print("press 0 to exit")

    @staticmethod
    def id_generator():
        id = random.randint(1000,9999)
        cur.execute("select * from customer")
        rows = cur.fetchall()
        for row in rows:
            if row[2] == id:
                id = random.randint(1000,9999)
            else:
                pass
        return id
    
    def get_data(self):
        name = input("Enter your name: ")
        fname = input("Enter your father's name: ")
        id = self.id_generator()
        password = input("Enter your password: ")
        amount = int(input("Enter your initial amount: "))
        cur.execute("INSERT INTO customer(name,father_name,id,password,amount) VALUES(%s,%s,%s,%s,%s)",(name,fname,id,password,amount))

        conn.commit()
        print("\nAcount created Successfully!\n")
    
    def del_acc(self):
        id = int(input("Enter your id: "))
        password = input("enter your password: ")
        cur.execute("SELECT * FROM customer")
        rows = cur.fetchall()
        match_found = False
        for row in rows:
            if row[2] == id and row[3] == password:
                cur.execute(f"DELETE FROM customer WHERE id = {id}")
                conn.commit()
                print("\nAccount Deleted Successfully\n")
                match_found = True
                break
        if not match_found:
            print("Incorrect Info please check again!")

    def deposit(self):
        cash = int(input("Enter amount to deposit: "))
        id = int(input("Enter your id: "))
        # password = input("enter your password: ")
        cur.execute("SELECT * FROM customer")
        rows = cur.fetchall()
        match_found = False
        for row in rows:
            if row[2] == id:
                dep_cash = row[4] + cash
                cur.execute("UPDATE customer SET amount = %s WHERE id = %s", (dep_cash,id))
                conn.commit()
                print("\nCash Deposit Successful\n")
                match_found = True
                break
        if not match_found:
            print("Incorrect Info please check again!")
    
    def withdraw(self):
        cash = int(input("Enter amount to Withdraw: "))
        id = int(input("Enter your id: "))
        password = input("enter your password: ")
        cur.execute("SELECT * FROM customer")
        rows = cur.fetchall()
        match_found = False
        for row in rows:
            if row[2] == id and row[3] == password and row[4] >= cash:
                with_cash = row[4] - cash
                cur.execute("UPDATE customer SET amount = %s WHERE id = %s", (with_cash,id))
                conn.commit()
                print("\nCash Withdraw Successful\n")
                match_found = True
                break
        if not match_found:
            print("Incorrect Info please check again!")
    
    def transfer(self):
        cash = int(input("Enter amount to Transfer: "))
        id = int(input("Enter your id: "))
        password = input("enter your password: ")
        rec_id = int(input("Enter receiver id: "))
        cur.execute("SELECT * FROM customer")
        rows = cur.fetchall()
        match_found = False
        for row in rows:
            if row[2] == id and row[3] == password and row[4] >= cash:
                with_cash = row[4] - cash
                cur.execute(f"UPDATE customer SET amount = {with_cash} WHERE id = {id}")
                conn.commit()
                match_found = True
                break
        if not match_found:
            print("Incorrect Info please check again!")
        else:
            for row in rows:
                if row[2] == rec_id:
                    with_cash = row[4] + cash
                    cur.execute(f"UPDATE customer SET amount = {with_cash} WHERE id = {rec_id}")
                    conn.commit()
                    print("\nTransfer Successful\n")
                    break

    @staticmethod
    def show_data():
        id = int(input("Enter your id: "))
        password = input("enter your password: ")
        cur.execute("SELECT * FROM customer")
        rows = cur.fetchall()
        confirm = False
        for row in rows:
            if row[2] == id and row[3] == password:
                print(f"Name         :{row[0]}")
                print(f"Father name  :{row[1]}")
                print(f"Id           :{row[2]}")
                print(f"Password     :{row[3]}")
                print(f"Cash         :{row[4]}")
                confirm = True
                break
            else:
                confirm = False
        if not confirm:
            print("\nIncorrect Info.\n")

            
if __name__ == '__main__':
    while True:
        params = config()
        conn = pg2.connect(**params)
        cur = conn.cursor()

        User.menu()
        choice = int(input("\nchoose: "))
        if choice == 1:
            obj = User()
            obj.get_data()
        elif choice == 2:
            obj = User()
            obj.show_data()
        elif choice == 3:
            obj = User()
            obj.del_acc()
        elif choice == 4:
            obj = User()
            obj.deposit()
        elif choice == 5:
            obj = User()
            obj.withdraw()
        elif choice == 6:
            obj = User()
            obj.transfer()
        elif choice == 0:
            break
        elif choice == 9:
            cur.execute("SELECT * FROM customer")
            rows = cur.fetchall()
            for row in rows:
                print(row)
        else:
            print("\nwrong Choice!\n")
        cur.close()
        conn.close()