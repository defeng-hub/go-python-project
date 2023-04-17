import time

import grpc
from loguru import logger

from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.model.models import User


class UserServicer(user_pb2_grpc.UserServicer):

    @logger.catch
    def GetUserList(self, request: user_pb2.PageInfo, context):
        rsp = user_pb2.UserListResponse()
        users = User.select()
        rsp.Total = users.count()
        start = 0
        per_page_nums = 10  # 每页数量
        if request.PageSize:
            per_page_nums = request.PageSize
        if request.Page:
            start = per_page_nums * (request.Page - 1)

        users = users.offset(start).limit(per_page_nums)

        for user in users:
            user_info = user_pb2.UserInfoResponse()
            user_info.Id = user.id
            user_info.Password = user.password
            user_info.Mobile = user.mobile
            user_info.Role = user.role

            if user.nick_name:
                user_info.NickName = user.nick_name
            if user.gender:
                user_info.Gender = user.gender
            if user.birthday:
                user_info.BirthDay = int(time.mktime(user.birthday.timetuple()))

            rsp.Data.append(user_info)
        return rsp
