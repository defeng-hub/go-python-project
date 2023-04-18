import time
from datetime import date

import grpc
from loguru import logger
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from google.protobuf import empty_pb2
from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.model.models import User
from peewee import DoesNotExist


class UserServicer(user_pb2_grpc.UserServicer):

    @staticmethod  # user模型转 user_pb2.UserInfoResponse
    def UserModelToUserInfoRsp(user) -> user_pb2.UserInfoResponse:
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
        return user_info

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
            user_info = self.UserModelToUserInfoRsp(user)
            rsp.Data.append(user_info)
        return rsp

    @logger.catch
    def GetUserByID(self, request: user_pb2.IdRequest, context):
        try:
            user = User.get(User.id == request.Id)
            return self.UserModelToUserInfoRsp(user)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def GetUserByMobile(self, request: user_pb2.MobileRequest, context):
        try:
            user = User.get(User.mobile == request.Mobile)
            return self.UserModelToUserInfoRsp(user)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def CreateUser(self, request: user_pb2.CreateUserInfo, context):  # 新建用户
        try:
            User.get(User.mobile == request.Mobile)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户已经存在")
            return user_pb2.UserInfoResponse()
        except DoesNotExist as e:
            user = User()
            #   string NickName = 1;
            #   string Password = 2;
            #   string Mobile = 3;
            user.nick_name = request.NickName
            user.mobile = request.Mobile
            user.password = pbkdf2_sha256.hash(request.Password)
            user.save()
            return self.UserModelToUserInfoRsp(user)

    @logger.catch
    def UpdateUser(self, request: user_pb2.UpdateUserInfo, context):
        try:
            user = User.get(User.id == request.Id)
            #   int32 Id = 1;
            #   string NickName = 2;
            #   string Gender = 3;
            #   uint64 BirthDay = 4;
            user.nick_name = request.NickName
            user.gender = request.Gender
            user.birthday = date.fromtimestamp(request.BirthDay)
            user.save()
            return user_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

