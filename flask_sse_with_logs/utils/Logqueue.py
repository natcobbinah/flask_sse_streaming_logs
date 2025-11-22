from .IQeue import QueueInterface
from collections import deque
from typing import Union

class LogQueue(QueueInterface):

    def __init__(self):
        self.queue = deque([])

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def size(self) -> int:
        return len(self.queue)

    def peek(self) -> Union[str, None]:
        if self.size() > 0:
            return self.queue[0]
        return None

    def peekAtIndex(self, index) -> Union[str, None]:
        if index < self.size():
            return self.queue[index]
        return None
    
    def enqueue(self, item):
        self.queue.append(item)
    
    def dequeue(self)-> Union[str, None]:
        if self.size() > 0:
            return self.queue.popleft()
        return None

    def dequeueAtIndex(self, index)-> Union[str, None]:
        if index < self.size():
            self.queue.__delitem__(index)
        return None