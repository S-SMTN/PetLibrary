from django.contrib.admin import AdminSite


class TenantAdminSite(AdminSite):
    site_header = "Tenant Administration"
    site_title = "Tenant Admin"
    index_title = "Welcome to the Tenant Admin"


tenant_admin_site = TenantAdminSite(name='tenant_admin')


