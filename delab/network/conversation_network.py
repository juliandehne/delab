import logging
from time import sleep

import django
import networkx as nx
from django.db.models import Exists, OuterRef
from matplotlib import pyplot as plt

from delab.corpus.download_author_information import download_authors
from delab.delab_enums import PLATFORM
from delab.models import Tweet, TweetAuthor, FollowerNetwork
from delab.network.DjangoTripleDAO import DjangoTripleDAO
from delab.tw_connection_util import DelabTwarc
from util.abusing_lists import batch
import matplotlib.pyplot as plt
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

logger = logging.getLogger(__name__)


def download_twitter_follower(levels, n_conversations=-1):
    count = 0
    conversation_ids = set(Tweet.objects.filter(platform=PLATFORM.TWITTER).values_list('conversation_id', flat=True))
    conversation_ids = prevent_multiple_downloads(conversation_ids)
    conversation_ids = restrict_conversations_to_reasonable(conversation_ids)
    if len(conversation_ids) > n_conversations > 0:
        conversation_ids = list(conversation_ids)[:n_conversations]
        for conversation_id in conversation_ids:
            count += 1
            download_conversation_network(conversation_id, conversation_ids, count, levels)
    else:
        if len(conversation_ids) < n_conversations > 0:
            for conversation_id in conversation_ids:
                count += 1
                download_conversation_network(conversation_id, conversation_ids, count, levels)
        else:
            for conversation_id in conversation_ids:
                count += 1
                download_conversation_network(conversation_id, conversation_ids, count, levels)
    logger.info("finished downloading networks")


def get_participants(conversation_id):
    """
    as a side effect this would create a conversation node in neo4j
    :param conversation_id:
    :return:
    """
    dao = DjangoTripleDAO()
    discussion_tweets = Tweet.objects.filter(conversation_id=conversation_id).all()
    nodes = set()
    for discussion_tweet in discussion_tweets:
        # time.sleep(15)
        user = discussion_tweet.author_id
        nodes.add(user)
    dao.add_discussion(nodes, conversation_id)  # this would be need in case of neo4j
    return nodes


def download_followers_recursively(user_ids, n_level=1, following=False):
    twarc = DelabTwarc()
    download_followers(user_ids, twarc, n_level, following)


def persist_user(follower_data):
    try:
        author, created = TweetAuthor.objects.get_or_create(
            twitter_id=follower_data["id"],
            name=follower_data["name"],
            screen_name=follower_data["username"],
            location=follower_data.get("location", "unknown")
        )
    except django.db.utils.IntegrityError as ex:
        # logger.error(ex)
        pass
    except Exception as e:
        logger.error(e)


def download_followers(user_ids, twarc, n_level=1, following=False):
    download_missing_author_data(user_ids)
    dao = DjangoTripleDAO()
    follower_ids = []
    count = 0
    user_batches = batch(list(user_ids), 15)
    for user_batch in user_batches:
        for user in user_batch:
            count += 1
            # try:
            if following:
                followers = twarc.following(user=user, user_fields="id,name,location,username", max_results=100)
            else:
                followers = twarc.followers(user=user, user_fields="id,name,location,username", max_results=10)
            for follower_iter in followers:
                # time.sleep(2)
                if "data" in follower_iter:
                    follower_datas = follower_iter["data"]
                    for follower_data in follower_datas:
                        persist_user(follower_data)
                        follower = follower_data["id"]
                        follower_ids.append(follower)
                        if follower:
                            dao.add_follower(user, follower)
                        else:
                            dao.add_follower(follower, user)
                break  # we don't want users with huge follower numbers to dominate the network anyways
        # one batch finished
        logger.debug(
            "Going to sleep after downloading following for max 15 user, {}/{} user finished".format(count,
                                                                                                     len(user_ids)))
        sleep(15 * 60)

    n_level = n_level - 1
    if n_level > 0:
        download_followers(follower_ids, twarc, n_level=n_level)


def download_missing_author_data(user_ids):
    missing_authors = []
    for user_id in user_ids:
        if not TweetAuthor.objects.filter(twitter_id=user_id).exists():
            missing_authors.append(user_id)
    download_authors(missing_authors)


class FaultyGraphException(Exception):
    pass


def get_nx_conversation_graph(conversation_id):
    replies = Tweet.objects.filter(conversation_id=conversation_id)
    # .only("id", "twitter_id", "tn_parent_id", "created_at")

    G = nx.DiGraph()
    edges = []
    nodes = [reply.twitter_id for reply in replies]
    for row in replies:
        nodes.append(row.twitter_id)
        G.add_node(row.twitter_id, id=row.id, created_at=row.created_at)
        if row.tn_parent_id is not None:
            assert row.tn_parent_id in nodes
            edges.append((row.tn_parent_id, row.twitter_id))
    G.add_edges_from(edges)
    return G


