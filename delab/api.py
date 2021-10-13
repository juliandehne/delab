import json

from django.http import HttpResponseNotFound
from django_filters.rest_framework import DjangoFilterBackend
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework import serializers, viewsets
from django.utils.encoding import smart_text
from rest_framework import renderers

# Serializers define the API representation.
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from delab.corpus.filter_conversation_trees import crop_trees, filter_conversations, get_filtered_conversations, \
    get_conversation_tree
from delab.models import Tweet

tweet_fields_used = ['id', 'twitter_id', 'text', 'conversation_id', 'author_id', 'created_at', 'in_reply_to_user_id',
                     'tn_children_pks',
                     'tn_order',
                     'sentiment_value', 'language']


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = tweet_fields_used


class TabbedTextRenderer(renderers.BaseRenderer):
    # here starts the wonky stuff
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)


def get_migration_query_set():
    queryset = Tweet.objects.filter(simple_request__topic__title="migration")
    return get_cropped_tweet_set(queryset)


def get_cropped_tweet_set(queryset):
    df = queryset.all().to_dataframe(tweet_fields_used)
    trees, ids, conversation_ids = crop_trees(df)
    # print(ids)
    queryset = queryset.filter(id__in=ids)
    return queryset


# ViewSets define the view behavior.
class TweetViewSet(viewsets.ModelViewSet):
    queryset = get_migration_query_set()
    serializer_class = TweetSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['conversation_id', 'tn_order', 'author_id', 'language']
    filterset_fields = tweet_fields_used
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


# ViewSets define the view behavior.
class TweetExcelViewSet(XLSXFileMixin, viewsets.ModelViewSet):
    queryset = get_migration_query_set()
    serializer_class = TweetSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'twitter_migration_export.xlsx'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = tweet_fields_used
    # filterset_fields = ['conversation_id', 'tn_order', 'author_id', 'language']


class TweetSingleViewSet(TweetViewSet):
    def get_queryset(self):
        queryset = get_cropped_conversation_qs_modelview(self)
        # TODO find out why the text api produces more tweets then this one
        return queryset


class TweetExcelSingleViewSet(TweetExcelViewSet):
    def get_queryset(self):
        queryset = get_cropped_conversation_qs_modelview(self)
        return queryset


def get_cropped_conversation_qs_modelview(model_view):
    conversation_id = model_view.kwargs["conversation_id"]
    queryset = Tweet.objects.filter(simple_request__topic__title="migration", conversation_id=conversation_id)
    if model_view.kwargs["full"] == "cropped":
        queryset = get_cropped_tweet_set(queryset)
    return queryset


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_cropped_conversation_ids(request):
    trees, ids, conversation_ids = filter_conversations()
    result = {"suitable_conversation_ids": conversation_ids}
    return Response(result)


@api_view(['GET'])
@renderer_classes([TabbedTextRenderer])
def get_all_tabbed_conversation_view(request):
    trees, ids, conversation_ids = filter_conversations()
    result = ""
    for tree in trees:
        result += tree.to_string() + "\n\n"
    return Response(result)


@api_view(['GET'])
@renderer_classes([TabbedTextRenderer])
def get_tabbed_conversation_view(request, conversation_id, full):
    if full == "cropped":
        # get_conversation_tree
        trees, ids, conversation_ids = get_filtered_conversations(conversation_id, "migration")
        conversation_trees = trees
        if not conversation_id:
            return " ".join(conversation_ids)

        if conversation_id not in conversation_ids:
            return HttpResponseNotFound("The conversation id was not found within the cropped trees")
    else:
        conversation_trees = get_conversation_tree(conversation_id, "migration", tweet_fields_used).values()
    result = ""
    for tree in conversation_trees:
        result += tree.to_string() + "\n\n"
    return Response(result)
