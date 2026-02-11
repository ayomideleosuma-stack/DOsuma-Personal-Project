"""
banking.py
Author: Dele Osuma

simulates a banking system using a dynamic circular queue for customer 
management and a round-robin scheduling system for fair service distribution.
"""

from queue import Queue
import job_generator


class Teller:
    """
    Represents a bank teller who serves customers.
    """

    def __init__(self, name):
        """
        Initializes a teller with a name and service tracking.
        Parameters:
            name (str): The name of the teller.
        """
        self._name = name
        self._total_service_time = 0
        self._current_customer = None

    def get_name(self):
        """Returns the teller's name."""
        return self._name

    def is_available(self):
        """Returns True if the teller is available to serve a customer."""
        return self._current_customer is None

    def accept_customer(self, service_time):
        """
        Accepts a new customer if the teller is available.
        Parameters:
            service_time (int): The requested service time for the customer.
        """
        if self.is_available():
            self._current_customer = service_time

    def service_customer(self, service_time):
        """
        Serves the current customer for the given service time.
        Parameters:
            service_time (int): The amount of time to serve the customer.
        """
        if self._current_customer is not None:
            served_time = min(self._current_customer, service_time)
            self._total_service_time += served_time
            self._current_customer -= served_time
            if self._current_customer == 0:
                self._current_customer = None  # Customer finished

    def release_customer(self):
        """Marks the teller as available for the next customer."""
        self._current_customer = None

    def get_total_service_time(self):
        """Returns the total service time of the teller."""
        return self._total_service_time

    def __str__(self):
        """Returns a formatted string representation of the teller."""
        return f"Teller: {self._name} Total service time: {self._total_service_time}"


class BankingSimulation:
    """
    A banking system simulation that manages tellers and customer service using a round-robin queue.
    """

    def __init__(self):
        """Initializes the banking simulation with a queue and teller list."""
        self.tellers = []
        self.customer_queue = Queue()
        self.total_simulation_time = 0

    def create_tellers(self, num_tellers):
        """Creates the specified number of tellers."""
        self.tellers = [Teller(str(i)) for i in range(num_tellers)]

    def add_customers(self, service_times):
        """Adds customers with the given service times to the queue."""
        for time in service_times:
            self.customer_queue.enqueue(time)

    def process_service_cycle(self, service_time):
        """
        Performs one service cycle, assigning customers to available tellers.

        Parameters:
            service_time (int): The time duration of the service cycle.
        """
        self.total_simulation_time += service_time

        # Assign available tellers to customers
        for teller in self.tellers:
            if teller.is_available() and not self.customer_queue.is_empty():
                teller.accept_customer(self.customer_queue.dequeue())

        # Serve customers for the given service time
        for teller in self.tellers:
            teller.service_customer(service_time)

        # Requeue customers who are not fully served
        for teller in self.tellers:
            if teller._current_customer is not None:
                self.customer_queue.enqueue(teller._current_customer)
                teller.release_customer()

    def print_status(self):
        """Prints the status of the tellers and the queue."""
        print("\n--- STATUS REPORT ---")
        for teller in self.tellers:
            idle_percentage = (
                (self.total_simulation_time - teller.get_total_service_time()) / self.total_simulation_time * 100
                if self.total_simulation_time > 0 else 0
            )
            print(f"{teller} Percentage idle: {idle_percentage:.2f}%")
        print(f"Customers in queue: {len(self.customer_queue)} {self.customer_queue}")

    def run_simulation(self):
        """Runs the banking simulation using job_generator."""
        job_gen = job_generator.generate_jobs()

        for job, value in job_gen:
            if job == "call":
                self.create_tellers(value)

            elif job == "add":
                service_times = list(map(int, value.split()))
                self.add_customers(service_times)

            elif job == "service":
                self.process_service_cycle(value)

            elif job == "status":
                self.print_status()

            elif job == "quit":
                print("\n--- FINAL REPORT ---")
                self.print_status()
                print(f"Customers left in queue: {len(self.customer_queue)}")
                break

