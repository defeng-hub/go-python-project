import grpc
from user_srv.proto import user_pb2_grpc, user_pb2


class UserTest:
    def __init__(self):
        # 连接rpc grpc服务器
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel=channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo())

        for u in rsp.Data:
            print(u.NickName, u.Mobile, u.BirthDay, u.Password)
        print("total", rsp.Total)

    def get_user_by_id(self, id):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserByID(user_pb2.IdRequest(Id=id))
        print(rsp.Mobile)
        return rsp

    def get_user_by_mobile(self, mobile):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserByMobile(user_pb2.MobileRequest(Mobile=mobile))
        print(rsp.Mobile)
        return rsp

    def create_user(self, nick_name, mobile, password):
        rsp: user_pb2.UserInfoResponse = self.stub.CreateUser(user_pb2.CreateUserInfo(
            NickName=nick_name,
            Mobile=mobile,
            Password=password
        ))
        print(rsp.Id)

    def update_user(self, Id, NickName, Gender, BirthDay):
        rsp: user_pb2.Empty = self.stub.UpdateUser(user_pb2.UpdateUserInfo(
            Id=Id,
            NickName=NickName,
            Gender=Gender,
            BirthDay=BirthDay
        ))
        print(rsp)


if __name__ == '__main__':
    user = UserTest()
    # user.create_user("www", "18738841574", "123456")
    user.update_user(4, "王德丰", "female", 1680660800)
    user.user_list()
