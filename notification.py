import Pyro4
import time


# creating notification process class

class notification_process:
    def __init__(self):
        a = 10


# main function

def main():
    #notification_process: "notification process starting"
    URI = "PYRO:karthik.com@localhost:5000"  # connecting through rpc
    rm = Pyro4.Proxy(URI)  # calling proxy server using defined uri
    while True:
        Message_Queues = rm.getProcessForMe("NOTIFICATION", "APPROVED")  # call from msq server
        Message_Que = rm.getProcessForMe("NOTIFICATION", "NOT APPROVED")  # call from msq server
        if Message_Queues is not None or Message_Que is not None:
            if Message_Queues is not None:
                rm.removeFromList(Message_Queues[0], Message_Queues[1],
                                  Message_Queues[2])  # call to delete values from the list
                print(Message_Queues[0] + " " + Message_Queues[1] + " " + Message_Queues[2])
            if Message_Que is not None:
                rm.removeFromList(Message_Que[0], Message_Que[1], Message_Que[2])  # call to delete values from the List
                print(Message_Que[0] + " " + Message_Que[1] + " " + Message_Que[2])
        else:
            print("No message found....")
            time.sleep(7)  # giving sleep time of 7 seconds to wait for data


if __name__ == "__main__":
    main()
