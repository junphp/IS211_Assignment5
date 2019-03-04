#import Queue # As previously defined
#import random
# Completed program for the printer simulation

import random
import argparse
import urllib2
import csv
'''
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) -1]

    def size(self):
        return len(self.items)
'''
"""
 instance Queue class
"""
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    #check list value for test purpose
    def showlist(self):
        return self.items
"""
 instance Server class
"""
class Server:
    def __init__(self):
        #self.page_rate = ppm
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
        if self.time_remaining <= 0:
            self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_process()
"""
 instance Request class
"""
class Request:
    def __init__(self, time, process):
        self.timestamp = int(time)
        self.process = int(process)

    def get_stamp(self):
        return self.timestamp

    def get_process(self):
        return self.process

    def wait_time(self):
        return self.timestamp - self.process
'''
 open url and return data object
'''
def downloadData(url):
    url = urllib2.urlopen(url)
    return url

'''
 processing request with one server
'''
def simulateOneServer(csvData):
    server = Server()
    queue = Queue()
    waiting_times = []
    #csvData = [next(csvData) for x in xrange(10)]
    for x in csvData:
        task = Request(x[0], x[2])
        queue.enqueue(task)
        if (not server.busy()) and (not queue.is_empty()):
            next_task = queue.dequeue()
            waiting_times.append(next_task.wait_time())
            server.start_next(next_task)
        server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining." % (average_wait, queue.size()))

'''
 processing requests with multiple servers
'''
def simulateManyServers(csvData, servers):
    waiting_times = []
    server_list = {} #store mutiple server class instance in dic
    queue_list = {} #store mutiple queue class instance in dic
    count = 0 #literal number for appending dir key name ex) key_01: 0, key_02:1 ..
    remain_count = 0 #totla number for remaining queue job each server
    #csvData = [next(csvData) for x in xrange(10)]
    #instance class each server in dic
    for j in range(servers):
        server_list['server_%s' %j] = Server()
        queue_list['queue_%s' %j] = Queue()

    for x in csvData:
        task = Request(x[0], x[2])
        queue_list['queue_%s'%count].enqueue(task)#insert instance into dic
        if (not server_list['server_%s' %count].busy()) and (not queue_list['queue_%s'%count].is_empty()):
            next_task = queue_list['queue_%s'%count].dequeue()
            waiting_times.append(next_task.wait_time())
            server_list['server_%s' % count].start_next(next_task)
        server_list['server_%s' % count].tick()
        #check dic key name with interal number
        if (len(server_list) - 1) == count:
            count = 0 #if auto increase number has reached to max number of dic length, make it to 0
        else:
            count+=1

    average_wait = sum(waiting_times) / len(waiting_times)
    #count each server has queue take
    for k in queue_list:
        remain_count+=queue_list[k].size()

    print("Average Wait %6.2f secs %3d tasks remaining." % (average_wait, remain_count))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help="read parameter")
    parser.add_argument('--servers', type=int, help="number of servers", default=1)
    args = parser.parse_args()

    url = args.url
    servers = args.servers
    #url = 'https://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'

    try:
        data = downloadData(url)
    except:
        print("Invaild FILE")
        exit()
    else:
        csvData = csv.reader(data)
        #if second parameter is exist and greater then 1
        if servers>1:
            simulateManyServers(csvData,servers)
        else:
            simulateOneServer(csvData)

main()
