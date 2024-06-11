import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches

def simulate_tandem_queue(lam, mu1, mu2, T, q, N):
    avg_customers = []
    for _ in range(N):
        t = 0
        L1 = q
        L2 = 0
        total_customers = 0
        events = []
        
        while t < T:
            if L1 > 0:
                t1 = np.random.exponential(1 / mu1)
            else:
                t1 = np.inf
            
            if L2 > 0:
                t2 = np.random.exponential(1 / mu2)
            else:
                t2 = np.inf
            
            ta = np.random.exponential(1 / lam)
            
            next_event = min(ta, t1, t2)
            t += next_event
            
            if next_event == ta:
                events.append(('arrival', t))
                L1 += 1
            elif next_event == t1:
                events.append(('service1', t))
                L1 -= 1
                L2 += 1
            else:
                events.append(('service2', t))
                L2 -= 1
            
            total_customers += (L1 + L2) * next_event
        
        avg_customers.append(total_customers / T)
    
    return np.mean(avg_customers)

def main():
    lam_values = [1, 5]
    mu1_values = [2, 4]
    mu2_values = [3, 4]
    T_values = [10, 50, 100, 1000]
    N = 100
    q_values = [0, 1000]
    results = []
    
    for q in q_values:
        for lam in lam_values:
            for mu1 in mu1_values:
                for mu2 in mu2_values:
                    for T in T_values:
                        avg_customers = simulate_tandem_queue(lam, mu1, mu2, T, q, N)
                        results.append((q, lam, mu1, mu2, T, round(avg_customers, 2)))
                        print(f"q={q}, λ={lam}, μ1={mu1}, μ2={mu2}, T={T}, Avg Customers={avg_customers:.2f}")
    
    document = Document()
    add_results_table(document, results)
    document.save('Tabulated Simulated Results.docx')

    # Generating all the plots
    # plot_simulation(1, 2, 3, 2000, 1000)
    # plot_simulation(1, 2, 4, 2000, 1000)
    # plot_simulation(1, 4, 3, 2000, 1000)
    # plot_simulation(1, 4, 4, 2000, 1000)
    # plot_simulation(5, 2, 3, 2000, 1000)
    # plot_simulation(5, 2, 4, 2000, 1000)
    # plot_simulation(5, 4, 3, 2000, 1000)
    # plot_simulation(5, 4, 4, 2000, 1000)

def plot_simulation(lam, mu1, mu2, T, q):
    t = 0
    L1 = q
    L2 = 0
    times = [0]
    L1_history = [L1]
    L2_history = [L2]
    
    while t < T:
        if L1 > 0:
            t1 = np.random.exponential(1 / mu1)
        else:
            t1 = np.inf
        
        if L2 > 0:
            t2 = np.random.exponential(1 / mu2)
        else:
            t2 = np.inf
        
        ta = np.random.exponential(1 / lam)
        
        next_event = min(ta, t1, t2)
        t += next_event
        
        if next_event == ta:
            L1 += 1
        elif next_event == t1:
            L1 -= 1
            L2 += 1
        else:
            L2 -= 1
        
        times.append(t)
        L1_history.append(L1)
        L2_history.append(L2)
    
    plt.figure(figsize=(12, 6))
    plt.step(times, L1_history, label="L1")
    plt.step(times, L2_history, label="L2")
    plt.xlabel("Time")
    plt.ylabel("Queue Length")
    plt.title(f"Queue Lengths Over Time (λ={lam}, μ1={mu1}, μ2={mu2}, q={q})")
    plt.legend()
    plt.show()


def add_results_table(document, results):
    table = document.add_table(rows=1, cols=len(results[0]))
    table.style = 'Table Grid'

    hdr_cells = table.rows[0].cells
    headers = ["q", "λ", "μ1", "μ2", "T", "Average Customers (Simulation)"]
    for i, header in enumerate(headers):
        hdr_cells[i].text = header

    for row in results:
        row_cells = table.add_row().cells
        for i, cell in enumerate(row):
            if i == 5:
                row_cells[i].text = f"{cell:.2f}"
            else:
                row_cells[i].text = str(cell)


main()
