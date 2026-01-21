import os
import django
from django.db import connection

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FleetManager.settings')
django.setup()

def clean_database():
    with connection.cursor() as cursor:
        # 1. 禁用外键检查（防止因依赖关系删不掉）
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # 2. 获取当前数据库里的所有表名
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        print(f"🔍 扫描到 {len(tables)} 张残留表，准备全部清除...")
        
        # 3. 循环删除每一张表
        for table in tables:
            table_name = table[0]
            try:
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
                print(f"🗑️ 已删除: {table_name}")
            except Exception as e:
                print(f"❌ 删除失败 {table_name}: {e}")
        
        # 4. 恢复外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("\n✨ 数据库已彻底清空！现在可以重新执行 migrate 了。")

if __name__ == '__main__':
    clean_database()