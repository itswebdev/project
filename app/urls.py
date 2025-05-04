from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.Landing, name="Landing"),

    path("camp_reg/", views.CampReg, name="CampReg"),
    path("police_reg/",views.PoliceReg, name="PoliceReg"),
    path("public_reg/",views.PublicReg,name="PublicReg"),
    path("volunteer_reg/", views.VolunteerReg, name="VolunteerReg"),
   # path("view_admin/",views.ViewAdmin,name="ViewAdmin"),

    path("camp_tables/",views.CampTable, name="CampTable"),
    path("station_tables/",views.StationTable, name="StationTable"),
    path("public_tables/",views.PublicTable, name="PublicTable"),
    path("volunteer_tables/",views.VolunteerTable, name="VolunteerTable"),
    path("camp_needs_table/",views.CampNeedsTable, name="CampNeedsTable"),

    path("login/",views.UserLogin,name="UserLogin"),
    path("logout/",views.Logout,name="Logout"),

    path("campHome/",views.CampHome, name='CampHome'),
    path("stationHome/",views.StationHome, name='StationHome'),
    path("publicHome/",views.PublicHome, name='PublicHome'),
    path("volunteerHome/",views.VolunteerHome, name='VolunteerHome'),

    path("editcamp/",views.EditCamp, name='EditCamp'),                             
    path("editstation/",views.EditStation, name='EditStation'),
    path("editpublic/",views.EditPublic, name='EditPublic'),
    path("editvolunteer/",views.EditVolunteer, name='EditVolunteer'),

    path('admin_view/',views.ViewAdmin2,name='ViewAdmin2'),

    path('camp_user_reg',views.CampAddUser,name="CampAddUser"),                     #         path of adding camp user
    path('campusersview',views.CampUsersView,name="CampUsersView"),                 #         path of viewing camp user
    path('camp_user_edit/<int:id>',views.EditCampUser,name="EditCampUser"),         #         path of editing camp user
    path('camp_user_delete/<int:id>/',views.CampUserDelete,name="CampUserDelete"),  #         path of deleting camp user

    path('camp_search',views.CampSearch,name="CampSearch"),

    path('camp_needs',views.CampNeedsSubmit,name="CampNeedsSubmit"),
    path('needs_view',views.NeedsViewTable,name="NeedsViewTable"),
    path('edit_camp_need/<int:id>',views.EditCampNeed,name="EditCampNeed"),
    path('delete_camp_need/<int:id>/',views.CampNeedsDelete,name="DeleteCampNeed"),
    path('set_camp_need_status/<int:id>',views.SetCampNeedStatus,name="SetCampNeedStatus"),

    path('camp_person_search',views.SearchCampPerson,name="SearchCampPerson"),
    path('person_search',views.SearchPerson,name="SearchPerson"),
    path('ReportMissingPerson/<int:id>',views.ReportMissingPerson,name="ReportMissingPerson"),    # missing person search


    path('camp_alert',views.CampAlerts,name="CampAlerts"),
    path('camp_alert_table',views.CampAlertTable,name="CampAlertTable"),
    path('alert_table',views.AlertCampTable,name="AlertCampTable"), 
    path('delete_alert/<int:id>',views.DeleteAlert,name="DeleteAlert"), 
    
    #       Request for volunteers required by camp

    path('volunteer_req',views.VolunteerReq,name="VolunteerReq"),
    path('volunteer_req_table',views.VolunteerReqTable,name="VolunteerReqTable"),
    path('req_volunteer_table',views.ReqVolunteerTable,name="ReqVolunteerTable"),
    path('edit_volunteer_req/<int:id>',views.EditVolunteerReq,name="EditVolunteerReq"),
    path('delete_volunteer_req/<int:id>',views.DeleteVolunteerReq,name="DeleteVolunteerReq"),

    path('volunteer_allocate_table/<int:id>/<int:requestid>',views.VolunteerAllocateTable,name="VolunteerAllocateTable"),
    path('VolAllocateNow/<int:campid>/<int:id>/<int:volreqid>',views.VolAllocateNow,name="VolAllocateNow"),
    path('VolDeAllocate/<int:campid>/<int:id>/<int:volreqid>',views.VolDeAllocate,name="VolDeAllocate"),
    
    path('Notification',views.Notification,name="Notification"),

    path('PublicComplaint',views.PublicComplaint,name="PublicComplaint"),
    path('ViewComplaints',views.ViewComplaints,name="ViewComplaints"),
    path('ListComplaints',views.ListComplaints,name="ListComplaints"),
    path('EditComplaint/<int:id>',views.EditComplaint,name="EditComplaint"),
    path('DeleteComplaint/<int:id>',views.DeleteComplaint,name="DeleteComplaint"),
    path('allocated_vol_List',views.AllocatedVolList,name="AllocatedVolList"),
    path('ComplaintReply/<int:id>',views.ComplaintReply,name="ComplaintReply"),
    path('ShowReply/<int:id>',views.ShowReply,name="ShowReply"),
    path('allocated_vol_List',views.AllocatedVolList,name="AllocatedVolList"),            #    List of the volunteers assingned to the camp
    path('ScheduleDuty/<int:camp>/<int:volunteer>',views.ScheduleDuty,name="ScheduleDuty"),
    path('ReScheduleDuty/<int:camp>/<int:volunteer>',views.ReScheduleDuty,name="ReScheduleDuty"),

    path('FundAllocationRequest',views.FundAllocationRequest,name="FundAllocationRequest"),
    path('FundAllocationRequestList',views.FundAllocationRequestList,name="FundAllocationRequestList"),
    path('FundAllocationRequestEdit/<int:id>',views.FundAllocationRequestEdit,name="FundAllocationRequestEdit"),
    path('FundAllocationRequestDelete/<int:id>',views.FundAllocationRequestDelete,name="FundAllocationRequestDelete"),
    path('FundAllocationRequestView',views.FundAllocationRequestView,name="FundAllocationRequestView"),
    path('ViewFundAllocationRequest/<int:id>',views.ViewFundAllocationRequest,name="ViewFundAllocationRequest"),
    path('AllocateFund/<int:id>',views.AllocateFund,name="AllocateFund"),
    path('Payment/<int:id>/<int:amount>',views.Payment,name="Payment"),
    # path('ScheduleNotify/<int:camp>',views.ScheduleNotify,name="ScheduleNotify"),
    path('ViewMissingReports',views.ViewMissingReports,name="ViewMissingReports"),
    path('AddMissingStatus/<int:id>',views.AddMissingStatus,name="AddMissingStatus"),
    path('ViewMissingList',views.ViewMissingList,name="ViewMissingList"),
    path('EditMissingStatus/<int:id>',views.EditMissingStatus,name="EditMissingStatus"),
    path('DeleteMissingStatus/<int:id>',views.DeleteMissingStatus,name="DeleteMissingStatus"),
     

    path('StationSearch',views.StationSearch,name="StationSearch"),


    path('EmergencyMessageAlert',views.EmergencyMessageAlert,name="EmergencyMessageAlert"),
    path('EmergencyAlertList',views.EmergencyAlertList,name="EmergencyAlertList"),
    path('EditEmergencyAlert/<int:id>',views.EditEmergencyAlert,name="EditEmergencyAlert"),
    path('DeleteEmergencyAlert/<int:id>',views.DeleteEmergencyAlert,name="DeleteEmergencyAlert"),
    path('EmergencyAlertView',views.EmergencyAlertView,name="EmergencyAlertView"),

    path('TableCamp',views.TableCamp,name="TableCamp"),
    path('CampEnquiry/<int:id>',views.CampEnquiry,name="CampEnquiry"),
    path('EnquiryTable',views.EnquiryTable,name="EnquiryTable"),
    path('EnquiryReply/<int:id>',views.EnquiryReply,name="EnquiryReply"),
    path('EnqResponseTable',views.EnqResponseTable,name="EnqResponseTable"),

    path('VehicleMissing/<int:id>',views.VehicleMissing,name="VehicleMissing"),
    path('VehicleMissingReports',views.VehicleMissingReports,name="VehicleMissingReports"),
    path('VehicleStatus/<int:id>',views.VehicleStatus,name="VehicleStatus"),
    path('EditVehicleStatus/<int:id>',views.EditVehicleStatus,name="EditVehicleStatus"),
    path('DeleteVehicleStatus/<int:id>',views.DeleteVehicleStatus,name="DeleteVehicleStatus"),
    path('VehicleList',views.VehicleList,name="VehicleList"),
    path('ComfirmPassCamp',views.ComfirmPassCamp,name="ComfirmPassCamp"),

    path('AddProduct',views.AddProduct,name="AddProduct"),
    path('ViewProduct',views.ViewProduct,name="ViewProduct"),
    path('EditProduct/<int:id>',views.EditProduct,name="EditProduct"),
    path('DeleteProduct/<int:id>',views.DeleteProduct,name="DeleteProduct"),
    path('ProdUsage/<int:id>',views.ProdUsage,name="ProdUsage"),
    path('MonthlyReport',views.MonthlyReport,name="MonthlyReport"),
    path('PerDayReport',views.PerDayReport,name="PerDayReport"),

    path('send_otp_view',views.send_otp_view,name="send_otp_view"),
    path('verify_otp_view/<str:email>/',views.verify_otp_view,name="verify_otp_view"),
    path('reset_password_view',views.reset_password_view,name="reset_password_view"),
    

    path("weather/", views.get_weather, name="weather"),
    path('misschecking/', views.misschecking, name='misschecking'),
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # new 
