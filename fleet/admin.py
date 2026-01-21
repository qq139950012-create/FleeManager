from django.contrib import admin
from .models import (
    Employee, Vehicle, OperationRecord, InventoryItem, 
    StockLog, MaintenanceRecord, PartUsage, WorkTask, 
    BonusBatch, BonusDetail
)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # 只显示存在的字段
    list_display = ['name', 'role', 'phone', 'team', 'work_status']
    list_filter = ['role', 'work_status', 'team']
    search_fields = ['name', 'phone']

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'vehicle_id', 'status', 'current_driver', 'current_mileage']
    list_filter = ['status']
    search_fields = ['plate_number', 'vehicle_id']

@admin.register(OperationRecord)
class OperationRecordAdmin(admin.ModelAdmin):
    # 移除了 amount，改用 volume (根据当前模型)
    list_display = ['vehicle', 'driver', 'record_type', 'volume', 'mileage', 'create_at']
    list_filter = ['record_type', 'create_at']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    # 移除了 unit_price
    list_display = ['name', 'category', 'spec', 'stock', 'unit']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(StockLog)
class StockLogAdmin(admin.ModelAdmin):
    # 修正：根据当前模型，字段是 item 和 change_amount
    list_display = ['item', 'change_amount', 'operator', 'create_at']
    list_filter = ['create_at']

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    # 移除了 cost 和 is_routine_maintenance
    list_display = ['vehicle', 'driver', 'fault_type', 'status', 'repairman', 'create_at']
    list_filter = ['status', 'create_at']

@admin.register(PartUsage)
class PartUsageAdmin(admin.ModelAdmin):
    list_display = ['maintenance', 'part', 'quantity']

@admin.register(WorkTask)
class WorkTaskAdmin(admin.ModelAdmin):
    # 移除了 target_team
    list_display = ['title', 'created_by', 'status', 'deadline', 'create_at']
    list_filter = ['status']

@admin.register(BonusBatch)
class BonusBatchAdmin(admin.ModelAdmin):
    # 移除了 team_name
    list_display = ['title', 'total_amount', 'month', 'leader', 'status']
    list_filter = ['status', 'month']

@admin.register(BonusDetail)
class BonusDetailAdmin(admin.ModelAdmin):
    list_display = ['batch', 'receiver', 'amount']