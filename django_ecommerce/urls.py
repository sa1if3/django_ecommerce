"""django_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
admin.site.site_header = 'Django Market Administration'                    # default: "Django Administration"
admin.site.index_title = 'Main Admin Page'                 # default: "Site administration"
admin.site.site_title = 'Django Market Site Admin' # default: "Django site admin"

urlpatterns = [
    path('accounts/', admin.site.urls),
    path('', include('themeonly.urls')),
    path('', include('genesis.urls')),
    path('', include('shoppingcart.urls')),
    path('', include('userchats.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
