from celery_conf import app
from sqlalchemy import create_engine, MetaData, Table, select, update
from sqlalchemy.orm import sessionmaker
import os

# Database vars
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')
# Database configuration
DATABASE_URL = 'postgresql://{user}:{password}@db/{db_name}'.format(user=db_user, password=db_password, db_name=db_name)

# Create the database engine
engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)
@app.task
def save_metrics_queue(data):
    """Celery task to save metrics to PostgreSQL."""
    function_metrics = Table(
        'function_metrics', metadata,
        autoload_with=engine
    )
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        for func_name, metrics in data.items():
            avg_time = metrics['total_time'] / metrics['num_calls'] if metrics['num_calls'] > 0 else 0.0
            # Use INSERT ... ON CONFLICT to handle upsert
            stmt = select(function_metrics).where(function_metrics.c.function_name == func_name)
            result = session.execute(stmt).fetchone()
            
            if result:
                # Record exists, perform an UPDATE
                existing_num_calls = result['num_calls']
                existing_avg_time = result['avg_execution_time']
                existing_num_errors = result['num_errors']

                # Calculate new metrics
                new_num_calls = existing_num_calls + metrics['num_calls']
                new_num_errors = existing_num_errors + metrics['num_calls']
                total_time = existing_avg_time * existing_num_calls + metrics['total_time']
                new_avg_execution_time = total_time / new_num_calls if new_num_calls > 0 else 0.0
                update_stmt = (
                    update(function_metrics)
                    .where(function_metrics.c.function_name == func_name)
                    .values(
                        num_calls=new_num_calls,
                        avg_execution_time=new_avg_execution_time,
                        num_errors=new_num_errors
                    )
                )
                session.execute(update_stmt)
                print(f"Updated metrics for function: {func_name}")
            else:
                # Record doesn't exist, perform an INSERT
                insert_stmt = function_metrics.insert().values(
                    function_name=func_name,
                    num_calls=metrics['num_calls'],
                    avg_execution_time=avg_time,
                    num_errors=metrics['num_errors']
                )
                session.execute(insert_stmt)
                print(f"Inserted metrics for function: {func_name}")
        
        # Commit the transaction
        session.commit()