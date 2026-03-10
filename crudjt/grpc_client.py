# This binding was generated automatically to ensure consistency across languages
# Generated using ChatGPT (GPT-5) from the canonical Ruby SDK
# API is stable and production-ready

import grpc
from .generated import token_service_pb2_grpc

class GrpcClient:
    def __init__(self, address: str):
        self._channel = grpc.insecure_channel(address)
        self._stub = token_service_pb2_grpc.TokenServiceStub(self._channel)

    @property
    def stub(self):
        return self._stub
