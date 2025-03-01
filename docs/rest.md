# Jestit: Empowering Django Models with RESTful API Capabilities

Jestit transforms Django models into a RESTful API, enabling developers to easily expose and manage model data via HTTP. This documentation provides a comprehensive guide on setting up Jestit within your Django project, focusing on the `RestMeta` configuration and offering basic to advanced usage examples.

## Setup

To begin using Jestit in your Django project, follow these steps:

1. **Add Jestit to Django Settings**: Ensure that Jestit is recognized by adding it to your Django settings. Place `jestit` within the `INSTALLED_APPS` list in your `settings.py` file:

    ```python
    INSTALLED_APPS = [
        ...
        'jestit',
    ]
    ```

2. **Migrate Database**: Execute Django migrations to incorporate necessary database changes:

    ```bash
    python manage.py migrate
    ```

3. **Configure Jestit Settings**: Jestit functionality relies on customizable settings. Ensure relevant Jestit settings are defined in your `settings.py`:

    ```python
    JESTIT_API_MODULE = "api"
    JESTIT_APPEND_SLASH = True  # Or False based on your preference
    ```

## `RestMeta` Configuration in Django Models

`RestMeta` facilitates integrating Django models into the RESTful framework. Here's how to configure it:

1. **Define Your Model**: Create your Django model as usual but include a nested class `RestMeta` to define the RESTful behavior:

    ```python
    from django.db import models
    from jestit.models import JestitBase

    class MyModel(JestitBase):
        name = models.CharField(max_length=100)
        created = models.DateTimeField(auto_now_add=True)

        class RestMeta:
            VIEW_PERMS = ["view_mymodel"]
            SAVE_PERMS = ["add_mymodel", "change_mymodel"]
            DELETE_PERMS = ["delete_mymodel"]
            LIST_DEFAULT_FILTERS = {"is_active": True}
            GRAPHS = {
                "default": {
                    "fields": ['id', 'name', 'created']
                }
            }
    ```

2. **Permissions**: `RestMeta` utilizes permission keys (`VIEW_PERMS`, `SAVE_PERMS`) to control user actions on records:

    - `VIEW_PERMS`: Defines permissions needed for viewing records.
    - `SAVE_PERMS`: Permissions required for creating or updating.
    - `DELETE_PERMS`: Permissions needed to delete models.

3. **Graphs**: `GRAPHS` allow for structured API responses, letting you predefine output formats:

    - Fields: Specifies which fields are returned as part of the API response.

## Converting Django Models into a RESTful API

Define endpoints with Jestit's decorators to effortlessly convert Django models into REST APIs:

```python
from jestit.decorators import GET, POST, DELETE

@GET('mymodel/<int:pk>/')
def get_mymodel(request, pk):
    return MyModel.on_rest_request(request, pk)

@POST('mymodel/')
def create_mymodel(request):
    return MyModel.on_rest_request(request)

@DELETE('mymodel/<int:pk>/')
def delete_mymodel(request, pk):
    return MyModel.on_rest_request(request, pk)
```

## Basic Usage Examples

### Listing Models

To list instances of a model:

```python
@GET('api/mymodels/')
def list_mymodels(request):
    return MyModel.on_rest_handle_list(request)
```

### Retrieving a Single Instance

```python
@GET('api/mymodel/<int:pk>/')
def get_single_mymodel(request, pk):
    return MyModel.get_instance_or_404(pk)
```

## Advanced Features and Customization

### Custom Filters and Sorting

Implement additional filtering/sorting logic directly within your model class:

```python
@classmethod
def on_rest_list_filter(cls, request, queryset):
    filters = {"name__icontains": request.GET.get('name', '')}
    return queryset.filter(**filters)
```

### Handling Permissions

Customize permission checks through the model:

```python
@classmethod
def rest_check_permission(cls, request, permission_keys, instance=None):
    # Custom logic for checking permissions
    return super().rest_check_permission(request, permission_keys, instance)
```

### Graph Serializer for Nested Data

Serialize nested relationships using the `GRAPHS` configuration:

```python
class MyModel(JestitBase):
    ...
    class RestMeta:
        GRAPHS = {
            "default": {
                "fields": ['id', 'name'],
                "graphs": {
                    "related_field": "related_graph"
                }
            }
        }
```

With Jestit, converting Django models into an API endpoint becomes seamless, saving time and reducing the complexities involved in building RESTful APIs from scratch. Customize as needed to match the specific requirements of your Django application.
