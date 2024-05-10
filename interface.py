import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np

import server as s

class SimulationResults:

    def __init__(self):
        self.simulation_series_results = []
        self.num_of_experiments = None

        self.sigma_a = None
        self.sigma_b = None
        self.lambda_value = None

        self.num_of_tasks = None
        self.num_of_experiments = None
        self.max_length = None

    def get_input(self):
        self.sigma_a = float(sigma_a_entry.get())
        self.sigma_b = float(sigma_b_entry.get())
        self.lambda_value = float(lambda_value_entry.get())

        self.num_of_tasks = int(num_of_tasks_entry.get())
        self.num_of_experiments = int(num_of_experiments_entry.get())
        self.max_length = int(max_length_entry.get())

    def start_simulation(self):
        try:
            self.get_input()
            server = s.Server(self.sigma_a, self.sigma_b, self.lambda_value, self.max_length, self.num_of_tasks, result_tree, result_label)
            server.simulate_server()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for Total Time.")

    def conduct_series(self):
        self.get_input()
        wait_window = tk.Toplevel(root)
        wait_window.title("Please Wait")
        wait_label = ttk.Label(wait_window, text="Simulating... Please wait.")
        wait_label.pack()
        root.update()

        # Now to update the Label text, simply `.set()` the `StringVar`

        self.simulation_series_results = []
        for _ in range(self.num_of_experiments):
            server = s.Server(self.sigma_a, self.sigma_b, self.lambda_value, self.max_length, self.num_of_tasks, result_tree, result_label)
            self.simulation_series_results.append(server.simulate_server())

        wait_window.destroy()

    def build_queue_plot(self):
        self.get_input()
        queue_lengths = [len(result[0].tasks) for result in self.simulation_series_results]

        # Нормализация данных для получения вероятностей
        unique_lengths, counts = np.unique(queue_lengths, return_counts=True)
        probabilities = counts / self.num_of_experiments

        # Построение графика
        plt.figure(figsize=(8, 6))
        plt.bar(unique_lengths, probabilities, color='skyblue')
        plt.title('Probability Distribution of Queue Lengths')
        plt.xlabel('Queue Length')
        plt.ylabel('Probability')
        plt.xticks(unique_lengths)
        plt.grid(axis='y')

        plt.text(0.70, 0.05, f'lambda: {self.lambda_value:.2f} \n sigma_a:{self.sigma_a:.2f}  \n sigma_b:{self.sigma_b:.2f}', ha='left', va='bottom', fontsize=12, bbox=dict(facecolor='white', alpha=0.5),
                 transform=plt.gca().transAxes)
        plt.show()

    def build_waiting_time_plot(self):
        self.get_input()
        waiting_times = [round(result[1][10].completed_time - result[1][10].sigma - result[1][10].arrival_time, 2) for
                         result in self.simulation_series_results]

        # Вычисление эмпирической функции распределения (ECDF)
        sorted_waiting_times = np.sort(waiting_times)
        ecdf = np.arange(1, len(sorted_waiting_times) + 1) / len(sorted_waiting_times)
        # Построение графика
        plt.figure(figsize=(8, 6))
        plt.plot(sorted_waiting_times, ecdf, marker='o', linestyle='-', color='b', markersize=3)
        plt.title('Distribution Function of Waiting Times')
        plt.xlabel('Waiting Time')
        plt.ylabel('Probability')

        plt.text(0.70, 0.05, f'lambda: {self.lambda_value:.2f} \n sigma_a:{self.sigma_a:.2f}  \n sigma_b:{self.sigma_b:.2f}', ha='left', va='bottom', fontsize=12, bbox=dict(facecolor='white', alpha=0.5),
                 transform=plt.gca().transAxes)

        plt.grid(True)
        plt.show()

    def plot_busy_cores(self):

        busy_cores_count = [result[2] for result in self.simulation_series_results]

        unique_busy_cores, counts = np.unique(busy_cores_count, return_counts=True)
        probabilities = counts / self.num_of_experiments

        # Построение графика
        plt.figure(figsize=(8, 6))
        plt.bar(unique_busy_cores, probabilities, color='lightgreen')
        plt.title('Probability Distribution of Busy Cores')
        plt.xlabel('Number of Busy Cores')
        plt.ylabel('Probability')
        plt.xticks(unique_busy_cores)
        plt.grid(axis='y')

        plt.text(0.70, 0.05, f'lambda: {self.lambda_value:.2f} \n sigma_a:{self.sigma_a:.2f}  \n sigma_b:{self.sigma_b:.2f}', ha='left', va='bottom', fontsize=12, bbox=dict(facecolor='white', alpha=0.5),
                 transform=plt.gca().transAxes)

        plt.show()


