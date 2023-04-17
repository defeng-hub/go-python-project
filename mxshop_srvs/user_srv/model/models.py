from peewee import *

from user_srv.settings import settings


class BaseModel(Model):
    class Meta:
        database = settings.DB


class User(BaseModel):
    Mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    Password = CharField(max_length=200, verbose_name="密码")
    NickName = CharField(max_length=20, null=True, verbose_name="昵称")
    HeadUrl = CharField(max_length=300, null=True, verbose_name="头像")
    Birthday = DateField(null=True, verbose_name="生日")
    Address = CharField(max_length=200, null=True, verbose_name="地址")
    Desc = CharField(verbose_name="个人简介", null=True)

    GENDER_CHOICES = (("female", "女"), ("male", "男"))
    Gender = CharField(max_length=6, choices=GENDER_CHOICES, null=True, verbose_name="性别")

    ROLE_CHOICES = ((1, "普通用户"), (2, "管理员"))
    Role = IntegerField(default=1, verbose_name="用户角色")


if __name__ == '__main__':
    # settings.DB.create_tables([User])

    from passlib.hash import pbkdf2_sha256

    hash = pbkdf2_sha256.hash("123456")
    print(hash)
    print(pbkdf2_sha256.verify("123456", hash))
    print(pbkdf2_sha256.verify("aa", hash))

    for i in range(3):
        user = User()
        user.nick_name = f""
