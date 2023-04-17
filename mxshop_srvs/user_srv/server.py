from concurrent import futures
import logging
import grpc

from loguru import logger
from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.handler.user import UserServicer


def serve():
    # 初始化logger
    logger.add("logs/user_srv_{time}.log", rotation="125 MB")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')

    logger.debug("启动服务0:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
