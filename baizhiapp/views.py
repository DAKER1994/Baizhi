import json
import uuid
# from datetime import timezone
# from time import timezone

from django.core import paginator
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render,HttpResponse
# Create your views here.
from django.utils import timezone

from baizhiapp.models import TTest,TZpgg,TUser,VisitNumber,User_ip,DayNumber
from baizhiapp import models, checkIP
from lxml import etree
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, PKCS1_OAEP
import base64


def decrypt_params(privkey,param):
    comfirm_param = base64.b64decode(param)
    # 私钥
    encrypted_key = RSA.import_key(privkey)
    cipher_rsa2 = PKCS1_v1_5.new(encrypted_key)
    data = cipher_rsa2.decrypt(comfirm_param,None)
    return bytes.decode(data)


def decorate(func):  # 修改网站访问量和访问ip等信息
    def inner(request,*args, **kwargs):
        try:
        # 每一次访问，网站总访问次数加一
            count_nums = VisitNumber.objects.filter(id=1)
            if count_nums:
                count_nums = count_nums[0]
                count_nums.count += 1
            else:
                count_nums = VisitNumber()
                count_nums.count = 1
            count_nums.save()
            # print(request.META)
            # 记录访问ip和每个ip的次数
            if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
                client_ip = request.META['HTTP_X_FORWARDED_FOR']
                client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
            else:
                client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip
            d_client_ip={'ip': client_ip}
            # print(d_client_ip)

            ip_exist = User_ip.objects.filter(ip=str(client_ip))
            if ip_exist:  # 判断是否存在该ip
                uobj = ip_exist[0]
                uobj.country = checkIP.checkip(d_client_ip)[0]
                uobj.province = checkIP.checkip(d_client_ip)[1]
                uobj.city = checkIP.checkip(d_client_ip)[2]
                uobj.operator = checkIP.checkip(d_client_ip)[3]
                uobj.create_times=timezone.datetime.now()
                uobj.count += 1
            else:
                uobj = User_ip()
                uobj.ip = client_ip
                uobj.country=checkIP.checkip(d_client_ip)[0]
                uobj.province=checkIP.checkip(d_client_ip)[1]
                uobj.city=checkIP.checkip(d_client_ip)[2]
                uobj.operator=checkIP.checkip(d_client_ip)[3]
                uobj.create_times = timezone.datetime.now()
                uobj.count = 1
            uobj.save()

            # 增加今日访问次数
            date = timezone.now().date()
            today = DayNumber.objects.filter(day=date)
            if today:
                temp = today[0]
                temp.count += 1
            else:
                temp = DayNumber()
                temp.dayTime = date
                temp.count = 1
            temp.save()
        except:
            pass
        return func(request,*args, **kwargs)
    return inner


@decorate
def introduce(request):
    return render(request,'baizhiapp/introduce.html')

def login(request):

    return render(request,'baizhiapp/login.html')

@decorate
def main(request):
    # 生成密钥
    key = RSA.generate(1024)
    # 公钥
    exportKey = key.publickey().exportKey()
    # 私钥
    encrypted_key = key.exportKey()
    # 私钥和公钥放入session
    request.session['privkey'] = bytes.decode(encrypted_key)
    request.session['publickey'] = bytes.decode(exportKey)
    s = str(uuid.uuid4())
    sess = request.session.get('username')
    response = render(request,'baizhiapp/main.html',{'sess':sess})
    response.set_cookie('asd',s)  # 设置新cookie

    request.session['random'] =  s  # 后端记住随机串
    # print(s,'我存的cookie')
    return  response

@decorate
def menu(request):
    privkey = request.session.get('privkey')
    publickey = request.session.get('publickey')

    city=request.GET.get('city')
    job=request.GET.get('job')
    number = request.GET.get('number')
    if number:
        number = number.replace(' ','+')
        print('加密的numberrrrrrrrrrrrr', number)
        number = decrypt_params(privkey,number)
        print('解密后的',number)
    # numebr = decrypt_params()
    print(city, job, '77777777777777777')
    if len(job) >10 or len(city)>10:
        city = city.replace(' ','+')
        job = job.replace(' ','+')
        city = decrypt_params(privkey,city)
        job = decrypt_params(privkey,job)
        print('解密后城市工作',city,job)

    # print(request.META,'sssss')
    # select=TZpgg.objects.filter(hope_location=city,hope_position=job)
    user_agent=request.META['HTTP_USER_AGENT']


    ran_cookie = request.COOKIES.get('asd')  # 从浏览器中获得的上次存进去的
    ran_session = request.session.get('random')  # 从数据库中拿出随机cookie值
    print(ran_session)
    # employers = TZpgg.objects.all().order_by("-id")

    employers = TZpgg.objects.filter(hope_location=city,hope_position__icontains=job)

    if 'python' in user_agent:
        return HttpResponse('asdhjaksf')
    if not number:
        number = 1
    pagtor = Paginator(employers, per_page=10)

    if ran_cookie == ran_session:
        page = pagtor.page(int(number))
        resp = render(request,'baizhiapp/menu.html',{'page':page,'employers':employers,'number':number,'city':city,'job':job,'publickey':publickey})
        s = str(uuid.uuid4())
        resp.set_cookie('asd',s)
        request.session['random'] = s
        return resp
    else:
        page = pagtor.page(1)
        print(city,job,'qqqqqqqqqqqqqqqqq')
        return  render(request,'baizhiapp/menu.html',{'page':page,'employers':employers,'number':number,'city':city,'job':job,'publickey':publickey})

