import requests

def checkip(ip):

    URL = 'http://ip.taobao.com/service/getIpInfo.php'

    try:

        r = requests.get(URL, params=ip, timeout=3)

    except requests.RequestException as e:

        print(e)

    else:

        json_data = r.json()

        if json_data[u'code'] == 0:

            country= json_data[u'data'][u'country']

            # print '所在地区： ' + json_data[u'data'][u'area'].encode('utf-8')

            province=json_data[u'data'][u'region']

            city= json_data[u'data'][u'city']
            operator=json_data[u'data'][u'isp']
            return country,province,city,operator

        else:

            return '查询失败,请稍后再试！'

# ip={'ip': '127.0.0.1'}
#
# print(checkip(ip))