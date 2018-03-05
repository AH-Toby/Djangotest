from django.db import models


# Create your models here.
# 写一个管理器的子类
class BookInfoManage(models.Manager):
    # 原始查询集，一启动程序就开始查询
    def get_queryset(self):
        # super().get_queryset()获取父级的原始查询结果
        # filter(isDelete=False)对查询的结果条件过滤 然后返回
        return super().get_queryset().filter(isDelete=False)

    # 把创建的方法封装到管理器中
    def createbook(self, title, date):
        # 实例化一本图书对象
        book = BookInfo()
        book.btitle = title
        book.bpub_date = date
        # save方法 把数据添加到数据库 相当于insert/update
        book.save()
        # 重定向到其他视图
        return book

    # 把删除的方法封装到管理器中
    def deletebook(self, bookid):
        # 获取图书
        book = BookInfo.bookmanage.get(id=bookid)
        # 删除图书
        # book.delete()

        # 逻辑删除 相当于update
        book.isDelete = True
        book.save()
        return book


# 创建数据表
# 定义图书模型类BookInfo   表名 = 应用名字_类名小写
class BookInfo(models.Model):  # 表名，括号里面是继承
    # 属性 = models.字段类型0(选项(约束))
    # db_column 定义字段在数据库中的名字，如果不去指定就是btitle
    btitle = models.CharField(max_length=20, db_column='title')  # 图书名称
    bpub_date = models.DateField()  # 发布日期
    bread = models.IntegerField(default=0)  # 阅读量，默认为0
    bcomment = models.IntegerField(default=0)  # 评论量，默认为0
    isDelete = models.BooleanField(default=False)  # 逻辑删除

    # 如果自己生成的管理器那么objects就不在生成了
    bookmanage = BookInfoManage()
    objects = models.Manager()  # 管理器可以有多个

    # 元选项自定义表名(注意迁移)
    class Meta:
        db_table = 'bookinfo'


# 定义英雄模型类
class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)  # 英雄姓名
    hgender = models.BooleanField(default=True)  # 英雄的性别
    isDelete = models.BooleanField(default=False)  # 逻辑删除
    hcontent = models.CharField(max_length=20)  # 英雄描述
    # hbook是一个对象
    hbook = models.ForeignKey('BookInfo')  # 英雄与图书表的关系为一对多，所以属性定义在英雄模型类中


# 多对多的关系
class TypeInfo(models.Model):
    tname = models.CharField(max_length=20)  # 新闻类别

    def __str__(self):
        return self.tname


class NewsInfo(models.Model):
    ntitle = models.CharField(max_length=60)  # 新闻标题
    ncontent = models.TextField()  # 新闻内容
    npub_date = models.DateTimeField(auto_now_add=True)  # 新闻发布时间
    ntype = models.ManyToManyField('TypeInfo')  # 通过ManyToManyField建立TypeInfo类和NewsInfo类之间多对多的关系

    def __str__(self):
        return self.ntitle


# 定义地区模型类，存储省、市、区县信息
class AreaInfo(models.Model):
    atitle = models.CharField(max_length=30)  # 名称
    aParent = models.ForeignKey('self', null=True, blank=True)  # 关系
