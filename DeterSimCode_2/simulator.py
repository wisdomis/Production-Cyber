import random
import heapq
from entity import Product
from resource import Machine
from parameters import arrival_rates, processing_params


class Event:
    def __init__(self, product_id, time, action):
        self.product_id = product_id
        self.time = time
        self.action = action

    def __lt__(self, other):
        return self.time < other.time


class Simulation:
    def __init__(self, machines):
        self.clock = 0
        self.event_queue = []
        self.product_queue = []
        self.machines = {m: Machine(m) for m in machines}
        self.completed_products = []
        self.total_tardiness = 0
        self.makespan = 0

    def schedule_event(self, product_id, delay, action):
        event_time = self.clock + delay
        heapq.heappush(self.event_queue, Event(product_id, event_time, action))

    def run(self, sim_duration, arrival_rates, processing_params):
        for product_id, arrival_rate in arrival_rates.items():
            self.schedule_event(product_id, random.expovariate(1/arrival_rate),
                                lambda: self.arrival(product_id, arrival_rate, processing_params[product_id]))
        while self.event_queue and self.clock < sim_duration:
            current_event = heapq.heappop(self.event_queue)
            self.clock = current_event.time
            current_event.action()
        self.report_statistics()

    def arrival(self, product_id, arrival_rate, processing_params):
        arrival_time = random.expovariate(1/arrival_rate)
        processing_time = max(0, random.normalvariate(*processing_params))
        product = Product(product_id, self.clock, processing_time)
        product.due_date = self.clock + 1.6 * processing_time + random.uniform(5, 10)
        self.product_queue.append(product)
        self.schedule_event(product_id, arrival_time, lambda: self.arrival(product_id, arrival_rate, processing_params))
        self.process_queue()

    def process_queue(self):
        for machine_id, machine in self.machines.items():
            if machine.status == "IDLE" and self.product_queue:
                product = self.get_next_product()
                if product:
                    self.start_processing(machine, product)

    def get_next_product(self):
        # FIFO: Return the first product in the queue
        if self.product_queue:
            return self.product_queue.pop(0)
        return None

    def start_processing(self, machine, product):
        machine.status = "RUN"
        machine.product_processed = product
        self.schedule_event(product.product_id, product.processing_time,
                            lambda: self.finish_processing(machine, product))

    def finish_processing(self, machine, product):
        machine.status = "IDLE"
        machine.product_processed = None
        completion_time = self.clock
        tardiness = max(0, completion_time - product.due_date)
        self.total_tardiness += tardiness
        self.makespan = max(self.makespan, completion_time)
        self.completed_products.append((product.product_id, completion_time, tardiness))
        self.process_queue()

    def report_statistics(self):
        print("\n--- Simulation Results ---")
        print(f"Total Tardiness: {self.total_tardiness}")
        print(f"Makespan: {self.makespan}")
        print("Completed Products:")
        for product_id, completion_time, tardiness in self.completed_products:
            print(f"Product {product_id}: Completion Time = {completion_time}, Tardiness = {tardiness}")
