from django.contrib import admin

from Public.models import Library, LibraryTenant, Domain


@admin.register(LibraryTenant)
class LibraryTenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name')
    search_fields = ('name', 'schema_name')
    ordering = ('name',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    search_fields = ('domain', 'tenant__name')
    ordering = ('domain',)


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'address')
    search_fields = ('name', 'subdomain')
    ordering = ('name',)
