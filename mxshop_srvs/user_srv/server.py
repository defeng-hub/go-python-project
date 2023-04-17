import os
import sys
from concurrent import futures
import logging
import grpc
import signal
from loguru import logger

# abspath 把 "/" 变成 "\"
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)
logger.info("BASE_DIR: {}".format(BASE_DIR))

from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.handler.user import UserServicer


def init_path():
    BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    sys.path.insert(0, BASE_DIR)

    print(BASE_DIR)


def on_exit(signo, frame):
    logger.warning("终端终止")
    sys.exit(0)


def serve():
    # 初始化logger
    logger.add("logs/user_srv_{time}.log", rotation="125 MB")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')

    """
        windows 下支持的信号有限
        SIGINT ctrl+c 终端
        SIGTERM kill 发出软件终止
    """
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    server.start()
    logger.debug("启动服务0:50051")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
