import argparse
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


def on_exit(signo, frame):
    logger.warning("终端终止")
    sys.exit(0)


def serve():
    # 1. 获取args
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', nargs="?", type=str, default="127.0.0.1", help="绑定ip")
    parser.add_argument('--port', nargs="?", type=int, default=50051, help="端口")
    args = parser.parse_args()
    # 初始化logger
    logger.add("logs/user_srv_{time}.log", rotation="125 MB")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port(f"{args.ip}:{args.port}")

    """
        windows 下支持的信号有限
        SIGINT ctrl+c 终端
        SIGTERM kill 发出软件终止
    """
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    server.start()
    logger.debug("服务启动: "+f"{args.ip}:{args.port}")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
