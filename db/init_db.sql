CREATE TABLE function_metrics (
    id SERIAL PRIMARY KEY,
    function_name VARCHAR(255) UNIQUE NOT NULL,
    num_calls INTEGER NOT NULL,
    avg_execution_time FLOAT NOT NULL,
    num_errors INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
