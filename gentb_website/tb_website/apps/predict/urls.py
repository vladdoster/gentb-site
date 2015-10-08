from django.conf.urls import patterns, include, url


urlpatterns = patterns('apps.predict.views',

    url(r'^upload-data/$', 'view_predict_page', name="view_predict_page"),

    url(r'^upload-success/(?P<dataset_md5>\w{32})/$', 'view_predict_upload_success', name="view_predict_upload_success"),

    url(r'^my-datasets/$', 'view_my_datasets', name="view_my_datasets"),

    url(r'^my-dataset-detail/(?P<dataset_md5>\w{32})/$', 'view_single_dataset', name="view_single_dataset"),


    #url(r'^test-upload-success/$', 'view_test_upload_success', name="view_test_upload_success"),


    #url(r'^milestone-history/(?P<chosen_year>(\d){4})/$', 'view_milestone_history', name="view_milestone_history_by_year"),

    #url(r'^milestone-roadmap/(?P<repo_name>(\-|_|\w){1,120})/$', 'view_single_repo_column', name="view_single_repo_column"),

)

urlpatterns += patterns('apps.predict.views_run_script',
    url(r'^my-dataset-run-script/(?P<dataset_md5>\w{32})/$', 'view_run_dataset_script', name="view_run_dataset_script"),

    url(r'^my-dataset-run-notification/$', 'view_dataset_run_notification', name="view_dataset_run_notification"),

)

#urlpatterns += patterns('apps.predict.views_contact',
    #url(r'^my-dataset-contact/(?P<dataset_md5>\w{32})/$', 'view_dataset_contact', name="view_dataset_contact"),
#)