import time
from typing import List


class PollutionEntry:

    def __init__(self, pollution: float, timestamp: float) -> None:
        """
        create an entry for the pollution log. The entry stores the pollution value and the timestamp
        :param pollution: caused pollution by a vehicle
        :param timestamp: when the pollution occurred as unix timestamp in ms
        """
        self.pollution = pollution
        self.timestamp = timestamp


class PollutionLog:

    def __init__(self, time_to_delete: float = 30) -> None:
        self.time_to_delete = time_to_delete
        pollution_list: List[PollutionEntry] = []
        self.log = pollution_list
        self.total_amount = 0


    def clean_list(self) -> None:
        """
        Clean the list from entry's that are to old
        :return: None
        """
        current_timestamp = time.time()
        filtered_list: List[PollutionEntry] = [entry for entry in self.log if
                                               entry.timestamp + self.time_to_delete >= current_timestamp]
        self.log = filtered_list

    def add_entry(self, pollution_entry: PollutionEntry) -> None:
        """
        Add an entry to the pollution log
        :param pollution_entry: the entry that will be added
        :return: None
        """
        self.log.append(pollution_entry)
        self.total_amount += 1

    def get_size(self) -> int:
        """
        :return: the length of the log
        """
        return len(self.log)

    def sum_pollution(self) -> float:
        """
        Calculate the sum of the pollution
        :return: the sum of all entry's
        """
        return sum(entry.pollution for entry in self.log)

    def get_total_amount(self) -> int:
        """
        :return: the total amount of entries written in the log
        """
        return self.total_amount
