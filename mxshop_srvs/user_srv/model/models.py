from peewee import *

from user_srv.settings import settings


class BaseModel(Model):
    class Meta:
        database = settings.DB


class User(BaseModel):
    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=200, verbose_name="密码")
    nick_name = CharField(max_length=20, null=True, verbose_name="昵称")
    head_url = CharField(max_length=300, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=200, null=True, verbose_name="地址")
    desc = CharField(verbose_name="个人简介", null=True)

    GENDER_CHOICES = (("female", "女"), ("male", "男"))
    gender = CharField(max_length=6, choices=GENDER_CHOICES, null=True, verbose_name="性别")

    ROLE_CHOICES = ((1, "普通用户"), (2, "管理员"))
    role = IntegerField(default=1, verbose_name="用户角色")


if __name__ == '__main__':
    # settings.DB.create_tables([User])

    from passlib.hash import pbkdf2_sha256
    #
    # hash = pbkdf2_sha256.hash("123456")
    # print(hash)
    # print(pbkdf2_sha256.verify("123456", hash))
    # print(pbkdf2_sha256.verify("aa", hash))
    #
    # for i in range(9):
    #     user = User()
    #     user.nick_name = "wdf{}".format(i)
    #     user.mobile = "1333372857{}".format(i)
    #     user.password = pbkdf2_sha256.hash("123456")
    #     user.gender = "male"
    #     user.role = 1
    #     user.save()

    # users = User.select()
    # users = users.limit(2).offset(0)
    # for user in users:
    #     print(user.mobile)

