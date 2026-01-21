from django.apps import AppConfig

class FleetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fleet'
    verbose_name = '车队管理中心'  # 这里定义后台左上角的标题