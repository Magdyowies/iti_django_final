from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        project_name_query = self.request.GET.get('project_name')
        if project_name_query:
            queryset = queryset.filter(title__icontains=project_name_query)
        return queryset


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project-list')

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner


class UserProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/user_project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def handle_no_permission(self):
        messages.warning(self.request, "You need to log in to view your projects.")
        return super().handle_no_permission()