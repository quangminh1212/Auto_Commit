import time

class Scheduler:
    def __init__(self, interval_minutes):
        """
        Initialize the scheduler
        interval_minutes: Time between commits in minutes
        """
        self.interval_seconds = interval_minutes * 60
        self.last_run = 0
    
    def should_run(self):
        """Check if it's time to run a commit"""
        current_time = time.time()
        return (current_time - self.last_run) >= self.interval_seconds
    
    def update_last_run(self):
        """Update the last run timestamp"""
        self.last_run = time.time()
