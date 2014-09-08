# -*- coding: utf-8 -*-

from app1.forms import ModelAForm
from app1.models import ModelA
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
import reversion


class ModelADetailView(DetailView):
    model = ModelA
    template_name = 'app1/ma_detail.html'


class ModelACreateView(CreateView):
    form_class = ModelAForm
    success_url = reverse_lazy('app1:ma_list')
    template_name = 'app1/ma_form.html'

    def form_valid(self, form):
        form.instance.updated_by_user = self.request.user
        return super(ModelACreateView, self).form_valid(form)


class ModelAUpdateView(UpdateView):
    model = ModelA
    form_class = ModelAForm
    success_url = reverse_lazy('app1:ma_list')
    template_name = 'app1/ma_form.html'

    def form_valid(self, form):
        form.instance.updated_by_user = self.request.user
        return super(ModelAUpdateView, self).form_valid(form)


class ModelADeleteView(DeleteView):
    model = ModelA
    success_url = reverse_lazy('app1:ma_list')
    template_name = 'app1/ma_delete.html'


class ModelAListView(ListView):
    model = ModelA
    template_name = 'app1/ma_list.html'


def get_history_ModelA(request, pk):
    template = 'app1/ma_history.html'
    ma = get_object_or_404(ModelA, pk=pk)
    version_list = reversion.get_for_object(ma)
    context = { 'obj_pk': pk, 'version_list': version_list }
    return render_to_response(template, RequestContext(request, context))


def revert_modela_to_revision(request, pk, rev_pk):
    ma = get_object_or_404(ModelA, pk=pk)
    version = reversion.get_for_object(ma).get(id=rev_pk)

    with transaction.atomic(), reversion.create_revision():
        reversion.set_comment("reverted ModelA")
        reversion.set_user(request.user)
        version.revision.revert()

    return HttpResponseRedirect(reverse_lazy('app1:ma_detail', args=(ma.pk,)))


ma_list = ModelAListView.as_view()
ma_detail = ModelADetailView.as_view()
ma_delete = ModelADeleteView.as_view()
ma_update = ModelAUpdateView.as_view()
ma_create = ModelACreateView.as_view()
