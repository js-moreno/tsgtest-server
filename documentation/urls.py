""" Swagger documentation urls """

# Django
from django.urls import path
from django.conf import settings

# Drf Yasg
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)

        schema["x-tagGroups"] = [
            {"name": "Accounts", "tags": ["users"]},
            {"name": "Finances", "tags": ["credit-cards"]},
        ]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title=settings.APP_NAME + " API",
        default_version=settings.APP_VERSION,
        description="""
    This is the official documentation to {app} API. It has be documented in **OpenAPI v2** format and you can find out more in [Swagger.io](https://swagger.io/specification/v2/).

    # Introduction

    {app} API uses **REST** technology for interchanging data through the HTTP protocol, so it can be used almost for all programming languages. 
    We use many standard features, like HTTP verbs, noun URLs, HTTP response codes, all with the aim of making understandable, predecible and easly integrable.

    # Specification

    **JSON:API** is the specification used to request and respond (including errors), for more information you can visit [JsonAPI.org](https://jsonapi.org/format/)

    # Language

    Default service language is **Spanish**, but you can chage it from Headers e.g. `Accept-Language=en`.Supported languages are:
    -   Spanish (es)
    -   English (en)

    # Administration

    The administration site is an internal management tool. Here you can use your staff account and configure your API by searching, creating, changing and deleting records from a simple interface. Let's go to [Admin site](/admin).
        
        """.format(
            app=settings.APP_NAME
        ),
        contact=openapi.Contact(
            name="Support",
            email="juanse.jm18@gmail.com",
        ),
    ),
    public=True,
    generator_class=CustomSchemaGenerator,
)

url_documentation = [
    path("documentation/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
