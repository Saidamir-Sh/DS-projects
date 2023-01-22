import threading

class Semaphore:
    def __init__(self, value):
        self.value = value
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def up(self):
        with self.condition:
            self.value += 1
            self.condition.notify()

    def down(self):
        with self.condition:
            while self.value <= 0:
                self.condition.wait()
            self.value -= 1

class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []
        self.mutex = Semaphore(1)
        self.empty_slots = Semaphore(size)
        self.full_slots = Semaphore(0)

    def insert(self, item):
        self.empty_slots.down()
        self.mutex.down()
        self.buffer.append(item)
        self.mutex.up()
        self.full_slots.up()

    def remove(self):
        self.full_slots.down()
        self.mutex.down()
        item = self.buffer.pop(0)
        self.mutex.up()
        self.empty_slots.up()
        return item

def producer(buffer, items):
    for item in items:
        buffer.insert(item)

def consumer(buffer):
    while True:
        item = buffer.remove()
        print(item)

buffer = Buffer(5)
producer_thread = threading.Thread(target=producer, args=(buffer, range(10)))
consumer_thread = threading.Thread(target=consumer, args=(buffer,))
producer_thread.start()
consumer_thread.start()
producer_thread.join()
consumer_thread.join()