result = SimulationResults()

root = tk.Tk()
root.title("Server Simulation")

# Input Frame
input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


labelPryProt = ttk.Label(input_frame, text='Single Simulation', font='Helvetica 16 bold').grid(row=0, column=0, padx=5, pady=5, sticky="w")

ttk.Label(input_frame, text="lambda_value:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
lambda_value_entry = ttk.Entry(input_frame)
lambda_value_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
lambda_value_entry.insert(0, "1.0")

ttk.Label(input_frame, text="sigma_a:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
sigma_a_entry = ttk.Entry(input_frame)
sigma_a_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
sigma_a_entry.insert(0, "1.0")

ttk.Label(input_frame, text="sigma_b:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
sigma_b_entry = ttk.Entry(input_frame)
sigma_b_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
sigma_b_entry.insert(0, "2.0")

ttk.Label(input_frame, text="queue_max_length:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
max_length_entry = ttk.Entry(input_frame)
max_length_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
max_length_entry.insert(0, "20")

ttk.Label(input_frame, text="Number of Tasks:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
num_of_tasks_entry = ttk.Entry(input_frame)
num_of_tasks_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
num_of_tasks_entry.insert(0, "100")

start_button = ttk.Button(input_frame, text="Start Simulation", command=result.start_simulation)
start_button.grid(row=6, column=0, columnspan=2, pady=10)


labelPryProt2 = ttk.Label(input_frame, text='Multiple Simulations', font='Helvetica 16 bold').grid(row=0, column=3, padx=5, pady=5, sticky="w")

ttk.Label(input_frame, text="Number of experiments:").grid(row=1, column=3, padx=5, pady=5, sticky="w")
num_of_experiments_entry = ttk.Entry(input_frame)
num_of_experiments_entry.grid(row=1, column=4, padx=5, pady=5, sticky="w")
num_of_experiments_entry.insert(0, "1000")
start_button = ttk.Button(input_frame, text="Conduct Series", command=result.conduct_series)
start_button.grid(row=1, column=5, columnspan=2, pady=10)


ttk.Label(input_frame, text="Build Plots:").grid(row=2, column=3, padx=5, pady=5, sticky="w")

start_button = ttk.Button(input_frame, text="Plot Queue ", command=result.build_queue_plot)
start_button.grid(row=2, column=3, columnspan=2, pady=10)

start_button = ttk.Button(input_frame, text="Plot Wait Time ", command=result.build_waiting_time_plot)
start_button.grid(row=2, column=4, columnspan=2, pady=10)

start_button = ttk.Button(input_frame, text="Plot Busy Cores", command=result.plot_busy_cores)
start_button.grid(row=2, column=5, columnspan=2, pady=10)

# Result Frame
result_frame = ttk.Frame(root)
result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

result_label = ttk.Label(result_frame, text="Simulation Results:")
result_label.pack()

result_tree = ttk.Treeview(result_frame, columns=('TS', 'Core 1 CurrTask', 'Core 2 CurrTask', 'Queue'), show='headings')

result_tree.heading('TS', text='TS')

result_tree.heading('Core 1 CurrTask', text='Core1')

result_tree.heading('Core 2 CurrTask', text='Core 2')

result_tree.heading('Queue', text='Queue')

result_tree.pack(expand=True, fill='both')

root.mainloop()


