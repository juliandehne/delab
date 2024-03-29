import time

from background_task.models import Task

from delab.tasks import download_intolerant_tweets, download_moderating_tweets, download_network_structures, \
    update_toxic_values


def run():
    """
      This sets off the pipeline for downloading intolerant and moderating tweets.
      This triggers the daily cron-job in the django background framework

      :return:
      """
    if Task.objects.filter(task_name='delab.tasks.download_moderating_tweets').exists():
        background_tasks = Task.objects.filter(task_name='delab.tasks.download_moderating_tweets')
        # deleting previous daily cron jobs
        for background_task in background_tasks:
            background_task.delete()

    if Task.objects.filter(task_name='delab.tasks.download_intolerant_tweets').exists():
        background_tasks_2 = Task.objects.filter(task_name='delab.tasks.download_intolerant_tweets')
        for background_task_2 in background_tasks_2:
            background_task_2.delete()

    if Task.objects.filter(task_name='delab.tasks.download_network_structures').exists():
        background_tasks_3 = Task.objects.filter(task_name='delab.tasks.download_network_structures')
        for background_task_3 in background_tasks_3:
            background_task_3.delete()

    if Task.objects.filter(task_name='delab.tasks.update_toxic_values').exists():
        background_tasks_4 = Task.objects.filter(task_name='delab.tasks.update_toxic_values')
        for background_task_4 in background_tasks_4:
            background_task_4.delete()

    time.sleep(2)

    # download_network_structures(repeat=Task.WEEKLY)
    # download_moderating_tweets(repeat=Task.WEEKLY)
    download_intolerant_tweets(repeat=Task.WEEKLY)
    # update_toxic_values()


