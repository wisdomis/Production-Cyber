import random
from collections import defaultdict
import matplotlib.pyplot as plt

# Machine Status
IDLE = 'IDLE'
RUN = 'RUN'
SETUP = 'SETUP'
DOWN = 'DOWN'

def generate_expo_time(expo_lambda):
    return random.expovariate(1/expo_lambda)


def generate_normal_time(mu, sigma):
    return random.normalvariate(mu, sigma)


def generate_uniform_time(lower, upper):
    return random.uniform(lower, upper)


class StatisticalAccumulator:
    def __init__(self):
        # Product (Entity) 관련된 accumulator
        self.num_of_output = defaultdict(int)
        self.total_waiting_time = defaultdict(int)
        self.max_waiting_time = defaultdict(int)
        self.total_flow_time = defaultdict(int)
        self.max_flow_time = defaultdict(int)
        self.total_wip_for_time = 0
        self.total_queue_for_time = 0

        # Machine (Resource) 관련된 accumulator
        self.total_processing_time = defaultdict(int)
        self.total_idle_time = defaultdict(int)

        # Final KPI
        self.makespan = 0
        self.machine_utilization = {}
        self.avg_waiting_time = {}
        self.total_machine_util = 0
        self.avg_wip = 0
        self.avg_queue = 0
        self.total_avg_waiting_time = 0

    def report(self, simulation_clock):
        self.makespan = simulation_clock
        self.machine_utilization = {m: self.total_processing_time[m] / simulation_clock for m in self.total_processing_time.keys()}
        self.avg_wip = self.total_wip_for_time / simulation_clock
        self.avg_queue = self.total_queue_for_time / simulation_clock

        print("\n--- Simulation Report ---")
        print(f'Total simulation time: {simulation_clock:.2f}')
        self.total_machine_util = 0
        for machine_id, util in self.machine_utilization.items():
            print(f'Machine {machine_id} utilization: {util:.2%}')
            self.total_machine_util += util
        self.total_machine_util = self.total_machine_util/len(self.machine_utilization)
        print(f'Average machine utilization: {self.total_machine_util/len(self.machine_utilization):.2%}')
        print(f'Average WIP: {self.avg_wip:.2f}')
        print(f'Average # of Queue: {self.avg_queue:.2f}')


class GanttChart:
    def __init__(self):
        self.gantt_chart_data = defaultdict(list)
        self.colors = self.generate_colors()

    def generate_colors(self):
        base_colors = plt.cm.tab20.colors  # Use tab20 colormap
        product_types = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Up to 26 different products
        return {product_types[i]: base_colors[i % len(base_colors)] for i in range(len(product_types))}

    def plot_gantt_chart(self):
        fig, ax = plt.subplots(figsize=(10, 3*len(self.gantt_chart_data)))
        y_ticks = []
        y_tick_labels = []
        for machine_id in sorted(self.gantt_chart_data.keys(), reverse=True):
            machine_data = self.gantt_chart_data[machine_id]
            y_ticks.append(machine_id)
            y_tick_labels.append('Machine ' + machine_id[-1])
            for start, end, product_id in machine_data:
                color = self.colors[product_id]
                ax.barh(machine_id, end - start, left=start, color=color, edgecolor='black', label=f'Product {product_id}')

        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_tick_labels)
        ax.set_xlabel('Time')
        ax.set_title('Gantt Chart of Machine Processing')
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))

        sorted_labels_handles = sorted(by_label.items())  # Sort by labels
        sorted_labels, sorted_handles = zip(*sorted_labels_handles)
        plt.legend(sorted_handles, sorted_labels, loc='upper right')
        plt.tight_layout()  # Adjust the layout to make sure everything fits
        plt.show()