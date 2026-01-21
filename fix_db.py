import os
import django
from django.db import connection

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FleetManager.settings')
django.setup()

def reset_tables():
    with connection.cursor() as cursor:
        # 强制禁用外键检查，防止删除报错
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # 定义需要重置的表名
        tables = [
            'fleet_maintenancerecord', # 维修记录
            'fleet_operationrecord',   # 运营记录
            'fleet_vehicle',           # 车辆表
            'fleet_employee',          # 员工表
            'django_migrations'        # 迁移历史表（关键！）
        ]
        
        print("正在清理旧的数据库表...")
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table};")
                print(f"✅ 已删除表: {table}")
            except Exception as e:
                print(f"❌ 删除表 {table} 失败: {e}")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("\n数据库清理完成！现在可以重新生成迁移了。")

if __name__ == '__main__':
    reset_tables()