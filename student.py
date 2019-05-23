import Pyro4


# creating student class

class student_process:
    def __init__(self):
        a = 10

# main function

def main():
    # student_process: "student process starting"
    URI = "PYRO:karthik.com@localhost:5000"  # connecting
    rm = Pyro4.Proxy(URI)  # calling proxy server using defined uri
    while True:
        name = input("Student's name : ")  # getting input from user
        course = input("Student's Course : ")
        rm.insert_into_db(name, course, "NOT PROCESSED")  # perfoming call from msq


if __name__ == "__main__":
    main()
