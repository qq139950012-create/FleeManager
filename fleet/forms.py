from django import forms
from .models import *

# ==========================================
# 1) 出车/收车表单
# ==========================================
class StartWorkForm(forms.ModelForm):
    current_mileage = forms.IntegerField(
        label="出车里程",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Vehicle
        fields = ['current_mileage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 默认填入系统当前里程
        self.fields['current_mileage'].initial = self.instance.current_mileage or 0

    def clean_current_mileage(self):
        mileage = self.cleaned_data.get('current_mileage')
        current = self.instance.current_mileage or 0
        if mileage is not None and mileage < current:
            raise forms.ValidationError(f"出车里程不能小于系统里程（当前：{current} km）")
        return mileage


class EndWorkForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['current_mileage']
        widgets = {
            'current_mileage': forms.NumberInput(attrs={'class': 'form-control'})
        }


# ==========================================
# 2) 运营表单 (加油/充电)
# ==========================================
class OperationForm(forms.ModelForm):
    FUEL_LOCATIONS = [('station', '加油站'), ('site', '现场加油')]
    location_type = forms.ChoiceField(
        choices=FUEL_LOCATIONS,
        required=False,
        label="加油地点",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    cost = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '金额 (选填)'})
    )
    receipt = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = OperationRecord
        fields = '__all__'
        exclude = ['vehicle', 'driver', 'record_type', 'create_at']
        widgets = {
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '当前里程'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '加油量/度数'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '备注'}),
        }


# ==========================================
# 3) 故障报修表单
# ==========================================
class RepairForm(forms.ModelForm):
    FAULT_CHOICES = [
        ('tire', '轮胎故障'), ('engine', '发动机/异响'),
        ('battery', '电路/电瓶'), ('body', '车身外观'),
        ('light', '灯光系统'), ('other', '其他问题')
    ]
    fault_category = forms.ChoiceField(
        choices=FAULT_CHOICES,
        label="故障类型",
        widget=forms.Select(attrs={'class': 'form-select text-center'})
    )

    content = forms.CharField(
        required=False,
        label="详细描述",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '详细描述 (选填，可不填)...'})
    )

    class Meta:
        model = MaintenanceRecord
        fields = '__all__'
        exclude = [
            'vehicle', 'driver', 'status', 'repairman',
            'finish_at', 'create_at',
            'fault_type',
        ]
        widgets = {
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ==========================================
# 4) 通用表单
# ==========================================
class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))


# ==========================================
# 5) 任务表单
# ==========================================
from django import forms
from .models import WorkTask, Employee

class TaskCreateForm(forms.ModelForm):
    target_team = forms.ChoiceField(
        label="下发班组",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = WorkTask
        fields = ['title', 'detail', 'deadline', 'target_team']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例如：去A区拉料'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '任务说明…'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        teams = (
            Employee.objects.exclude(team__isnull=True)
            .exclude(team__exact='')
            .values_list('team', flat=True)
            .distinct()
            .order_by('team')
        )
        self.fields['target_team'].choices = [('', '请选择班组')] + [(t, t) for t in teams]

    def clean_target_team(self):
        team = self.cleaned_data.get('target_team')
        if not team:
            raise forms.ValidationError("请选择班组")
        return team



# ==========================================
# 6) 管理员表单（保留你现有逻辑）
# ==========================================
class AdminVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'plate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_id': forms.TextInput(attrs={'class': 'form-control'})
        }


class AdminEmployeeForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'team': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'})
        }


class AdminBonusCreateForm(forms.ModelForm):
    class Meta:
        model = BonusBatch
        fields = '__all__'
        exclude = ['leader', 'status', 'created_at', 'distributed_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'month': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'})
        }
