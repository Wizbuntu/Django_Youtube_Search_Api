from django.contrib import admin
from .models import Youtube_Search_Api
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter


# Register your models here.
@admin.register(Youtube_Search_Api)
class Youtube_Search_Api_Admin(admin.ModelAdmin):
    list_display = ['search_id', 'title', 'duration', 'view_count', 'date']
    list_filter = (('duration', RangeNumericFilter),)
    search_fields = ('search_id', 'title', 'date', 'view_count',)

