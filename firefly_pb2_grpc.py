# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import firefly_pb2 as firefly__pb2


class FireflyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendPhases = channel.unary_unary(
                '/FireflyService/SendPhases',
                request_serializer=firefly__pb2.PhasesRequest.SerializeToString,
                response_deserializer=firefly__pb2.PhasesResponse.FromString,
                )
        self.GetPosition = channel.unary_unary(
                '/FireflyService/GetPosition',
                request_serializer=firefly__pb2.PositionRequest.SerializeToString,
                response_deserializer=firefly__pb2.PositionResponse.FromString,
                )


class FireflyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendPhases(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPosition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FireflyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendPhases': grpc.unary_unary_rpc_method_handler(
                    servicer.SendPhases,
                    request_deserializer=firefly__pb2.PhasesRequest.FromString,
                    response_serializer=firefly__pb2.PhasesResponse.SerializeToString,
            ),
            'GetPosition': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPosition,
                    request_deserializer=firefly__pb2.PositionRequest.FromString,
                    response_serializer=firefly__pb2.PositionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'FireflyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FireflyService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendPhases(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FireflyService/SendPhases',
            firefly__pb2.PhasesRequest.SerializeToString,
            firefly__pb2.PhasesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPosition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FireflyService/GetPosition',
            firefly__pb2.PositionRequest.SerializeToString,
            firefly__pb2.PositionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
