import time
import functools
from save_metrics_tasks import save_metrics_queue

metrics_data = {} # task 1 purpose

def metrics_collector(func):
    func_name = func.__name__
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        metrics_data_temp = {}
        if func_name not in metrics_data:
            metrics_data[func_name] = {
                'num_calls': 0,
                'num_errors': 0,
                'total_time': 0.0
            }
        metrics_data_temp[func_name] = {
            'num_calls': 0,
            'num_errors': 0,
            'total_time': 0.0
        }
            
        metrics_data[func_name]['num_calls'] +=1
        metrics_data_temp[func_name]['num_calls'] +=1

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            metrics_data[func_name]["num_errors"] +=1
            metrics_data_temp[func_name]['num_errors'] +=1
            raise e
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            metrics_data[func_name]["total_time"] += elapsed_time
            metrics_data_temp[func_name]['total_time'] = elapsed_time
            save_metrics_queue.delay(metrics_data_temp)
        return result
    
    return wrapper

def get_metrics(func_name):
    """Retrieve and display metrics for the given function."""
    if func_name not in metrics_data:
        return f"No metrics found for function: {func_name}"
    
    data = metrics_data[func_name]
    num_calls = data['num_calls']
    avg_time = data['total_time'] / num_calls if num_calls > 0 else 0.0
    return {
        'Function': func_name,
        'Number of calls': num_calls,
        'Average execution time': avg_time,
        'Number of errors': data['num_errors']
    }
