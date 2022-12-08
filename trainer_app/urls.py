from django.urls import path

from trainer_app import views

urlpatterns = [

    # --------------------------------------------------------------
    #    register and login urls common for both admin and trainer
    # --------------------------------------------------------------

    path('register', views.register_fun, name='register'),                              # it will display register_page.html output
    path('reg_data', views.reg_data_fun),                                               # it will store the data in  either in user table or it will store in trainer_reg table

    path('', views.log_fun, name='login'),                                              # it will display login.html
    path('log_data', views.log_data_fun),                                               # it will read the data and login as the admin or trainer

    # -------------------------------------------------------------
    #           admin module urls
    # -------------------------------------------------------------

    path('admin_home', views.admin_home_fun, name='admin_home'),                        # it will display the trainer admin_page.html
    path('trainer_details', views.trainer_details_fun, name='trainer_details'),         # it will display the trainer details
    path('delete/<int:id>', views.delete_fun, name='delete'),                           # it will delete the particular trainer details

    path('batch_assign', views.batch_assign_fun, name='batch_assign'),                  # it will display the batch_asign.html page
    path('batch_assign_data', views.batch_assign_data_fun),                             # it will store the data in the batch_assign table
    path('batch_details', views.batch_details_fun, name='batch_details'),               # it will display the batch_details.html page
    path('batch_delete/<int:id>', views.batch_delete_fun, name='batch_delete'),         # it will delete the particular trainer batch details
    path('batch_update/<int:id>', views.batch_update_fun, name='batch_update'),         # it will update the assigned batch

    # ----------------------------------------------------------------------
    #               trainer module urls
    # ----------------------------------------------------------------------

    path('trainer_home', views.trainer_home_fun, name='trainer_home'),                   # it will display the trainer home_page.html
    path('tbatch_details', views.tbatch_details_fun, name='tbatch_details'),             # it will display the particular trainer batch details
    path('Trainer_details', views.trainer_Details_fun, name='Trainer_details'),          # it will display the particular trainer details
    path('trainer_update/<int:id>', views.trainer_update_fun, name='trainer_update'),    # it will update the trainer details

    # -----------------------------------------------------------------------
    #           logot url common for both admin and trainer
    # -----------------------------------------------------------------------

    path('log_out', views.logout_fun, name='log_out')                                   # this logout url common for both trainer and for admin
]