def get_root(conversation_graph: nx.DiGraph):  # tree rooted at 0
    roots = [n for n, d in conversation_graph.in_degree() if d == 0]
    return roots[0]


def get_tweet_subgraph(conversation_graph):
    nodes = (
        node
        for node, data
        in conversation_graph.nodes(data=True)
        if data.get("subset") == "tweets"
    )
    subgraph = conversation_graph.subgraph(nodes)
    return subgraph


def compute_author_graph(conversation_id: int):
    G = get_nx_conversation_graph(conversation_id)
    G2 = compute_author_graph_helper(G, conversation_id)
    return G2


def compute_author_graph_helper(G, conversation_id):
    author_tweet_pairs = Tweet.objects.filter(conversation_id=conversation_id).only("twitter_id", "author_id")
    G2 = nx.MultiDiGraph()
    G2.add_nodes_from(G.nodes(data=True), subset="tweets")
    G2.add_edges_from(G.edges(data=True), label="parent_of")
    for result_pair in author_tweet_pairs:
        G2.add_node(result_pair.author_id, author=result_pair.author_id, subset="authors")
        G2.add_edge(result_pair.author_id, result_pair.twitter_id, label="author_of")
    return G2


def restrict_conversations_to_reasonable(unhandled_conversation_ids):
    reasonable_small_conversations = []
    for conversation_id in unhandled_conversation_ids:
        if TweetAuthor.objects.filter(tweet__in=Tweet.objects.filter(conversation_id=conversation_id)).count() <= 15:
            reasonable_small_conversations.append(conversation_id)
    return reasonable_small_conversations


def download_conversation_network(conversation_id, conversation_ids, count, levels):
    user_ids = get_participants(conversation_id)
    download_followers_recursively(user_ids, levels, following=True)
    # this would also search the network in the other direction
    download_followers_recursively(user_ids, levels, following=False)
    logger.debug(" {}/{} conversations finished".format(count, len(conversation_ids)))


def prevent_multiple_downloads(conversation_ids):
    unhandled_conversation_ids = []
    for conversation_id in conversation_ids:
        authors_is = set(Tweet.objects.filter(conversation_id=conversation_id).values_list("author_id", flat=True))
        author_part_of_networks = TweetAuthor.objects.filter(twitter_id__in=authors_is). \
            filter(Exists(FollowerNetwork.objects.filter(source_id=OuterRef('pk')))
                   | Exists(FollowerNetwork.objects.filter(target_id=OuterRef('pk')))).distinct()
        assert len(authors_is) > 0
        if not len(author_part_of_networks) > len(authors_is) / 2:
            unhandled_conversation_ids.append(conversation_id)
        else:
            logger.debug("conversation {} has been handled before".format(conversation_id))
    return unhandled_conversation_ids


def draw_author_conversation_dist(conversation_id):
    reply_graph = get_nx_conversation_graph(conversation_id)
    conversation_graph = compute_author_graph(conversation_id)
    root_node = get_root(reply_graph)
    paint_bipartite_author_graph(conversation_graph, root_node=root_node)


def paint_bipartite_author_graph(G2, root_node):
    # Specify the edges you want here
    red_edges = [(source, target, attr) for source, target, attr in G2.edges(data=True) if
                 attr['label'] == 'author_of']
    # edge_colours = ['black' if edge not in red_edges else 'red'
    #                for edge in G2.edges()]
    black_edges = [edge for edge in G2.edges(data=True) if edge not in red_edges]
    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    paint_bipartite(G2, black_edges, red_edges, root_node=root_node)


def paint_bipartite(G2, black_edges, red_edges, root_node):
    # pos = nx.multipartite_layout(G2)

    pos = graphviz_layout(G2, prog="twopi", root=root_node)
    nx.draw_networkx_nodes(G2, pos, node_size=400)
    nx.draw_networkx_labels(G2, pos)
    nx.draw_networkx_edges(G2, pos, edgelist=red_edges, edge_color='red', arrows=True)
    nx.draw_networkx_edges(G2, pos, edgelist=black_edges, arrows=True)
    plt.show()


def paint_reply_graph(conversation_graph: nx.DiGraph):
    assert nx.is_tree(conversation_graph)
    root = get_root(conversation_graph)
    tree = nx.bfs_tree(conversation_graph, root)
    pos = graphviz_layout(tree, prog="twopi")
    # add_attributes_to_plot(conversation_graph, pos, tree)
    nx.draw_networkx_labels(tree, pos)
    nx.draw(tree, pos)
    plt.show()


def add_attributes_to_plot(conversation_graph, pos, tree):
    labels = dict()
    names = nx.get_node_attributes(conversation_graph, 'created_at')
    for node in conversation_graph.nodes:
        labels[node] = f"{names[node]}\n{node}"
    nx.draw_networkx_labels(tree, labels=labels, pos=pos)
