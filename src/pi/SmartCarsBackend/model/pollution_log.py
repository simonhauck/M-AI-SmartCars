from typing import List


class PollutionLog:

    def __init__(self, time_to_delete: float = 30 * 1000) -> None:
        self.time_to_delete = time_to_delete
        pollution_list: List[PollutionEntry] = []
        self.log = pollution_list

    def __clean_list(self):
        return


class PollutionEntry:

    def __init__(self, pollution: float, timestamp: int) -> None:
        """
        create an entry for the pollution log. The entry stores the pollution value and the timestamp
        :param pollution: caused pollution by a vehicle
        :param timestamp: when the pollution occurred as unix timestamp in ms
        """
        self.pollution = pollution
        self.timestamp = timestamp