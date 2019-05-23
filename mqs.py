import sqlite3
import Pyro4


# Declaring global variables to use inside all the classes

Message_Queue = []
field = 'Name'
column1 = 'Course'
column2 = 'Decision'
file_name = 'mqs.sqlite'
table_name = 'mqs'
field_type = 'VARCHAR'


class newClass:
    def __init__(self, user_name, user_course, user_decision):
        self.user_name = user_name  # Declaring variables corresponding to class instance
        self.user_course = user_course
        self.user_decision = user_decision

    def input_user_name(self):
        return self.user_name  # Function to return name value

    def input_user_course(self):
        return self.user_course  # Function to return course value

    def input_user_decision(self):
        return self.user_decision  # Function to return decision value

    def save_user_decision(self, user_decision):
        self.user_decision = user_decision  # Function to set decision value

    def save_user_name(self, user_name):
        self.user_name = user_name  # Function to set name value

    def save_user_course(self, user_course):
        self.user_course = user_course  # Function to set course value


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class db(object):
    def __init__(self):
        print("starting server")
        self.s1 = sqlite3.connect(file_name)  # starting sqlite3 connection
        self.s1 = sqlite3.connect(file_name)
        cursor_obj = self.s1.cursor()  # creating sqlite3 cursor object
        temp = cursor_obj.execute("SELECT * FROM " + table_name).fetchall()  # Querying the database to fetch all values from the table
        cursor_obj.execute("SELECT * FROM " + table_name)
        if (
                temp.__sizeof__() > 0):  # looping through the data to insert values into the list that are present in the db when server starts again.
            for Message_Queues in cursor_obj:
                Message_Queue.append(newClass(Message_Queues[0], Message_Queues[1], Message_Queues[2]))
        else:
            return

    # Function to remove values from database and list when data is printed in notification module.

    def removeFromList(self, arg1, arg2, arg3):
        self.s1 = sqlite3.connect(file_name)  # starting sqlite3 connection
        cursor_obj = self.s1.cursor()  # creating sqlite3 cursor object
        cursor_obj.execute("DELETE FROM " + table_name + " WHERE Name = (?) AND Course = (?) AND Decision = (?)",
                           (arg1, arg2, arg3))  # Querying the database to select the values
        self.s1.commit()  # committing the database
        for Message_Queues in cursor_obj:
            print(Message_Queues[1])
        self.s1.close()
        for i in range(0, len(Message_Queue)):  # looping though the list to delete the values
            s2 = Message_Queue.pop(i)
            print(s2.input_user_name())
            if s2.input_user_name() == arg1:
                if s2.input_user_course() == arg2:
                    return
                else:
                    Message_Queue.insert(i, s2)
            else:
                Message_Queue.insert(i, s2)

    # Function to select data from db which has decision as not processed

    def getProcessForMe(self, data, ProcessName):
        self.s1 = sqlite3.connect(file_name)  # starting sqlite3 connection
        cursor_obj = self.s1.cursor()  # creating sqlite3 cursor object
        cursor_obj.execute("SELECT * FROM " + table_name + " WHERE Decision = (?)",
                           (ProcessName,))  # querying the database to select data which has decision has unprocessed
        for Message_Queues in cursor_obj:  # looping through the database object to store the values fetched in list
            self.s1.close()
            return Message_Queues
        return None

    # Function to insert values into the database and list

    def insert_into_db(self, arg1, arg2, arg3):
        self.s1 = sqlite3.connect(file_name)  # starting sqlite3 connection
        cursor_obj = self.s1.cursor()  # creating sqlite3 cursor object
        field_type = "VARCHAR"
        cursor_obj.execute("INSERT INTO " + table_name + " VALUES (?,?,?)",
                           (arg1, arg2, arg3))  # querying the database to insert values fetched into the db
        self.s1.commit()  # committing the database
        self.s1.close()  # closing the db connection
        tempObject = newClass(arg1, arg2, arg3)
        Message_Queue.append(tempObject)  # appending the received values into the list
        # print(len(Message_Queue))

    # Function to fetch the data

    def input_Data(self, arg1):
        print("Get Data")


# main function

def main():
    s = db()
    server_daemon = Pyro4.Daemon(None, 5000, None)  # setting up the daemon connection so that the uri value stays constant
    URI = server_daemon.register(db, "karthik.com")
    print(URI)
    server_daemon.requestLoop()


if __name__ == "__main__":
    main()
