import heapq
from typing import Union, TypeVar

T = TypeVar("T")

"""
Implementation of different queue structures and a stack, methods have been designed according to the needs of the application
"""


class Queue:
    """
    A FIFO queue data structure

    Attributes:
        screen_elements (list): Contains the screen elements relevant to the queue type
    """

    screen_elements = [
        "-queue_demo_enqueue-",
        "-queue_demo_dequeue-",
        "-queue_demo_peek-",
        "-queue_demo_isempty-",
        "-queue_demo_size-",
        "-queue_demo_isfull-",
    ]

    def __init__(self, max_size: int) -> None:
        """
        Initialise the queue with the given maximum size.

        Arguments:
            max_size (int): Maximum size of the queue.
        """
        self.queue = []
        self.max_size = max_size
        self.front = 0
        self.rear = -1

    def enqueue(self, item: T) -> Union[bool, T]:
        """
        Add an item to the rear of the queue.

        Arguments:
            item (T): Item to be added to the queue.

        Returns:
            bool or T: Return False if the queue is full, return enqueued item if not.
        """
        if self.is_full():
            return False
        self.queue.append(item)
        self.rear += 1
        return item

    def dequeue(self) -> Union[bool, T]:
        """
        Remove item from the front of the queue.

        Returns:
            bool or T: Return False if the queue is full, return dequeued item if not.
        """
        if self.is_empty():
            return False
        self.rear -= 1
        return self.queue.pop(0)

    def is_empty(self) -> bool:
        """Check if the queue is empty"""
        return len(self.queue) == 0

    def is_full(self) -> bool:
        """Check if the queue is full"""
        return len(self.queue) == self.max_size

    def peek(self) -> Union[bool, T]:
        """Return the item at the front of the queue, return False if the queue is empty."""
        if self.is_empty():
            return False
        return self.queue[0]

    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self.queue)


class PriorityQueue(Queue):
    """
    A priority queue data structure

    Attributes:
        screen_elements (list): Contains the screen elements relevant to the queue type
    """

    screen_elements = [
        "-queue_demo_enqueue-",
        "-queue_demo_dequeue-",
        "-queue_demo_peek-",
        "-queue_demo_isempty-",
        "-queue_demo_size-",
        "-queue_demo_isfull-",
    ]

    def __init__(self, max_size: int) -> None:
        """
        Initialise the queue with the given maximum size.

        Arguments:
            max_size (int): Maximum size of the queue.
        """
        super().__init__(max_size)

    def enqueue(self, item: str) -> Union[bool, str]:
        """
        Enqueue an item into the priority queue.

        Arguments:
            item (T): The item to be added to the priority queue. It should be a string
                in the format '<priority>-<value>', where '<priority>' is an integer
                representing the priority of the item and '<value>' is the value of the item.

        Returns:
            bool or T: If the queue is full, returns False. Otherwise, returns the enqueued item.
        """
        priority = int(item.split("-")[0])
        if self.is_full():
            return False
        self.rear += 1
        heapq.heappush(self.queue, (priority, item))
        return item

    def dequeue(self) -> Union[bool, str]:
        """
        Dequeue the highest priority item from the queue.

        Returns:
            bool or T: If the queue is empty, returns False. Otherwise, returns the dequeued item.
        """
        if self.is_empty():
            return False
        _, item = heapq.heappop(self.queue)
        self.rear -= 1
        return item

    def peek(self) -> Union[bool, str]:
        """Return False if the queue is empty, otherwise return the highest priority item."""
        if self.is_empty():
            return False
        return f"{self.queue[0][1]} with priority {self.queue[0][0]}"


