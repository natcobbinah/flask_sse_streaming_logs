from abc import ABC, abstractmethod

class QueueInterface(ABC):
    """
    Abstract class: QueueInterface

    ...
    Methods
    is_empty(self):
        checks if queue is empty
    size(self):
        returns the length of the queue
    peek(self):
        view the top element in-front of the queue without dequeueing it
    peekAtIndex(self, index):
        view element in queue at specified index without dequeueing it
    enqueue(self, item)
        add element to the queue
    dequeue(self)
        remove element from queue
    dequeueAtIndex(self, index)
        remove element from queue at specified index
    """

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def peek(self):
        pass

    @abstractmethod
    def peekAtIndex(self, index):
        pass
    
    @abstractmethod
    def enqueue(self, item):
        pass
    
    @abstractmethod
    def dequeue(self):
        pass

    @abstractmethod
    def dequeueAtIndex(self, index):
        pass