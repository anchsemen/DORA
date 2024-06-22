from celery import Celery

from src.api.tasks.utils import rag_run

celery = Celery("communication_tasks", broker="redis://localhost:6379")


@celery.task
def run_model(input_data, history):
    try:
        answer = rag_run(input_data, history)
        data_to_update = {"is_success": True,
                          "output_data": answer}

    except Exception as e:
        print(e)

        data_to_update = {"is_success": False,
                          "error_info": str(e)}
    return data_to_update
