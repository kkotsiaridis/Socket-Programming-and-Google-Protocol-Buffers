#!/usr/bin/env python3

import socket
import time
import os
from protocolBuffers import project2021_ece441_pb2

HOST = '194.177.207.90'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
TEAM_ID = 26

CLIENT_MAC = '00:0c:29:63:b3:25'
CLIENT_IP = '192.168.2.1'

counter = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    send_message  = project2021_ece441_pb2.project_message()
    send_message.conn_req_msg.header.id = TEAM_ID

    student1 = send_message.conn_req_msg.student.add()
    student1.aem = 2547
    student1.name = "Konstantinos"
    student1.email = "kkotsiaridis@uth.gr"

    student2 = send_message.conn_req_msg.student.add()
    student2.aem = 2577
    student2.name = "Vangelis"
    student2.email = "evabakas@uth.gr"

    pkt = send_message.SerializeToString()
    print("Sending--> conn Request\n")
    s.sendall(pkt)

    interval = -1
    current_time = int(time.perf_counter())
    last_hello = current_time + 50000000

    recieved_data = s.recv(1024)

    msg = project2021_ece441_pb2.project_message()
    msg.ParseFromString(recieved_data)

    msg_type = msg.WhichOneof("msg")

    if(msg_type == "conn_resp_msg"):
        print("Con Response from server\n")
        print(msg)

        interval = msg.conn_resp_msg.interval
        print(interval)
        current_time = int(time.perf_counter())
        last_hello = current_time

        send_message  = project2021_ece441_pb2.project_message()
        send_message.hello_msg.header.id = TEAM_ID

        pkt = send_message.SerializeToString()
        print("Sending--> Hello Message\n")
        s.sendall(pkt)

        recieved_data = s.recv(1024)

        msg = project2021_ece441_pb2.project_message()
        msg.ParseFromString(recieved_data)

        msg_type = msg.WhichOneof("msg")
        if(msg_type == "hello_msg"):
            print("Hello Message from server\n")
            print(msg)
    

    while True:
        current_time = int(time.perf_counter())
        
        if(current_time - last_hello > interval):
            counter = counter + 1
            last_hello = current_time

            send_message  = project2021_ece441_pb2.project_message()
            send_message.hello_msg.header.id = TEAM_ID

            pkt = send_message.SerializeToString()
            print("Sending--> Hello Message\n")
            s.sendall(pkt)

            recieved_data = s.recv(1024)
            if not recieved_data:
                    break

            msg = project2021_ece441_pb2.project_message()
            msg.ParseFromString(recieved_data)

            msg_type = msg.WhichOneof("msg")
            if(msg_type == "hello_msg"):
                print("Hello Message from server\n")
                print(msg)



        if counter == 3:  #netsat sequence
            counter = counter + 1
            send_message  = project2021_ece441_pb2.project_message()
            send_message.netstat_req_msg.header.id = TEAM_ID

            student1 = send_message.netstat_req_msg.student.add()
            student1.aem = 2547
            student1.name = "Konstantinos"
            student1.email = "kkotsiaridis@uth.gr"

            student2 = send_message.netstat_req_msg.student.add()
            student2.aem = 2577
            student2.name = "Vangelis"
            student2.email = "evabakas@uth.gr"

            pkt = send_message.SerializeToString()
            print("---Sending--> Netstat Request---\n")
            s.sendall(pkt)

            recieved_data = s.recv(1024)
            if not recieved_data:
                    break

            msg = project2021_ece441_pb2.project_message()
            msg.ParseFromString(recieved_data)

            msg_type = msg.WhichOneof("msg")
            print(msg)
            if(msg_type == "netstat_resp_msg"):
                print("---Netstat response from server---\n")

                send_message = project2021_ece441_pb2.project_message()
                send_message.netstat_data_msg.header.id = TEAM_ID

                send_message.netstat_data_msg.direction = 1
                send_message.netstat_data_msg.mac_address = CLIENT_MAC
                send_message.netstat_data_msg.ip_address = CLIENT_IP

                pkt = send_message.SerializeToString()
                print("---Sending--> Netstat Data---\n")
                print(send_message)
                s.sendall(pkt)

                recieved_data = s.recv(1024)
                if not recieved_data:
                    break

                msg = project2021_ece441_pb2.project_message()
                msg.ParseFromString(recieved_data)
                
                msg_type = msg.WhichOneof("msg")

                if(msg_type == "netstat_data_ack_msg"):
                    print("---Netstat data ack from server---\n")
                    print(msg)

        if counter == 6:
            counter = 0
            send_message = project2021_ece441_pb2.project_message()
            send_message.netmeas_req_msg.header.id = TEAM_ID

            student1 = send_message.netmeas_req_msg.student.add()
            student1.aem = 2547
            student1.name = "Konstantinos"
            student1.email = "kkotsiaridis@uth.gr"

            student2 = send_message.netmeas_req_msg.student.add()
            student2.aem = 2577
            student2.name = "Vangelis"
            student2.email = "evabakas@uth.gr"

            pkt = send_message.SerializeToString()
            print("+++++Sending--> Netmeas Request+++++\n")
            s.sendall(pkt)

            recieved_data = s.recv(1024)
            if not recieved_data:
                    break

            msg = project2021_ece441_pb2.project_message()
            msg.ParseFromString(recieved_data)
                
            msg_type = msg.WhichOneof("msg")

            if(msg_type == "netmeas_resp_msg"):
                print("+++++Netmeas response from server+++++\n")

                iperf_port = msg.netmeas_resp_msg.port
                iperf_interval = msg.netmeas_resp_msg.interval
                
                print("iperf -c %s -p %d -t %d "%(HOST, iperf_port, iperf_interval))
                
                os.system("iperf -c %s -p %d -t %d > test.txt"%(HOST, iperf_port, iperf_interval))

                f = open("test.txt", "r")
                for x in range(6):
                    f.readline()
                line = f.readline()
                f.close()
                elements = line.split(' ')
                if not elements:
                    print("List is empty")
                    bandwidth = 0
                else:
                    bandwidth = float(elements[-2])

                send_message = project2021_ece441_pb2.project_message()
                send_message.netmeas_data_msg.header.id = TEAM_ID
                
                send_message.netmeas_data_msg.header.type = 9
                send_message.netmeas_data_msg.direction = 1
                send_message.netmeas_data_msg.report = bandwidth
                
                pkt = send_message.SerializeToString()
                print("+++++Sending--> Netmeas Data+++++\n")
                s.sendall(pkt)

                recieved_data = s.recv(1024)
                if not recieved_data:
                    break

                msg = project2021_ece441_pb2.project_message()
                msg.ParseFromString(recieved_data)
                    
                msg_type = msg.WhichOneof("msg")

                if(msg_type == "netmeas_data_ack_msg"):
                    print("+++++Netmeas data ack from server+++++\n")
                    print(msg)
        

        


        





       

           




    
    





