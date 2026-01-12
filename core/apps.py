from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Customize Django admin site after apps are loaded
        from django.contrib import admin
        admin.site.site_header = "PayCoreX Administration"
        admin.site.site_title = "PayCoreX Admin"
        admin.site.index_title = "Welcome to PayCoreX Administration"

