import grpc
from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.model.models import User

class UserServicer(user_pb2_grpc.UserServicer):
    def GetUserList(self, request: user_pb2.PageInfo, context):
        rsp = user_pb2.UserListResponse()

        users = User.select()
        for user in users:
            user_info = user_pb2.UserInfoResponse()
            user_info.Id = user.id
            user_info.Password = user.Password
            user_info.Mobile = user.Mobile
            user_info.Role = user.Role
            rsp.data.append(user_info)

