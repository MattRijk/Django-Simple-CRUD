

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

# views CRUD
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from servers.models import Server

class ServerList(ListView):
    model = Server

class ServerCreate(CreateView):
    model = Server
    success_url = reverse_lazy('server_list')
    fields = ['name', 'ip', 'order']

class ServerUpdate(UpdateView):
    model = Server
    success_url = reverse_lazy('server_list')
    fields = ['name', 'ip', 'order']

class ServerDelete(DeleteView):
    model = Server
    success_url = reverse_lazy('server_list')


# servers.urls.py 
from django.conf.urls import patterns, url

from servers import views

urlpatterns = patterns('',
  url(r'^$', views.ServerList.as_view(), name='server_list'),
  url(r'^new$', views.ServerCreate.as_view(), name='server_new'),
  url(r'^edit/(?P<pk>\d+)$', views.ServerUpdate.as_view(), name='server_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.ServerDelete.as_view(), name='server_delete'),
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