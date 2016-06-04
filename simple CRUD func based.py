

# startapp servers

# settings
INSTALLED_APPS = (
  
  'servers',
  
)

# model
from django.db import models
from django.core.urlresolvers import reverse

class Server(models.Model):
    name = models.CharField(max_length=200)
    ip = models.GenericIPAddressField()
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('server_edit', kwargs={'pk': self.pk})

# admin
from django.contrib import admin
from servers.models import Server

admin.site.register(Server)

# views CRUD func-based
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from servers.models import Server

class ServerForm(ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'ip', 'order']

def server_list(request, template_name='servers/server_list.html'):
    servers = Server.objects.all()
    data = {}
    data['object_list'] = servers
    return render(request, template_name, data)

def server_create(request, template_name='servers/server_form.html'):
    form = ServerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('server_list')
    return render(request, template_name, {'form':form})

def server_update(request, pk, template_name='servers/server_form.html'):
    server = get_object_or_404(Server, pk=pk)
    form = ServerForm(request.POST or None, instance=server)
    if form.is_valid():
        form.save()
        return redirect('server_list')
    return render(request, template_name, {'form':form})

def server_delete(request, pk, template_name='servers/server_confirm_delete.html'):
    server = get_object_or_404(Server, pk=pk)    
    if request.method=='POST':
        server.delete()
        return redirect('server_list')
    return render(request, template_name, {'object':server})


# servers.urls.py 
from django.conf.urls import patterns, url

from servers import views

urlpatterns = patterns('',
  url(r'^$', views.server_list, name='server_list'),
  url(r'^new$', views.server_create, name='server_new'),
  url(r'^edit/(?P<pk>\d+)$', views.server_update, name='server_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.server_delete, name='server_delete'),
)

# project/urls.py
urlpatterns = patterns('',
  
  url(r'^servers/', include('servers.urls')),
  
)

# Templates
#templates/servers/server_form.html
<form method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit" />
</form>

# templates/servers/server_list.html 
<h1>Servers</h1>
<ul>
    {% for server in object_list %}
    <li>{{ server.name }}  :  
    <a href="{% url "server_edit" server.id %}">{{ server.ip }}</a>
    <a href="{% url "server_delete" server.id %}">delete</a>
    </li>
    {% endfor %}
</ul>

<a href="{% url "server_new" %}">New</a>

# templates/servers/server_confirm_delete.html
<form method="post">{% csrf_token %}
    Are you sure you want to delete "{{ object }}" ?
    <input type="submit" value="Submit" />
</form>