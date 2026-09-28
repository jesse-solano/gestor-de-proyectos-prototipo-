from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Project, Deliverable, MonthlyTrend


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'poo', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'poo')
    fieldsets = UserAdmin.fieldsets + (
        ('Información Corporativa ProjectFlow', {
            'fields': ('role', 'poo', 'personal_email', 'phone', 'avatar_color', 'failed_login_attempts')
        }),
    )


class DeliverableInline(admin.TabularInline):
    model = Deliverable
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'phase', 'status', 'estatus', 'real_percentage', 'planned_percentage', 'deviation', 'procura', 'assigned_user')
    list_filter = ('phase', 'status', 'estatus', 'procura')
    search_fields = ('code', 'name', 'description', 'objective')
    inlines = [DeliverableInline]


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'phase', 'assigned_to', 'due_date', 'progress', 'is_completed')
    list_filter = ('phase', 'is_completed')
    search_fields = ('title', 'project__name')


@admin.register(MonthlyTrend)
class MonthlyTrendAdmin(admin.ModelAdmin):
    list_display = ('month_name', 'year', 'in_progress', 'paused', 'closing', 'completed', 'cancelled', 'total')
    list_filter = ('year',)