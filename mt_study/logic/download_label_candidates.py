import pickle
import timeit
from functools import partial

from delab.corpus.download_conversations_proxy import download_daily_sample

from delab.delab_enums import PLATFORM
from delab.models import Tweet
from delab_trees import TreeManager
from delab_trees.delab_tree import DelabTree

M_TURK_TOPIC = "mturk_candidate"


def download_mturk_sample_conversations(n_runs, platform, min_results):
    # Perform 100 runs of the function and measure the time taken

    download_mturk_sample_helper = partial(download_mturk_samples, platform, min_results, True)
    execution_time = timeit.timeit(download_mturk_sample_helper, number=n_runs)
    average_time = (execution_time / 100) / 60
    print("Execution time:", execution_time, "seconds")
    print("Aberage Execution time:", average_time, "minutes")


def download_mturk_samples(platform=PLATFORM.TWITTER, min_results=20, persist=True) -> list[DelabTree]:
    result = []
    print("downloading random conversations for mturk_labeling")
    while len(result) < min_results:
        # try:
        downloaded_trees = download_daily_sample(topic_string=M_TURK_TOPIC, platform=platform, persist=True)
        for tree in downloaded_trees:
            tree.validate(verbose=False)
        result += downloaded_trees
        print("downloaded candidates:", len(result))
        """
        except Exception as ex:
            print(ex)
            exception_counter += 1
            if exception_counter > 100:
                break
        """

    forest = TreeManager.from_trees(result)
    # print(f"finished downloading trees {forest}")

    flow_sample = forest.get_flow_sample(5, filter_function=is_short_text)
    print(flow_sample)

    # collect ids of the trees from the sample
    sample_tree_ids = []
    for sample in flow_sample:
        first_post = sample[0]
        tree_id = first_post.tree_id
        sample_tree_ids.append(tree_id)
    # throw out the trees not sampled
    forest.keep(sample_tree_ids)

    if persist:
        objects = Tweet.objects.filter(conversation_id__in=sample_tree_ids).values_list("conversation_id", flat=True)
        n_stored_objects = len(set(list(objects)))
        n_sample_tree_ids = len(set(sample_tree_ids))
        assert n_stored_objects == n_sample_tree_ids
    # TODO persist flow_sample


def is_short_text(text):
    """
    Check if the given text is shorter than 280 characters.

    Args:
        text (str): The text to be checked.

    Returns:
        bool: True if the text is shorter than 280 characters, False otherwise.
    """
    return len(text) < 280