def register(request):
    return render(request,'baizhiapp/register.html')

def register_logic(request):
    username = request.POST.get('username')
    usertel = request.POST.get('usertel')
    email = request.POST.get('email')
    password = request.POST.get('password')
    dataname = TUser.objects.filter(username=username)
    if not dataname:
        new_user = models.TUser.objects.create(username=username,usertel=usertel,email=email,password=password)
        print(new_user)
        if new_user:
            return redirect('baizhiapp:login')
    return redirect('baizhiapp:register')

def login_logic(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    dataname = TUser.objects.filter(username=username)
    datapwd = TUser.objects.filter(password=password)
    if dataname and datapwd:
        request.session['username'] = username
        return redirect('baizhiapp:main')
    return redirect('baizhiapp:login')
#



from aliyunsdkcore import client
from aliyunsdkafs.request.v20180112 import AuthenticateSigRequest
from aliyunsdkcore.profile import region_provider

def move_code(request):   #登录验证
    sessionid = request.GET.get('csessionid')
    sig = request.GET.get('sig')
    token = request.GET.get('nc_token')
    region_provider.add_endpoint('afs', 'cn-hangzhou', 'afs.aliyuncs.com')

    clt = client.AcsClient('LTAIXrRJT7ikiMG7','mJpj344qlvwy33ImCikjVoAYvNaN5K','cn-hangzhou')
    request = AuthenticateSigRequest.AuthenticateSigRequest()


    #必填参数：从前端获取，不可更改，android和ios只传这个参数即可
    request.set_SessionId(sessionid)
    #必填参数：从前端获取，不可更改
    request.set_Sig(sig)
    #必填参数：从前端获取，不可更改
    request.set_Token(token)
    #必填参数：从前端获取，不可更改
    request.set_Scene('nc_login')
    #必填参数：后端填写
    request.set_AppKey('FFFF0N00000000007F75')
    #必填参数：后端填写
    request.set_RemoteIp('192.168.73.1')

    result = clt.do_action_with_exception(request)  # 返回code 100表示验签通过，900表示验签失败
    print(result,'asdasdasdasd')
    # html = etree.HTML(result)
    # code = html.xpath('//code/text()')[0]
    code = json.loads(result)['Code']
    return HttpResponse('%s' % code)



def mainc(request):
    # try:
        cj=request.GET.get('cj')#获取前端传来的下拉框值
        searchtext=request.GET.get('searchtext')#获取前端传来的搜索词
        number = request.GET.get("number")  # 获取前端传来的页码
        if not number:  # 判断如果页面为空的话
            number = 1  # 页码的值默认为1
        if cj=='城市':
            select = TZpgg.objects.filter(hope_location__icontains=searchtext)
        elif cj=='职位':
            select = TZpgg.objects.filter(hope_position__icontains=searchtext)
        elif cj=='--请选择--':
            if searchtext in '北京':
                select = TZpgg.objects.filter(hope_location__icontains=searchtext)
            elif searchtext in '上海':
                select=TZpgg.objects.filter(hope_location__icontains=searchtext)
            elif searchtext in '广州':
                select=TZpgg.objects.filter(hope_location__icontains=searchtext)
            elif searchtext in '深圳':
                select=TZpgg.objects.filter(hope_location__icontains=searchtext)
            elif searchtext in '平面设计':
                select=TZpgg.objects.filter(hope_position__icontains=searchtext)
            elif searchtext in '软件工程师':
                select=TZpgg.objects.filter(hope_position__icontains=searchtext)
            elif searchtext in 'Java开发工程师':
                select=TZpgg.objects.filter(hope_position__icontains=searchtext)
            elif searchtext in '软件测试':
                select=TZpgg.objects.filter(hope_position__icontains=searchtext)
        elif not searchtext:
            select = TZpgg.objects.all()
        else:
            return HttpResponse('您输入的查询不到')
        pagtor = Paginator(select, per_page=30)  # 将查询到的数据进行每一页30条数据划分
        page=pagtor.page(number)
        print(cj,searchtext)
        return render(request,'baizhiapp/menu.html',{'select':select,'page':page,'number':number,})

