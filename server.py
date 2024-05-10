import random


class Queue:
    def __init__(self, max_length):
        self.tasks = []
        self.max_length = max_length

    def get_task(self):
        if self.tasks:
            return self.tasks.pop(random.randint(0, len(self.tasks) - 1))
        else:
            return None

class Core:
    def __init__(self):
        self.current_task = None
        self.is_occupied = False
        self.finish_time = None


class Task:
    def __init__(self, tau, sigma, arrival_time):
        self.tau = tau
        self.sigma = sigma
        self.arrival_time = arrival_time
        self.start_processing = 0
        self.completed_time = 0


class Server:
    def __init__(self, sigma_a,sigma_b, lambda_value, max_length, num_of_tasks, result_tree, result_label):
        self.TS = 0
        self.T1 = 0
        self.T2 = 0
        self.TIP = False
        self.L = 0
        self.rejected_tasks = 0
        self.processed_tasks = []
        self.core1 = Core()
        self.core2 = Core()
        self.queue = Queue(max_length)

        self.task_counter = 0
        self.new_task = None

        self.lambda_value = lambda_value
        self.sigma_a = sigma_a
        self.sigma_b = sigma_b
        self.num_of_tasks = num_of_tasks

        self.result_tree = result_tree
        self.result_label = result_label

        try:
            if self.sigma_a <= 0:
                raise ValueError("Sigma_a должно быть больше 0.")

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))



    def generate_tau(self):
        return random.expovariate(1 / self.lambda_value)

    def generate_sigma(self):
        return random.uniform(self.sigma_a, self.sigma_b)

    def simulation_results(self):
        self.result_tree.insert('', 'end', values=(self.TS,
                                              f' {(round(self.core1.current_task.tau, 2), round(self.core1.current_task.sigma, 2)) if self.core1.current_task else "0"}, FT {round(self.core1.finish_time, 2) if self.core1.finish_time else "0"}',
                                              f' {(round(self.core2.current_task.tau, 2), round(self.core2.current_task.sigma, 2)) if self.core2.current_task else "0"}, FT {round(self.core2.finish_time, 2) if self.core2.finish_time else "0"}',
                                              f' L: {len(self.queue.tasks)}'))

    def occupy_core(self, core, task, time):
        core.current_task = task
        core.finish_time = time + task.sigma
        core.is_occupied = True

    def deoccupy_core(self, core):
        task = core.current_task
        task.completed_time = core.finish_time
        core.is_occupied = False
        core.current_task = None
        core.finish_time = None
        # Move task to processed
        self.processed_tasks.append(task)

    def simulate_server(self):
        self.result_tree.delete(*self.result_tree.get_children())


        tau = self.generate_tau()
        sigma = self.generate_sigma()

        self.T1 = tau
        self.TS = self.T1
        self.T2 = self.T1 + sigma

        task = Task(self.T1, sigma, self.T1)
        self.task_counter += 1

        self.occupy_core(self.core1, task, self.T1)

        while self.task_counter <= self.num_of_tasks:
            self.process_time_step()

        busy_cores = sum(core.is_occupied for core in [self.core1, self.core2])  # Подсчитываем занятые ядра

        return (self.queue, self.processed_tasks, busy_cores)

    def process_task(self):
        core = self.core1 if self.core1.finish_time == self.T2 else (
            self.core2 if self.core2.finish_time == self.T2 else None)
        self.deoccupy_core(core)

        if len(self.queue.tasks) != 0:
            task = self.queue.get_task()
            self.occupy_core(core, task, self.T2)

    def process_time_step(self):

        if self.TIP:  # End processing
            self.process_task()

        else:  # New Task
            if self.new_task:
                task = self.new_task
                self.new_task = None
            else:
                tau = self.generate_tau()
                sigma = self.generate_sigma()

                self.T1 += tau
                task = Task(tau, sigma, self.T1)
                self.task_counter += 1

            if self.T1 < self.T2:
                core = self.core1 if not self.core1.is_occupied else (
                    self.core2 if not self.core2.is_occupied else None)
                if core:
                    self.occupy_core(core, task,self.T1)
                else:
                    if len(self.queue.tasks) < self.queue.max_length:
                        self.queue.tasks.append(task)
                    else:
                        self.rejected_tasks += 1

            else:
                self.new_task = task

        self.simulation_results()

        if self.core1.finish_time and self.core2.finish_time:
            self.T2 = min(self.core1.finish_time, self.core2.finish_time)
        else:
            if self.core1.finish_time:
                self.T2 = self.core1.finish_time
            elif self.core2.finish_time:
                self.T2 = self.core2.finish_time
            else:
                self.T2 = float("inf")

        self.TIP = self.T1 > self.T2
        self.TS = min(self.T1, self.T2)

        self.result_label.config(
            text=f"Simulation Results: Processed Tasks - {len(self.processed_tasks)}, Rejected Tasks - {self.rejected_tasks}")