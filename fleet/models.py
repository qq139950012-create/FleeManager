from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ==========================================
# 1. 人员与角色
# ==========================================
class Employee(models.Model):
    ROLE_CHOICES = [
        ('driver', '司机'),
        ('repairman', '点检长'),
        ('team_leader', '班长'),
        ('dispatcher', '调度'),
        ('admin', '管理员'),
    ]

    WORK_STATUS_CHOICES = [
        ('on_duty', '在岗'),
        ('off_duty', '休息'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name='系统用户'
    )
    name = models.CharField(max_length=50, verbose_name='姓名')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='driver', verbose_name='角色')
    team = models.CharField(max_length=50, blank=True, null=True, verbose_name='班组')
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name='岗位')
    work_status = models.CharField(
        max_length=20,
        default='off_duty',
        choices=WORK_STATUS_CHOICES,
        verbose_name='出勤状态'
    )

    class Meta:
        verbose_name = "员工"
        verbose_name_plural = "员工"

    def __str__(self):
        role_label = dict(self.ROLE_CHOICES).get(self.role, self.role)
        return f"{self.name}（{role_label}）"


# ==========================================
# 2. 车辆与运营
# ==========================================
class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('idle', '空闲'),
        ('working', '作业中'),
        ('repairing', '维修中'),
    ]

    vehicle_id = models.CharField(max_length=50, unique=True, verbose_name='车辆编号')
    plate_number = models.CharField(max_length=20, verbose_name='车牌号')
    brand_model = models.CharField(max_length=50, verbose_name='品牌型号')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idle', verbose_name='状态')
    current_driver = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='driving_vehicle',
        verbose_name='当前司机'
    )
    current_mileage = models.IntegerField(default=0, verbose_name='当前里程')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "车辆"
        verbose_name_plural = "车辆"

    def __str__(self):
        return f"{self.plate_number}（{self.brand_model}）"


class OperationRecord(models.Model):
    TYPE_CHOICES = [
        ('fuel', '加油'),
        ('charge', '充电'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name='车辆')
    driver = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='司机')
    record_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='类型')
    mileage = models.IntegerField(verbose_name='里程')
    volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='数量')
    remark = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')

    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='费用')
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True, verbose_name='凭证图片')

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "运营记录"
        verbose_name_plural = "运营记录"

    def __str__(self):
        type_label = dict(self.TYPE_CHOICES).get(self.record_type, self.record_type)
        return f"{self.vehicle.plate_number} - {type_label} - {self.volume}"


# ==========================================
# 3. 库存管理
# ==========================================
class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ('spare', '备品'),
        ('material', '辅材'),
    ]

    name = models.CharField(max_length=100, verbose_name="配件名称")
    spec = models.CharField(max_length=100, blank=True, null=True, verbose_name="规格型号")
    unit = models.CharField(max_length=20, verbose_name="单位")
    stock = models.IntegerField(default=0, verbose_name="库存")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='spare', verbose_name="分类")

    class Meta:
        verbose_name = "库存物品"
        verbose_name_plural = "库存物品"

    def __str__(self):
        category_label = dict(self.CATEGORY_CHOICES).get(self.category, self.category)
        return f"{self.name}（{category_label}）"


class StockLog(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, verbose_name='物品')
    change_amount = models.IntegerField(verbose_name='变动数量')
    operator = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='操作人')
    note = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "库存变动日志"
        verbose_name_plural = "库存变动日志"

    def __str__(self):
        return f"{self.item.name} 变动 {self.change_amount}（{self.operator.name}）"


# ==========================================
# 4. 维修管理
# ==========================================
class MaintenanceRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', '待维修'),
        ('repairing', '维修中'),
        ('completed', '已完成'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name='车辆')
    driver = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reported_repairs', verbose_name='报修人')
    fault_type = models.CharField(max_length=50, verbose_name='故障类型')
    content = models.TextField(blank=True, null=True, verbose_name='故障描述')
    images = models.ImageField(upload_to='repairs/', null=True, blank=True, verbose_name='图片')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    repairman = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_repairs',
        verbose_name='维修人员'
    )
    finish_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "维修记录"
        verbose_name_plural = "维修记录"

    def __str__(self):
        status_label = dict(self.STATUS_CHOICES).get(self.status, self.status)
        return f"{self.vehicle.plate_number} - {self.fault_type}（{status_label}）"


class PartUsage(models.Model):
    maintenance = models.ForeignKey(MaintenanceRecord, on_delete=models.CASCADE, verbose_name='维修单')
    part = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, verbose_name='配件')
    quantity = models.IntegerField(default=1, verbose_name='数量')

    class Meta:
        verbose_name = "配件使用记录"
        verbose_name_plural = "配件使用记录"

    def __str__(self):
        return f"{self.maintenance.vehicle.plate_number} - {self.part.name} x {self.quantity}"


# ==========================================
# 5. 任务与奖金
# ==========================================
class WorkTask(models.Model):
    TASK_STATUS_CHOICES = [
        ('pending', '待处理'),
        ('doing', '处理中'),
        ('done', '已完成'),
    ]


    target_team = models.CharField("目标班组", max_length=50, blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name='标题')
    detail = models.TextField(verbose_name='内容')
    deadline = models.DateTimeField(verbose_name='截止时间')
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='created_tasks', verbose_name='创建人')
    assigned_drivers = models.ManyToManyField(Employee, related_name='tasks', verbose_name='指派对象')
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='pending', verbose_name='状态')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = "工作任务"
        verbose_name_plural = "工作任务"

    def __str__(self):
        return self.title


class BonusBatch(models.Model):
    STATUS_CHOICES = [
        ('pending', '待发放'),
        ('completed', '已完成'),
    ]

    title = models.CharField(max_length=100, verbose_name='标题')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    month = models.CharField(max_length=20, verbose_name='月份')
    note = models.TextField(blank=True, null=True, verbose_name='备注')
    leader = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='负责人')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    distributed_at = models.DateTimeField(null=True, blank=True, verbose_name='发放时间')

    class Meta:
        verbose_name = "奖金批次"
        verbose_name_plural = "奖金批次"

    def __str__(self):
        return f"{self.title}（{self.month}）"


class BonusDetail(models.Model):
    batch = models.ForeignKey(BonusBatch, on_delete=models.CASCADE, verbose_name='批次')
    receiver = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='领取人')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')

    class Meta:
        verbose_name = "奖金明细"
        verbose_name_plural = "奖金明细"

    def __str__(self):
        return f"{self.receiver.name} - {self.amount}"
