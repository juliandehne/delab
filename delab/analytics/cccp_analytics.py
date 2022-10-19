import pandas as pd

from delab.models import Tweet

MEASURES = ["repetition_prob", "baseline_vision", "centrality"]


def compute_all_cccp_authors():
    df = prepare_metric_records()
    candidate_lists = []
    measure_authors_dictionary = {}
    author2measure = {}
    for measure in MEASURES:
        candidate_list = compute_cccp_candidate_authors(df, measure=measure)
        for conversation_id, author_id in candidate_list:
            if measure in measure_authors_dictionary:
                current_author_list = measure_authors_dictionary[measure]
                current_author_list.append(author_id)
                measure_authors_dictionary[measure] = current_author_list
            else:
                measure_authors_dictionary[measure] = [author_id]
            author2measure[author_id] = measure
        candidate_lists += candidate_list
    return candidate_lists, measure_authors_dictionary, author2measure


def get_central_author_tweet_queryset(conversation_id, tw_author_id):
    tweets = Tweet.objects.filter(conversation_id=conversation_id).all()
    return tweets, tw_author_id


def prepare_metric_records():
    records = []
    tweets = Tweet.objects.all()
    for tweet in tweets:
        if tweet.tw_author is None:
            continue
        tweet_record = {"tweet_id": tweet.id, "text": tweet.text, "conversation_id": tweet.conversation_id,
                        "author_id": tweet.tw_author.id}
        metrics = tweet.tw_author.conversationauthormetrics_set.filter(
            conversation_id=tweet.conversation_id)
        if not metrics.exists():
            continue
        else:
            author_metrics = metrics.get()
            tweet_record["centrality"] = author_metrics.centrality
            tweet_record["baseline_vision"] = author_metrics.baseline_vision
            tweet_record["n_posts"] = author_metrics.n_posts
            records.append(tweet_record)
    df = pd.DataFrame.from_records(records)
    return df


def compute_cccp_candidate_authors(df, measure="mean"):
    """
    @param df: the dataframe containing the metrics centrality, baseline_vision etc.
    @param measure: the measure to be used for filtering candidates, such as "mean" for all measures, or "centrality"
    @return: a list of pairs (conversation_id, author_id)
    """
    df_central_authors = df.drop(
        ["text"], axis=1)
    df_repetition_probs = df.drop(
        ["text",
         "centrality", "baseline_vision", "n_posts", "author_id"], axis=1)
    # %%
    df_repetition_probs = df_repetition_probs.groupby(["conversation_id"]).count()
    grouped_ca = df_central_authors.groupby(["conversation_id", "author_id"]).mean()
    grouped_ca = grouped_ca.drop("tweet_id", axis=1)
    grouped_ca = grouped_ca.join(df_repetition_probs)
    grouped_ca = grouped_ca.assign(repetition_prob=grouped_ca.n_posts / grouped_ca.tweet_id)
    grouped_ca = grouped_ca.drop("tweet_id", axis=1)
    if measure == "mean":
        grouped_ca = grouped_ca.apply(lambda x: x / x.max())
        grouped_ca['mean'] = grouped_ca.mean(axis=1)
        mean_largest = grouped_ca.nlargest(20, "mean")
    if measure == "repetition_prob" or measure == "baseline_vision" or measure == "centrality":
        mean_largest = grouped_ca.nlargest(20, measure)

    # this is the result list, first element of tuple is conversation, second the author
    result = mean_largest.index.tolist()
    # print(result)
    return result
