### Build and Deploy
```bash
   docker-compose build
   docker-compose up -d
   ```
### Task: Developing a Decorator for Metrics Collection
Running the Task:
    ```
    docker exec -it <politetech_celery_worker_1> python decorator_impl.py 
    ```
### Task: Additional Challenge, Saving metrics to a database for further analysis
To see data updates in postgresql, use the following command:
   ```bash
   docker exec -it <postgresql_container_name> bash
   psql -U postgres -d postgres
   \dt
   postgres=# select * from function_metrics ;
 id |  function_name   | num_calls | avg_execution_time  | num_errors |         created_at
----+------------------+-----------+---------------------+------------+----------------------------
  3 | access_metrics   |         4 | 0.10034465789794922 |          3 | 2024-09-19 15:48:36.940054
  2 | test_function    |         6 | 0.10023196538289388 |          5 | 2024-09-19 15:48:36.817878
  1 | example_function |         9 | 0.10027233759562175 |          8 | 2024-09-19 15:48:36.740664
   ```
