"""Exposes Amanita via gRPC. """
import time
from concurrent import futures

import grpc

import app.services.amanita_pb2 as amanita_pb2
import app.services.amanita_pb2_grpc as amanita_pb2_grpc
from app.apiparams.mapping import map_param_values_to_given_definitions
from app.clients.elastic.client import ESClient
from app.clients.elastic.process_response import map_client_results_to_proto_resultset, \
    map_client_item_to_proto_minimal_item
from app.clients.sparql.client import SPARQLClient
from app.utils import logging
from app.utils.conversions import map_grpc_request_params_to_dict
from app.utils.global_vars import ONE_DAY_IN_SECONDS, MAX_WORKERS, DB_ENDPOINT, DB_USER, DB_PASS, DB_CLIENT
from exceptions.clientexceptions import InvalidClientName

logger = logging.get_logger(__name__)

logger.info(f'Using credentials:\n endpoint: {DB_ENDPOINT}\n user: {DB_USER}\n pass: {DB_PASS}')

db_client_classes = {
    'stardog': SPARQLClient,
    'elasticsearch': ESClient
}


def get_client(db_client_name):
    try:
        client = db_client_classes[db_client_name](DB_ENDPOINT, DB_USER, DB_PASS)
    except KeyError:
        raise InvalidClientName(
            f'Client {db_client_name} is not implemented, choose from {list(db_client_classes)}')
    return client


class Amanita(amanita_pb2_grpc.DatalabAmanitaAPIServiceServicer):

    def ListContent(self, request, context):
        client = get_client(DB_CLIENT)
        query_params = map_grpc_request_params_to_dict(request)
        mapped_params = map_param_values_to_given_definitions(client.get_parameter_definitions('rpc'), 'content',
                                                              query_params)
        result = client.get_content(mapped_params)
        mapped_result = map_client_results_to_proto_resultset(result)
        return mapped_result

    def ListSimilarItems(self, request, context):
        client = get_client(DB_CLIENT)
        query_params = map_grpc_request_params_to_dict(request)
        mapped_params = map_param_values_to_given_definitions(client.get_parameter_definitions('rpc'), 'similar',
                                                              query_params)
        result = client.get_similar(mapped_params)
        mapped_result = map_client_results_to_proto_resultset(result)
        return mapped_result

    def Item(self, request, context):
        client = get_client(DB_CLIENT)
        query_params = map_grpc_request_params_to_dict(request)
        mapped_params = map_param_values_to_given_definitions(client.get_parameter_definitions('rpc'), 'item',
                                                              query_params)
        result = client.get_item(mapped_params)
        mapped_result = map_client_item_to_proto_minimal_item(result)
        return mapped_result

    def HealthCheck(self, request, context):
        return amanita_pb2.HealthCheckResponse(
            message='AMANITA',
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    amanita_pb2_grpc.add_DatalabAmanitaAPIServiceServicer_to_server(Amanita(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()
    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
