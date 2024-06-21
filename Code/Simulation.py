import numpy as np
import sys


class Simulation:
    def __init__(self):
        self.__time = []
        self.__queue_1 = []
        self.__queue_2 = []

    def get_time_data(self):
        return self.__time

    def get_queue_1_data(self):
        return self.__queue_1

    def get_queue_2_data(self):
        return self.__queue_2

    def __generate_arrival_time(self, rate: float, interval: int) -> list[float]:
        time = []
        current_time = 0.0
        while current_time < interval:
            current_time += np.random.exponential(1.0 / rate)
            time.append(current_time)
        return time

    def __generate_service_time(self, rate: float, size: int) -> list[float]:
        time = []
        for _ in range(size):
            time.append(np.random.exponential(1.0 / rate))
        return time

    def simulate(self, arrival_rate: float, service_1_rate: float, service_2_rate: float, interval: int,
                 initial_capacity: int):
        current_time = 0.0
        index = 0
        arrival_time = [0.0 for _ in range(initial_capacity)]
        arrival_time = arrival_time + self.__generate_arrival_time(arrival_rate, interval)
        service_time_1 = self.__generate_service_time(service_1_rate, len(arrival_time))
        service_time_2 = self.__generate_service_time(service_2_rate, len(arrival_time))
        queue_1 = []
        queue_2 = []
        queue_1_service_end = sys.maxsize
        queue_2_service_end = sys.maxsize
        while current_time <= interval:
            current_time = min(arrival_time[index], queue_1_service_end, queue_2_service_end)
            # new arrival
            if current_time == arrival_time[index]:
                queue_1.append(index)
                if len(queue_1) == 1:
                    queue_1_service_end = current_time + service_time_1[index]
                index += 1

            # queue 1 service end
            elif current_time == queue_1_service_end:
                finished_index = queue_1.pop(0)
                queue_2.append(index)
                if len(queue_2) == 1:
                    queue_2_service_end = current_time + service_time_2[finished_index]
                if len(queue_1) > 0:
                    queue_1_service_end = current_time + service_time_1[queue_1[0]]
                else:
                    queue_1_service_end = sys.maxsize

            # queue 2 service end
            else:
                queue_2.pop(0)
                if len(queue_2) > 0:
                    queue_2_service_end = current_time + service_time_2[queue_2[0]]
                else:
                    queue_2_service_end = sys.maxsize

            # store current state
            self.__time.append(current_time)
            self.__queue_1.append(len(queue_1))
            self.__queue_2.append(len(queue_2))
