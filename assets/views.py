from django.shortcuts import render, HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from assets import models
from assets import asset_handler
from django.shortcuts import get_object_or_404

'''
403就是拒绝服务的错误了。

原因在于我们模拟浏览器发送了一个POST请求给Django，但是请求中没有携带Django需要的csrf安全令牌，所以拒绝了请求。

为了解决这个问题，我们需要在这个report视图上忽略csrf验证，可以通过Django的@csrf_exempt装饰器
'''


@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse('没有数据')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须是字典格式')
        sn = data.get('sn', None)
        print('sn=,', sn)
        if sn:
            # 进入审批流程
            asset_obj = models.Asset.objects.filter(sn=sn)

            if asset_obj:
                # 进入已上线资产的数据更新流程
                print('asset_obj[0]=', asset_obj[0])
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                print('update_asset = ', update_asset )
                return HttpResponse("资产数据已经更新！")
            else:  # 如果已上线资产中没有，那么说明是未批准资产，进入新资产待审批区，更新或者创建资产。
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse('资产没有sn序列号，请检查数据')
    return HttpResponse('请使用post方法')


def index(request):

    assets = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())


def dashboard(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()
    up_rate = round(upline/total*100)
    o_rate = round(offline/total*100)
    un_rate = round(unknown/total*100)
    bd_rate = round(breakdown/total*100)
    bu_rate = round(backup/total*100)
    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()

    return render(request, 'assets/dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'assets/detail.html', locals())