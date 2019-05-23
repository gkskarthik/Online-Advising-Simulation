import Pyro4
import time
import random


# creating advisor process class

class advisor_process:
    def __init__(self):
        a = 10


# main function

def main():
    # advisor_process: "advisor process starting"
    URI = "PYRO:karthik.com@localhost:5000"
    rm = Pyro4.Proxy(URI)
    while True:
        Message_Queues = rm.getProcessForMe("GUIDE", "NOT PROCESSED")  # call from msq server to get values
        if Message_Queues is not None:
            rm.removeFromList(Message_Queues[0], Message_Queues[1], Message_Queues[2])
            random_value = random.randint(1, 10)  # randomly generating decision
            if random_value % 2 == 0:
                Message_Queues = [Message_Queues[0], Message_Queues[1], "APPROVED"]
            else:
                Message_Queues = [Message_Queues[0], Message_Queues[1], "NOT APPROVED"]
            print(Message_Queues[0] + " " + Message_Queues[1] + " " + Message_Queues[2] + "\n")  # printing the decision in advisor module
            rm.insert_into_db(Message_Queues[0], Message_Queues[1], Message_Queues[2])  # call from mqs to insert decision into list
        else:
            print("No message found....")
            time.sleep(3)  # wait for data


if __name__ == "__main__":
    main()
