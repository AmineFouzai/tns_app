from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db import models
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token, TokenProxy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

from django.contrib import admin
from unfold.admin import ModelAdmin

from service.models import Recipient, Template, Campaign
from service.models.merchant import Merchant


from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(TokenProxy)


@admin.register(Recipient)
class RecipientAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    pass


@admin.register(Template)
class TemplateAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }


@admin.register(Campaign)
class CampaignAdmin(ModelAdmin):
    list_display = ("name", "channel", "status", "scheduled_time", "created_at")
    actions = ["send_now", "cancel_schedule"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == "scheduled" and obj.scheduled_time:
            obj.schedule_task()

    @admin.action(description="Send Now")
    def send_now(self, _, queryset):
        for campaign in queryset:
            campaign.trigger_immediate()

    @admin.action(description="Cancel Scheduled Task")
    def cancel_schedule(self, _, queryset):
        for campaign in queryset:
            campaign.cancel_scheduled_task()
            campaign.status = "cancelled"
            campaign.save()


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(Token)
class TokenProxyAdmin(TokenAdmin, ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Merchant)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
