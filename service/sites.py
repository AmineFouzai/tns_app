from django.contrib import admin
from unfold.sites import UnfoldAdminSite


class AppAdminSite(UnfoldAdminSite,admin.AdminSite):
    site_url="https://localhost:8000/admin"


app_admin_site = AppAdminSite(name="admin_site")