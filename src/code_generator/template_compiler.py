import logging

def handle_task(task, output_dir):
    
    try:
    
        match task['type']:
            case 'producer_nats':
                __generate_producer(task, output_dir)
            case 'processor_nats':
                __generate_processor(task, output_dir)
            case 'dbsync_nats':
                __generate_dbsync(task, output_dir)
            case _:
                logging.error(f"Task type {task['type']} not supported")
                pass
    except KeyError as e:
        logging.error(f"Error parsing task: {e}")
        pass
    
def __generate_producer(task, output_dir):
    pass

def __generate_processor(task, output_dir):
    pass

def __generate_dbsync(task, output_dir):
    pass