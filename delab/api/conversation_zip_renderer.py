"""
In this file we bundle the methods used for exporting our current data as a zip file

"""
import io
import zipfile

import requests
from django.http import HttpResponse

from django_project.settings import INTERNAL_IPS
from .api_util import get_file_name, get_all_conversation_ids
from delab.analytics.cccp_analytics import compute_cccp_candidate_authors, compute_all_cccp_authors


def create_zip_response_conversation(request, topic, conversation_id, filename):
    # Create zip

    buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(buffer, 'w')

    download_conversations_in_all_formats(conversation_id, request, topic, zip_file, "both")

    zip_file.close()

    # Return zip
    response = HttpResponse(buffer.getvalue())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    return response


def download_conversations_in_all_formats(conversation_id, request, topic, zip_file, full):
    full_string = "full"
    full_cropped_string = "cropped"
    server_adress = "http://" + INTERNAL_IPS[0] + ":" + request.META['SERVER_PORT']
    file_type_text = "tweets_text"

    """
    if full == "cropped" or full == "both":
        cropped_response = get_file_from_rest(conversation_id, file_type_text, full_cropped_string, server_adress,
                                              topic)
        zip_file.writestr(get_file_name(conversation_id, full_cropped_string, ".txt"), cropped_response.content)
        cropped_response = get_file_from_rest(conversation_id, "tweets_excel", full_cropped_string, server_adress,
                                              topic)
        zip_file.writestr(get_file_name(conversation_id, full_cropped_string, ".xlsx"), cropped_response.content)

        # cropped_response = get_file_from_rest(conversation_id, "tweets_json", full_cropped_string, server_adress, topic)
        # zip_file.writestr(get_file_name(conversation_id, full_cropped_string, ".json"), cropped_response.content)
    """
    if full == "full" or full == "both":
        cropped_response = get_file_from_rest(conversation_id, "tweets_json", full_string, server_adress, topic)
        zip_file.writestr(get_file_name(conversation_id, full_string, ".json"), cropped_response.content)
        cropped_response = get_file_from_rest(conversation_id, file_type_text, full_string, server_adress, topic)
        zip_file.writestr(get_file_name(conversation_id, full_string, ".txt"), cropped_response.content)
        cropped_response = get_file_from_rest(conversation_id, "tweets_excel", full_string, server_adress, topic)
        zip_file.writestr(get_file_name(conversation_id, full_string, ".xlsx"), cropped_response.content)
        cropped_response = get_file_from_rest(conversation_id, "tweets_xml", full_string, server_adress, topic)
        zip_file.writestr(get_file_name(conversation_id, full_string, ".xml"), cropped_response.content)


def get_file_from_rest(conversation_id, file_type, full, server_address, topic):
    txt_cropped_url = "{}/delab/rest/{}/{}/conversation/{}/{}".format(server_address,
                                                                      topic,
                                                                      file_type,
                                                                      str(conversation_id),
                                                                      full)
    if file_type == "tweets_json":
        txt_cropped_url += "?format=json"
    # Get file
    cropped_response = requests.get(txt_cropped_url)
    # cropped_response
    return cropped_response


def download_flows_in_all_formats(conversation_id, request, zip_file):
    server_address = "http://" + INTERNAL_IPS[0] + ":" + request.META['SERVER_PORT']
    url = "{}/delab/rest/flow_text/conversation/{}".format(server_address, conversation_id)
    text_file_response = requests.get(url)
    zip_file.writestr("conversation_flow_{}.txt".format(str(conversation_id)), text_file_response.content)


def create_full_zip_response_conversation(request, topic, filename, full):
    buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(buffer, 'w')

    conversation_ids = get_all_conversation_ids(topic)
    # sample_size = min(len(conversation_ids), 10)
    # conversation_ids = conversation_ids[:sample_size]
    for conversation_id in conversation_ids:
        download_conversations_in_all_formats(conversation_id, request, topic, zip_file, full)
        download_flows_in_all_formats(conversation_id, request, zip_file)

    zip_file.close()

    # Return zip
    response = HttpResponse(buffer.getvalue())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    return response


def download_cccp_text(conversation_id, author_id, measure, request, zip_file):
    server_address = "http://" + INTERNAL_IPS[0] + ":" + request.META['SERVER_PORT']
    url = "{}/delab/rest/cccp/conversation/{}/author/{}".format(server_address, conversation_id, author_id)
    text_file_response = requests.get(url)
    zip_file.writestr("cccp_tree_{}_{}_{}.txt".format(measure, str(conversation_id), str(author_id)),
                      text_file_response.content)


def create_zip_response_cccp(request):
    # Create zip

    buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(buffer, 'w')
    filename = "cccp_conversations.zip"

    candidate_lists, measure_authors_dictionary, author2measure = compute_all_cccp_authors()
    for conversation_id, author_id in candidate_lists:
        measure = author2measure[author_id]
        download_cccp_text(conversation_id, author_id, measure, request, zip_file),

    zip_file.close()

    # Return zip
    response = HttpResponse(buffer.getvalue())
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    return response
