import grpc
from concurrent import futures
import msgpack

from .generated import token_service_pb2
from .generated import token_service_pb2_grpc

class TokenServiceImpl(token_service_pb2_grpc.TokenServiceServicer):

    @classmethod
    def call(cls, port: str) -> grpc.Server:
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=2)
        )

        token_service_pb2_grpc.add_TokenServiceServicer_to_server(
            cls(), server
        )

        server.add_insecure_port(port)

        return server

    def CreateToken(self, request, context):
        packed_data = msgpack.unpackb(request.packed_data, raw=False)

        ttl = request.ttl
        silence_read = request.silence_read

        # proto int64 не вміє nil → sentinel
        ttl = None if ttl == -1 else ttl
        silence_read = None if silence_read == -1 else silence_read

        token = CRUDJT.original_create(
            packed_data,
            ttl=ttl,
            silence_read=silence_read
        )

        return token_service_pb2.CreateTokenResponse(token=token)

    def ReadToken(self, request, context):
        raw_token = request.token

        result_hash = CRUDJT.original_read(raw_token)
        packed_data = msgpack.packb(result_hash, use_bin_type=True)

        return token_service_pb2.ReadTokenResponse(
            packed_data=packed_data
        )

    def UpdateToken(self, request, context):
        raw_token = request.token
        packed_data = msgpack.unpackb(request.packed_data, raw=False)

        ttl = request.ttl
        silence_read = request.silence_read

        ttl = None if ttl == -1 else ttl
        silence_read = None if silence_read == -1 else silence_read

        result = CRUDJT.original_update(
            raw_token,
            packed_data,
            ttl=ttl,
            silence_read=silence_read
        )

        return token_service_pb2.UpdateTokenResponse(result=result)

    def DeleteToken(self, request, context):
        raw_token = request.token

        result = CRUDJT.original_delete(raw_token)

        return token_service_pb2.DeleteTokenResponse(result=result)
