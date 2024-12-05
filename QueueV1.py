from typing import Dict, Optional

class EventQueue:

    def __init__(self, depth: int = 1024, safe_mode: bool = True) -> None:
        self.__events: Dict[str, dict] = {}
        self.depth: int = depth
        self.safe_mode: bool = safe_mode

    def insert(self, ID: str, content: Optional[Dict]) -> None:
        """
        Takes a string ID and a dictionary of content that contains the info about said event.
        :param ID:
        :param content:
        :return:
        """
        if not ID or not content:
            raise ValueError('ID and content cannot be empty')

        if not isinstance(ID, str):
            raise TypeError('ID must be a string')

        if not isinstance(content, dict):
            raise TypeError('Content must be a dictionary')

        self.__events[ID] = content

        while len(self.__events) > self.depth:
            # Clears the oldest event in safe mode, otherwise throws error event
            if self.safe_mode:
                oldest_key = next(iter(self.__events))
                self.__events.pop(oldest_key)
            else:
                raise ValueError('Event queue is full, cannot insert new event')

    def handle(self, ID: str) -> Optional[Dict] or bool:
        """
        Takes a string ID and returns the dictionary of content associated with that ID.
        :param ID:
        :return:
        """
        body = self.__events.pop(ID, None)
        if body is None:
            return False
        body = {"ID": ID, "content": body}
        
        return body

    def peek(self, ID: str) -> Optional[Dict] or bool:
        """
        returns a peak of the dictionary of content associated with that ID without removing it.
        :param ID:
        :return:
        """
        body = self.__events.get(ID, None)
        if body is None:
            return False
        body = {"ID": ID, "content": body}

        return body

    def clear(self) -> None:
        """
        Removes all the events from the queue.
        :return:
        """
        self.__events.clear()

    def dump(self) -> Optional[Dict[str, Dict]]:
        """
        Returns a dictionary of all events in the queue.
        :return:
        """
        package = self.__events.copy()
        if not package:
            return None
        self.clear()
        return package

queue = EventQueue(3, safe_mode=True)
queue.insert('event1', {'hello': 'game_start', 'player': 'Alice'})
queue.insert('event2', {'hello': 'game_over', 'player': 'Bob'})
queue.insert('event3', {'hello': 'game_pause', 'player': 'Charlie'})
queue.insert('event4', {'hello': 'game_resume', 'player': 'David'})
print(queue.dump())


