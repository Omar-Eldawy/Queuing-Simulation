import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from Simulation import Simulation


def main():
    simulation_factory(True)
    simulation_factory(False)


def simulation_factory(part_A: bool):
    table = []
    arrival_rate = (1, 5)
    service_1_rate = (2, 4)
    service_2_rate = (3, 4)
    N = 200
    T = (10, 50, 100, 1000)
    part_B_time = 2000
    q0 = 1000

    for l in arrival_rate:
        for u1 in service_1_rate:
            for u2 in service_2_rate:
                if part_A:
                    for t in T:
                        total_time = 0.0
                        for i in range(N):
                            simulation = Simulation()
                            simulation.simulate(l, u1, u2, t, 0)
                            time_data = np.array(simulation.get_time_data())
                            queue_1_data = np.array(simulation.get_queue_1_data())
                            queue_2_data = np.array(simulation.get_queue_2_data())
                            integral_1 = np.trapz(y=queue_1_data, x=time_data)
                            integral_2 = np.trapz(y=queue_2_data, x=time_data)
                            total_time += ((1 / t) * (integral_1 + integral_2))

                        print(f"For l={l}, u1={u1}, u2={u2}, T={t}, the time average number of customers in the system "
                              f"E[T]={(total_time / N):.3f}")
                        table.append([0, l, u1, u2, t, total_time / N])

                    print("-----------------------------------------------------------------------------------------"
                          "------")
                else:
                    simulation = Simulation()
                    simulation.simulate(l, u1, u2, part_B_time, q0)
                    time_data = np.array(simulation.get_time_data())
                    queue_1_data = np.array(simulation.get_queue_1_data())
                    queue_2_data = np.array(simulation.get_queue_2_data())
                    plt.plot(time_data, queue_1_data, label="Queue 1")
                    plt.plot(time_data, queue_2_data, label="Queue 2")
                    plt.xlabel("Time unit")
                    plt.ylabel("Number of customers")
                    plt.title(f"Number of customers in the system l={l}, u1={u1}, u2={u2}")
                    plt.legend()
                    plt.xlim(0, part_B_time)
                    plt.show()
                    table.append([1000, l, u1, u2, part_B_time, queue_1_data[-1], queue_2_data[-1]])

    if part_A:
        df = pd.DataFrame(table, columns=["q", "l", "u1", "u2", "T", "E[T]"])
        df.to_csv("part_a.csv", index=False)
    else:
        df = pd.DataFrame(table, columns=["q", "l", "u1", "u2", "T", "Queue 1 final size", "Queue 2 final size"])
        df.to_csv("part_b.csv", index=False)


if __name__ == "__main__":
    main()
