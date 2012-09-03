from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'imageex.views.home'),
    
    (r'^upload$', 'imageex.upload.views.upload_file'),
    (r'^upload-raw$', 'imageex.upload.views.upload_file_raw'),
    
    (r'^segmentation/kmeans', 'imageex.segmentation.views.labelize_kmeans'),
    (r'^segmentation/grabcut', 'imageex.segmentation.views.labelize_grabcut'),
    (r'^segmentation/watershed', 'imageex.segmentation.views.labelize_watershed'),
    (r'^segmentation/reset', 'imageex.segmentation.views.reset'),
    
    (r'^featureextraction/extractsamplesnotextracted', 'imageex.featureextraction.views.extractSamplesNotExtracted'),
    
    (r'^learning/learn/(?P<classifier>.*)', 'imageex.learning.views.learn'),

    (r'^learning/learnall/(?P<classifier>.*)', 'imageex.learning.views.learnAllSamples'),
    (r'^learning/createclassifiers', 'imageex.learning.views.createClassifiers'),
    
    (r'^learning/predict/(?P<classifier>.*)', 'imageex.learning.views.predictClassHTMLimageinlined'),
    (r'^learning/predict_json/(?P<classifier>.*)', 'imageex.learning.views.predictClassJSON'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
