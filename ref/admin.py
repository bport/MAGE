# coding: utf-8

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from ref.models import Project, Environment, LogicalComponent, Application, SLA, ComponentInstance, \
    ComponentImplementationClass, NamingConvention, NamingConventionField
from ref.naming import nc_sync_naming_convention



################################################################################
## No-frills admins
################################################################################

admin.site.register(Project)
admin.site.register(Application)
admin.site.register(LogicalComponent)
admin.site.register(SLA)

class EnvironmentAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'destructionDate', ]
    list_display = ('name', 'description',)
    ordering = ('name',)

admin.site.register(Environment, EnvironmentAdmin)



################################################################################
## Naming conventions
################################################################################
    
class NamingConventionFieldInline(admin.TabularInline):
    model = NamingConventionField
    extra = 0
    can_delete = False
    fields = ['model', 'field', 'pattern', ]
    readonly_fields = ['model', 'field', ]
    ordering = ['model', 'field']
    template = 'MAGE/admin/tabular_no_title.html'

class NamingConventionAdmin(admin.ModelAdmin):
    fields = ['name', 'applications']
    inlines = [NamingConventionFieldInline, ]
    actions = ['make_refresh_nc',]
    
    def make_refresh_nc(self, request, queryset):
        for nc in queryset:
            nc_sync_naming_convention(nc)
            self.message_user(request, "%s successfully refreshed." % nc.name)
    make_refresh_nc.short_description = u'actualiser les champs des modèles'

admin.site.register(NamingConvention, NamingConventionAdmin)



################################################################################
## Component instances
################################################################################

class CICFilter(SimpleListFilter):
    title = u'implémentation de'
    parameter_name = 'impl'

    def lookups(self, request, model_admin):
        model_name = request.path.split('/')[3]
        cics = ComponentImplementationClass.objects.filter(python_model_to_use__model__iexact=model_name)
        res = ()
        for cic in cics:
            res += ((cic.id, cic.__unicode__()),)
        return res

    def queryset(self, request, queryset):
        print self.value()
        if self.value():
            return queryset.filter(instanciates_id=self.value())
        else:
            return queryset

class ComponentInstanceAdmin(admin.ModelAdmin):
    """
        Base admin class for components. It filters 'dependsOn' fields so that the admin will 
        only display relevant components and not every single last one of them, and it provides
        default display behaviour.
        
        @note: This class is NOT meant to be directly used with the Component model, but only with
        models inheriting from Component
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        ## Find the model that this class admins
        model = [ k for k, v in admin.site._registry.iteritems() if v == self][0]

        ## Superseed the fields as defined in the class
        if db_field.name == 'dependsOn' and hasattr(model, 'parents'):
            kwargs['queryset'] = ComponentInstance.objects.filter(model__model__in=[u.lower() for u in model.parents.itervalues()])
        elif db_field.name == 'dependsOn' and not hasattr(model, 'parents'):
            kwargs['queryset'] = ComponentInstance.objects.none()
            
        if db_field.name == 'instanciates':
            kwargs['queryset'] = ComponentImplementationClass.objects.filter(python_model_to_use__model__iexact=model.__name__)
        return super(ComponentInstanceAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
    ## Default values for the various admin options. Should usually be at least partially overloaded
    fieldsets_generic = [ ('Informations génériques', {'fields': ['name', 'instanciates', 'environments', 'connectedTo']}), ]
    fieldsets_generic_no_class = [ ('Informations génériques', {'fields': ['environments', 'connectedTo']}), ]
    fieldsets = fieldsets_generic
    filter_horizontal = ('connectedTo', 'dependsOn', 'environments')
    ordering = ('name',)
    search_fields = ('name', 'dependsOn__name',)
    list_filter = ['environments__name', CICFilter, ]
    list_display = ('name', 'instanciates')
