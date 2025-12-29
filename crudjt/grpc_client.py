import grpc
from .generated import token_service_pb2_grpc

class GrpcClient:
    def __init__(self, address: str):
        self._channel = grpc.insecure_channel(address)
        self._stub = token_service_pb2_grpc.TokenServiceStub(self._channel)

    @property
    def stub(self):
        return self._stub
