from django.urls import path
from main.views import (
    show_main,
    show_experience,
    show_education,
    create_education,
    get_education_json,
    get_education_xml,
    delete_education,
    update_education,
    create_project,
    register,
    login_user,
    logout_user,
    toggle_star,
    get_projects_json,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("education/create/", create_education, name="create_education"),
    path("education/json/", get_education_json, name="get_education_json"),
    path("education/xml/", get_education_xml, name="get_education_xml"),
    path("education/delete/<uuid:education_id>/", delete_education, name="delete_education"),
    path("education/update/<uuid:education_id>/", update_education, name="update_education"),
    path("project/create/", create_project, name="create_project"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("project/star/<int:project_id>/", toggle_star, name="toggle_star"),
    path("get-projects-json/", get_projects_json, name="get_projects_json"),
]