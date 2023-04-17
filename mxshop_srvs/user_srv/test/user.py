import grpc
from user_srv.proto import user_pb2_grpc, user_pb2


class UserTest:
    def __init__(self):
        # 连接rpc grpc服务器
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel=channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(Page=2, PageSize=2))
        print(rsp.Total)

        for user in rsp.Data:
            print(user.Mobile, user.BirthDay)


if __name__ == '__main__':
    user = UserTest()
    user.user_list()
