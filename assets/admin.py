from django.contrib import admin

# Register your models here.
from assets import models
from assets import asset_handler
'''
通过actions = ['approve_selected_new_assets']定义当前模型的新acitons列表；
approve_selected_new_assets()方法包含具体的动作逻辑；
自定义的action接收至少三个参数，第一个是self，第二个是request即请求，第三个是被选中的数据对象集合queryset。
首先通过request.POST.getlist()方法获取被打钩的checkbox对应的资产；
可能同时有多个资产被选择，所以这是个批量操作，需要进行循环；
selected是一个包含了被选中资产的id值的列表；
对于每一个资产，创建一个asset_handler.ApproveAsset()的实例，然后调用实例的asset_upline()方法，并获取返回值。如果返回值为True，说明该资产被成功批准，那么success_upline_number变量+1，保存成功批准的资产数；
最后，在admin中给与提示信息。
approve_selected_new_assets.short_description = "批准选择的新资产"用于在admin界面中为action提供中文显示。你可以尝试去掉这条，看看效果。
'''


class NewAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
    list_filter = ['asset_type', 'manufacturer', 'c_time']
    search_fields = ('sn',)

    actions = ['approve_selected_new_assets']  # 编写自己的执行动作

    def approve_selected_new_assets(self, request, queryset):
        # 获取被打钩的checkbox对应的资产
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        success_upline_number = 0
        for asset_id in selected:
            obj = asset_handler.ApproveAsset(request, asset_id)
            ret = obj.asset_upline()
            if ret:
                success_upline_number += 1
        # 顶部绿色提示信息
        self.message_user(request, '成功批准 %s 条资产上线' % success_upline_number)
    approve_selected_new_assets.short_description = '批准选择的薪资产'


class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']


admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.NewAssetApprovalZone, NewAssetAdmin)

admin.site.register(models.Server)
admin.site.register(models.StorageDevice)
admin.site.register(models.SecurityDevice)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Contract)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.EventLog)
admin.site.register(models.IDC)
admin.site.register(models.Manufacturer)
admin.site.register(models.NetworkDevice)
admin.site.register(models.NIC)
admin.site.register(models.RAM)
admin.site.register(models.Software)
admin.site.register(models.Tag)

