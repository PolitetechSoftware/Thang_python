from celery_conf import app
from metrics_decorator import metrics_collector  # Import metrics_data
import time, random

@metrics_collector
def example_function():
    # Simulate processing time and occasional errors
    time.sleep(0.1)
    if random.random() < 0.3:  # 30% chance to raise an error
        raise ValueError("Something went wrong!")

@metrics_collector
def test_function():
    # Simulate processing time and occasional errors
    time.sleep(0.1)
    if random.random() < 0.3:  # 30% chance to raise an error
        raise ValueError("Something went wrong!")
    
@metrics_collector
def access_metrics():
    # Simulate processing time and occasional errors
    time.sleep(0.1)
    if random.random() < 0.3:  # 30% chance to raise an error
        raise ValueError("Something went wrong!")

# Simulate calling the function multiple times
@app.task
def simulate_func_call():
    try:
        example_function()
        test_function()
        access_metrics()
    except ValueError:
        print ("Error in simulate_func_call function")
        pass  # Ignore errors for demonstration