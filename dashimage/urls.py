from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.main_index, name='index'),
    path(r'', views.home, name='dashimage_home'),
    # path(r'', views.index, name='index'),
    path(r'dash_image', views.home, name='dashimage_home'),
    path(r'convert_dicom', views.dashimage, name='convert_dicom'),
    path(r'view_dashimage', views.view_dashimage, name='view_dashimage'),
    path(r'upload_file', views.upload_file, name='upload_file'),
    path(r'upload_batch_files', views.upload_batch_files, name='upload_batch_files'),
    path(r'download_model', views.download_model, name='download_model'),
    path(r'make_predictions', views.make_predictions, name='make_predictions'),
    path(r'train_model', views.train_model, name='train_model'),
    path(r'download/<patient_id>', views.download_file, name='download_file'),
    path(r'model_training_status', views.get_model_training_status, name='model_training_status'),

    path(r'query', views.query, name='query')
]
