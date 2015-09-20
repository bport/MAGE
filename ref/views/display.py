# coding: utf-8
from django.contrib.auth.views import redirect_to_login

from django.shortcuts import render
from django.db.models.query import Prefetch
from django.db.models import Q
from django.db.models.aggregates import Count
from ref.models.classifier import AdministrationUnit

from ref.models.instances import Environment, ComponentInstance, \
    ComponentInstanceField
from ref.models.description import ImplementationFieldDescription, \
    ImplementationComputedFieldDescription


def envt(request, envt_id):
    envt = Environment.objects.\
                    select_related('typology').select_related('project').\
                    get(pk=envt_id)

    if not request.user.has_perm('read_envt', envt):
        return redirect_to_login(request.path)

    deleted = []
    if request.user.is_authenticated() and request.user.has_perm('ref.change_component_instance'):
        deleted = ComponentInstance.objects.filter(environments__id=envt_id, deleted=True).\
                    select_related('description').\
                    order_by('description__name', 'id')

    sec = (False,)
    if not envt.protected or (request.user.is_authenticated() and request.user.has_perm('read_envt_sensible', envt)):
        sec = (True, False)

    cis = ComponentInstance.objects.filter(environments__id=envt_id, deleted=False).\
                    select_related('description').\
                    select_related('instanciates__implements__application').\
                    prefetch_related(Prefetch('field_set', queryset=ComponentInstanceField.objects.filter(field__widget_row__gte=0, field__sensitive__in=sec).order_by('field__widget_row', 'field__id'))).\
                    prefetch_related(Prefetch('description__field_set', queryset=ImplementationFieldDescription.objects.filter(widget_row__gte=0, sensitive__in=sec).order_by('widget_row', 'id'))).\
                    prefetch_related(Prefetch('description__computed_field_set', queryset=ImplementationComputedFieldDescription.objects.filter(widget_row__gte=0, sensitive__in=sec).order_by('widget_row', 'id'))).\
                    order_by('description__tag', 'description__name')

    return render(request, 'ref/envt.html', {'envt': envt, 'deleted': deleted, 'cis' : cis})

def backuped(request, scope_id):
    folder = AdministrationUnit.objects.get(pk = scope_id)
    if not request.user.has_perm('read_envt', folder):
        return redirect_to_login(request.path)

    cis = ComponentInstance.objects.filter(include_in_envt_backup=True, deleted=False, environments__project__in = folder.scope()).\
            select_related('instanciates__implements__application').\
            select_related('description').\
            prefetch_related('environments')
    return render(request, 'ref/instance_backup.html', {'cis': cis, 'folder': folder})


def shared_ci(request):
    deleted = []
    if request.user.is_authenticated() and request.user.has_perm('ref.change_component_instance'):
        deleted = ComponentInstance.objects.annotate(num_envt=Count('environments')).filter(~Q(num_envt=1), deleted=True).\
                    select_related('description').\
                    order_by('description__name', 'id')

    sec = (False,)
    if request.user.is_authenticated() and request.user.has_perm('ref.allfields_componentinstance'):
        sec = (True, False)

    cis = ComponentInstance.objects.annotate(num_envt=Count('environments')).filter(~Q(num_envt=1), deleted=False).\
                    select_related('description').\
                    prefetch_related('environments').\
                    prefetch_related(Prefetch('field_set', queryset=ComponentInstanceField.objects.filter(field__widget_row__gte=0, field__sensitive__in=sec).order_by('field__widget_row', 'field__id'))).\
                    prefetch_related(Prefetch('description__field_set', queryset=ImplementationFieldDescription.objects.filter(widget_row__gte=0, sensitive__in=sec).order_by('widget_row', 'id'))).\
                    prefetch_related(Prefetch('description__computed_field_set', queryset=ImplementationComputedFieldDescription.objects.filter(widget_row__gte=0, sensitive__in=sec).order_by('widget_row', 'id'))).\
                    order_by('description__tag', 'description__name')

    return render(request, 'ref/envt_shared.html', {'deleted': deleted, 'cis' : cis})
