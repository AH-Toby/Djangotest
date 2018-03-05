from datetime import date

from django.db.models import F, Sum, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from booktest.models import BookInfo, HeroInfo, AreaInfo


def index(request):
    # 查询等：
    # eg:查询编号为1的图书
    # 获取id = 1的图书对象
    # get方法，获取的结果为空会报错，如果结果数量大于一个也会报错
    book = BookInfo.objects.get(id=1)
    # 使用filter查询得到的是多个数据
    # books = BookInfo.objects.filter(id=1)  # 简写
    books = BookInfo.objects.filter(id__exact=1)  # 完整写法

    # 模糊查询：contains：是否包含
    # eg:查询书名包含'湖'的图书
    # list = BookInfo.objects.filter(btitle__contains='湖')

    # 空查询：isnull:是否为null
    # eg:查询不为空的图书
    # list = BookInfo.objects.filter(btitle__isnull=False)

    # 范围查询： in:是否包含在范围内
    # eg:查询编号为1或3或5的图书
    # list = BookInfo.objects.filter(id__in=[1, 3, 5])

    # 比较查询：gt(大于), gte(大于等于), lt(小于), lte(小于等于)
    # eg:查询编号大于(大于等于，小于，小于等于)3的图书
    # list = BookInfo.objects.filter(id__gt=3)
    # list = BookInfo.objects.filter(id__gte=3)
    # list = BookInfo.objects.filter(id__lt=3)
    # list = BookInfo.objects.filter(id__lte=3)

    # 不等于运算符，使用exclude()过滤器
    # eg:查询编号不等于3的图书
    # list = BookInfo.objects.exclude(id=3)

    # 日期查询：year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算。
    # eg:查询1980年发表的图书
    # list = BookInfo.objects.filter(bpub_date__year=1980)

    # eg:查询1980年1月1日后发表的图书
    # list = BookInfo.objects.filter(bpub_date__gt=date(1980, 1, 1))

    # F对象：F(属性名)，用于查询两个属性间的比较
    # eg：查询阅读量大于等于评论量的图书
    # list = BookInfo.objects.filter(bread__gte=F('bcomment'))

    # 可以在F对象上使用算数运算
    # eg: 查询阅读量大于2倍评论量的图书
    # list = BookInfo.objects.filter(bread__gte=F('bcomment')*2)

    # Q对象：Q(属性名__运算符=值)：多个过滤器逐个调用表示逻辑与关系
    # Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或。

    # eg:查询阅读量大于20，并且编号小于3的图书。
    # ,同sql语句中where部分的and关键字,一般表示并且不用Q对象直接使用,
    # list = BookInfo.objects.filter(bread__gte=20, id__lt=3)
    # list = BookInfo.objects.filter(bread__gte=20).filter(id__lt=3)  # 等同于上面的写法
    # list = BookInfo.objects.filter(Q(bread__gte=20) & Q(id__lt=3))  # 等同于第一步

    # eg:查询阅读量大于20的图书，改写为Q对象如下
    # list = BookInfo.objects.filter(Q(bread__gt=20))

    # 表示或的化只能使用Q标签
    # eg:询阅读量大于20，或编号小于3的图书，只能使用Q对象实现
    # list = BookInfo.objects.filter(Q(bread__gt=20) | Q(id__lt=3))

    # Q对象前可以使用~操作符，表示非not。
    # eg:查询编号不等于3的图书。
    list = BookInfo.objects.filter(~Q(pk=3))  # pk代表自动生成的主键

    # 聚合函数
    # 使用aggregate()过滤器调用聚合函数。
    # 聚合函数包括：Avg，Count，Max，Min，Sum，被定义在django.db.models中。

    # eg:查询图书的总阅读量。aggregate 聚合函数
    # {‘bread__sum’:126}   聚合函数返回的是一个字典 key:字段名字__函数名小写
    dictread = BookInfo.objects.aggregate(Sum('bread'))
    # 获取字典的值
    readsum = dictread.get('bread__sum')

    # 使用count时一般不使用aggregate()过滤器。
    # eg:查询图书总数。
    booksum = BookInfo.objects.count()
    context = {'book': book, 'books': books, 'list': list, 'readsum': readsum, 'booksum': booksum}
    return render(request, 'booktest/index.html', context)


