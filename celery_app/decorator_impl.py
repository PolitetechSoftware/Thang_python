from metrics_decorator import metrics_collector, get_metrics
import time, random


@metrics_collector
def example_function():
    # Simulate processing time and occasional errors
    time.sleep(0.1)
    if random.random() < 0.3:  # 30% chance to raise an error
        raise ValueError("Something went wrong!")

# Simulate calling the function multiple times
for _ in range(10):
    try:
        example_function()
    except ValueError:
        pass  # Ignore errors for demonstration

# Retrieve and display metrics
metrics = get_metrics('example_function')
print(metrics)
