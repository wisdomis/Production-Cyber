
class Product:
    def __init__(self, product_id, arrival_time, processing_time=0):
        self.product_id = product_id
        self.arrival_time = arrival_time
        self.processing_time = processing_time
        self.due_date = 0  # Due date calculated later
