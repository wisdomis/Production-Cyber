

class Machine(object):
    def __init__(self, machine_id, feasible_product_id_list=None, status='IDLE'):
        self.machine_id = machine_id
        self.feasible_product_id_list = feasible_product_id_list
        self.status = status
        self.product_processed = None
        self.cumulative_idle_time = None
        self.last_work_finish_time = 0
        self.event_start_time = 0