class CircularQueue(Queue):
    """
    A circular queue data structure

    Attributes:
        screen_elements (list): Contains the screen elements relevant to the queue type
    """

    screen_elements = [
        "-queue_demo_enqueue-",
        "-queue_demo_dequeue-",
        "-queue_demo_peek-",
        "-queue_demo_isempty-",
        "-queue_demo_size-",
        "-queue_demo_isfull-",
        "-queue_demo_rear-",
    ]

    def __init__(self, max_size: int) -> None:
        """
        initialise the queue with the given maximum size.

        Arguments:
            max_size (int): Maximum size of the queue.
        """
        super().__init__(max_size)
        self.queue = [None] * self.max_size
        self.front = self.rear = -1
        self.current_size = 0

    def enqueue(self, item: T) -> Union[bool, T]:
        """
        Enqueue an item into the circular queue.

        Arguments:
            item (T): The item to be added to the circular queue.

        Returns:
            bool or T: If the queue is full, returns False. Otherwise, returns the enqueued item.
        """
        if self.is_full():
            return False
        if self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.max_size
        self.queue[self.rear] = item
        self.current_size += 1
        return item

    def dequeue(self) -> Union[bool, T]:
        """
        Dequeue an item from the circular queue.

        Returns:
            bool or T: If the queue is empty, returns False. Otherwise, returns the dequeued item.
        """
        if self.is_empty():
            return False
        elif self.front == self.rear:
            dequeued_item = self.queue[self.front]
            self.front = self.rear = -1
        else:
            dequeued_item = self.queue[self.front]
            self.front = (self.front + 1) % self.max_size
        self.current_size -= 1
        return dequeued_item

    def size(self) -> int:
        """Return the amount of items in the circular queue"""
        return self.current_size

    def is_full(self) -> bool:
        """Return True if the queue is full, otherwise return False"""
        return self.current_size == self.max_size

    def is_empty(self) -> bool:
        """Return True if the queue is empty, otherwise return False"""
        return self.current_size == 0

    def peek(self) -> Union[bool, T]:
        """If the queue is empty, return False, otherwise return the item at the front of the circular queue."""
        if self.is_empty():
            return False
        return self.queue[self.front % self.max_size]

    def rear_item(self) -> Union[bool, T]:
        """If the queue is empty, return False, otherwise return the item at the rear of the circular queue."""
        if self.is_empty():
            return False
        return self.queue[self.rear]


class Stack:
    """
    A stack data structure.

    Attributes:
        screen_elements (list): Contains the screen elements relevant to the queue type.
    """

    screen_elements = [
        "-queue_demo_push-",
        "-queue_demo_pop-",
        "-queue_demo_peek-",
        "-queue_demo_isempty-",
        "-queue_demo_isfull-",
        "-queue_demo_size-",
    ]

    def __init__(self, max_size: int) -> None:
        """
        Initialise the stack with the given maximum size.

        Arguments:
            max_size (int): Maximum size of the stack.
        """
        self.stack = []
        self.max_size = max_size

    def push(self, item: T) -> Union[bool, T]:
        """
        Pushes an item to the top of the stack.

        Arguments:
            item (T): The item to be added to the stack.

        Returns:
            bool or T: If the stack is full, returns False. Otherwise, returns the pushed item.
        """
        if self.is_full():
            return False
        self.stack.append(item)
        return item

    def pop(self) -> Union[bool, T]:
        """
        Remove the top item in the stack.

        Returns:
            bool or T: If the stack is empty, returns False. Otherwise, returns the popped item.
        """
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self) -> Union[bool, T]:
        """If the stack is empty, return False, otherwise return the item at the top of the stack."""
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_full(self) -> bool:
        """Return True if the stack is full, otherwise return False."""
        return len(self.stack) == self.max_size

    def is_empty(self) -> bool:
        """Return True if the stack is empty, otherwise return False."""
        return len(self.stack) == 0

    def size(self) -> int:
        """Return the amount of items in the stack."""
        return len(self.stack)

    @property
    def front(self) -> int:
        """Return the index pointing to the front of the stack"""
        return (self.max_size - 1) - (len(self.stack) - 1)

    @property
    def queue(self) -> list[T]:
        """Return a list representation of the stack, shifted such that the rear is in the final index position"""
        padding_size = max(0, self.max_size - len(self.stack))
        stack_inverse = [None] * padding_size + self.stack[::-1]
        return stack_inverse
