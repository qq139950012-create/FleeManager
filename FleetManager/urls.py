from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from fleet import views

urlpatterns = [
    # === 基础与认证 ===
    path('', views.home, name='home'),
    path('dashboard/', views.home, name='driver_dashboard'),
    path('accounts/logout/', views.sign_out, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    # === 核心业务：扫码与绑定 ===
    path('driver/scan/', views.driver_scan_vehicle, name='driver_scan_vehicle'),
    path('scan/<int:vehicle_id>/start/', views.vehicle_start, name='vehicle_start'),
    path('scan/<int:vehicle_id>/end/', views.vehicle_end, name='vehicle_end'),
    path('qrcode/<int:vehicle_id>/', views.generate_qrcode, name='generate_qrcode'),

    # === 司机运营 ===
    path('work/toggle/', views.toggle_work_status, name='toggle_work_status'),
    path('vehicle/<int:vehicle_id>/add/<str:type>/', views.add_record, name='vehicle_add'),
    path('vehicle/<int:vehicle_id>/repair/', views.add_repair, name='add_repair'),
    path('scan/<int:vehicle_id>/', views.vehicle_dashboard, name='vehicle_dashboard'),

    # === 管理员后台 ===
    path('super_admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # 车辆与人员
    path('super_admin/vehicle/add/', views.admin_vehicle_manage, name='admin_vehicle_add'),
    path('super_admin/vehicle/<int:v_id>/', views.admin_vehicle_manage, name='admin_vehicle_edit'),
    path('super_admin/employee/add/', views.admin_employee_manage, name='admin_employee_add'),
    path('super_admin/employee/<int:emp_id>/', views.admin_employee_manage, name='admin_employee_edit'),
    
    # 奖金管理
    path('super_admin/bonus/', views.admin_bonus_list, name='admin_bonus_list'),
    path('super_admin/bonus/create/', views.admin_bonus_create, name='admin_bonus_create'),
    # 关键修复：补全了奖金导出路由
    path('super_admin/export/bonus/', views.admin_bonus_export, name='admin_bonus_export'), 
    path('super_admin/bonus/report/<int:batch_id>/', views.admin_bonus_report, name='admin_bonus_report'),

    # 导入导出
    path('super_admin/import/employee/', views.admin_employee_import, name='admin_employee_import'),
    path('super_admin/import/vehicle/', views.admin_vehicle_import, name='admin_vehicle_import'),
    path('super_admin/import/inventory/', views.admin_inventory_import, name='admin_inventory_import'),
    
    path('super_admin/export/employee/', views.admin_employee_export, name='admin_employee_export'),
    path('super_admin/export/vehicle/', views.admin_vehicle_export, name='admin_vehicle_export'),
    path('super_admin/export/inventory/', views.admin_inventory_export, name='admin_inventory_export'),
    
    # 下载模板
    path('super_admin/template/employee/', views.admin_download_employee_template, name='admin_download_employee_template'),
    path('super_admin/template/vehicle/', views.admin_download_template, name='admin_download_template'),
    path('super_admin/template/inventory/', views.admin_download_inventory_template, name='admin_download_inventory_template'),

    # === 班长/调度/维修 ===
    path('leader/dashboard/', views.leader_dashboard, name='leader_dashboard'),
    path('leader/team/', views.team_dashboard, name='team_dashboard'),
    # 班长分钱页面
    path('leader/bonus/<int:batch_id>/', views.leader_bonus_distribute, name='leader_bonus_distribute'),

    path('tv/dashboard/', views.tv_dashboard, name='tv_dashboard'),
    path('dispatch/', views.dispatch_dashboard, name='dispatch_dashboard'),
    path('repair/dashboard/', views.repair_dashboard, name='repair_dashboard'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    
    # 任务操作
    path('task/complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('leader/task/assign/<int:task_id>/', views.assign_task_to_driver, name='assign_task_to_driver'),
    path('leader/task/complete/<int:task_id>/', views.leader_complete_task, name='leader_complete_task'),
    path('leader/task/reset/<int:task_id>/', views.leader_reset_task, name='leader_reset_task'),
    path('leader/force_end/<int:vehicle_id>/', views.leader_force_end, name='leader_force_end'),


    path('dispatch/', views.dispatch_dashboard, name='dispatch_dashboard'),
    path('leader/task/<int:task_id>/assign/', views.leader_assign_task, name='leader_assign_task'),
    path('leader/task/<int:task_id>/finish/', views.leader_finish_task, name='leader_finish_task'),


    # 维修操作
    path('repair/start/<int:repair_id>/', views.repair_start, name='repair_start'),
    path('repair/detail/<int:repair_id>/', views.repair_detail, name='repair_detail'),
    path('repair/add_part/<int:repair_id>/', views.repair_add_part, name='repair_add_part'),
    path('repair/complete/<int:repair_id>/', views.repair_complete, name='repair_complete'),
    
    # 库存操作
    path('inventory/add/', views.inventory_add, name='inventory_add'),
    path('inventory/action/<int:item_id>/', views.inventory_action, name='inventory_action'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)