# 查询集
# 从数据库中获取的对象集合，在管理器上调用某些过滤器方法会返回查询集，
# 查询集可以含有零个、一个或多个过滤器
def testQuery(request):
    # 特性1：惰性执行 什么时候使用books什么时候执行sql语句
    # books = BookInfo.objects.all()
    books = BookInfo.objects.all()[0:2]  # 对查询的结果进行切片操作
    return render(request, 'booktest/testQuery.html', {'books': books})


def testQuery1(request):
    # 特性2： 缓存
    # 查询集在第一次被使用数据 会执行SQL 然后结果会缓存 后面再次使用这个查询集 就不会查询了
    # 下面会产生两个查询集对象会执行
    [book.btitle for book in BookInfo.objects.all()]
    [book.btitle for book in BookInfo.objects.all()]

    # 下面只会产生一个查询集对象，只会执行一次sql语句
    books = BookInfo.objects.all()
    [book.btitle for book in books]
    [book.btitle for book in books]

    return HttpResponse('ok')


# 测试关联查询 1：n
def testjoin(request):
    # 查询id为1的图书
    book = BookInfo.objects.get(id=1)

    # 获取图书所有的英雄 1：n  关联的类名小写_set
    heros = book.heroinfo_set.all()

    # 查询id为1的英雄
    hero = HeroInfo.objects.get(id=1)
    # hbook已经在HeroInfo类里面定义了 就是属于的图书对象
    book1 = hero.hbook
    context = {'book': book, 'heros': heros, 'hero': hero, 'book1': book1}
    return render(request, 'booktest/testjoin.html', context)


# 通过模型类执行关联查询(多表查询)
def testjoin1(request):
    # eg:查询图书，要求图书中英雄的描述包含'八'。
    # 关联模型类名小写__属性名__条件运算符=值（由多模型类条件查询一模型类数据:
    # 生成inner... join..。查询
    books = BookInfo.objects.filter(heroinfo__hcontent__contains='八')

    # 由一模型类条件查询多模型类数据:一模型类关联属性名__一模型类属性名__条件运算符=值
    # eg:查询书名为“天龙八部”的所有英雄。
    heroes = HeroInfo.objects.filter(hbook__btitle='天龙八部')
    context = {'books': books, 'heroes': heroes}
    return render(request, 'booktest/testjoin1.html', context)


# 自关联
def testself(request):
    # 查询广州市
    # areainfo = AreaInfo.objects.get(atitle='广州市')

    # 查询北京市
    areainfos = AreaInfo.objects.filter(atitle='北京市')
    # 如果是直辖市 会返回多个在做之间需要判断
    if areainfos.count() > 1:
        areainfo = areainfos[1]
    else:
        areainfo = areainfos[0]

    # 查询广州市所在的省份
    parent = areainfo.aParent
    # 查询广州市有那些区县
    children = areainfo.areainfo_set.all()
    context = {'areainfo': areainfo, 'parent': parent, 'children': children}
    return render(request, 'booktest/testself.html', context)


# 显示创建页面
def showbooks(request):
    books = BookInfo.bookmanage.all()
    context = {'books': books}
    return render(request, 'booktest/showbooks.html', context)


# 创建一本书
def createbook(request):
    # # 实例化一本图书对象
    # book = BookInfo()
    # book.btitle = '流星蝴蝶剑'
    # book.bpub_date = date(2018, 2, 26)
    # # save方法 把数据添加到数据库 相当于insert/update
    # book.save()
    BookInfo.bookmanage.createbook('流星蝴蝶剑', date(2018, 2, 26))
    # 重定向到其他视图
    return redirect('/showbooks')


# 删除一本图书
def deletebook(request, bookid):
    BookInfo.bookmanage.deletebook(bookid)
    # 重定向到其他视图
    return redirect('/showbooks')


def testwork(request):
    # 1.查询性别为男的英雄
    # hero = HeroInfo.objects.filter(hgender=True)

    # 2.查询姓黄的男性英雄
    # hero = HeroInfo.objects.filter(hname__startswith='黄',hgender=True)

    # 3.查询图书名为“天龙八部”的英雄
    # hero = HeroInfo.objects.filter(hbook__btitle='天龙八部')

    # 4.查询编号小于5或性别为女的英雄
    hero = HeroInfo.objects.filter(Q(id__lt=5) | Q(hgender=False))

    # 5.查询女生总人数
    count = HeroInfo.objects.filter(hgender=False).count()
    context = {'hero': hero, 'count': count}
    return render(request, 'booktest/testwork.html', context)
