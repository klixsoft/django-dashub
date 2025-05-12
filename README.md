<h1 align="center" id="title">Dashub</h1>

<p align="center"><img src="https://socialify.git.ci/klixsoft/django-dashub/image?font=Inter&amp;forks=1&amp;issues=1&amp;language=1&amp;name=1&amp;owner=1&amp;pattern=Circuit%20Board&amp;pulls=1&amp;stargazers=1&amp;theme=Light" alt="project-image"></p>

<p>A modern Django admin dashboard with enhanced customization options, inspired by Jazzmin but featuring a fresh theme and additional functionality.</p>

## Features

- Customizable site title, logo, and favicon
- Custom theme color support
- Ordered menu and submenu management
- Custom links for side menu apps
- Custom sidebar menu support
- Related modal support for improved usability
- Enhanced UI tweaks with collapsible and tab-based change views

## Installation

Since Dashub is available on PyPI, you can install it directly using `pip`.

```bash
pip install django-dashub
```

## Configuration

To use Dashub, add it to your Django project's installed apps:

```python
INSTALLED_APPS = [
    'dashub',
    'django.contrib.admin',
    ...
]
```

## Customization

All the configuration settings for Dashub are defined in the `DASHHUB_SETTINGS` dictionary in your Django settings file. You can customize the appearance and behavior of the admin dashboard by modifying these settings.

### 1. Site Identification

### `site_logo`
Defines the path to the site logo image.

- **Example:**
  ```python
  "site_logo": "/static/logo.svg"
  
### `site_icon`
Defines the path to the site's favicon.

- **Example:**
  ```python
  "site_icon": "/static/favicon.ico"

### `theme_color`
Sets the theme color for the site. This will reflect in the browser's address bar or UI elements.

- **Example:**
  ```python
  "theme_color": "#31aa98"
  

### 2. **Hide Models**

### `hide_models`
This setting allows you to hide specific models in the Django admin panel. Models are specified using the `{app_name}.{model_name}` format, in lowercase. You can hide multiple models by listing them in an array.

- **Format:**
  ```python
  "hide_models": [
      "app_name.model_name",
      "another_app.another_model"
  ]
  ```

- **Example:**
  ```python
  "hide_models": [
      "user.group",
  ]
  ```

This configuration hides the `group` model from the `user` app.

---

## 3. **Custom Links**

### `custom_links`
Custom links are used to add new sections or menus to the sidebar of the admin interface. You can create custom sections by providing an array of menus under specific app names. 

Each menu item can have the following options:
- `name` (optional): The name of the menu item.
- `url` (optional): The URL to be linked to.
- `icon` (optional): The icon to display for the menu item (using Font Awesome classes).
- `order` (optional): Defines the order of the menu item (higher numbers appear higher).
- `submenu` (optional): A list of submenus within the menu. Each submenu can contain either a `model` key or an entire submenu structure.
- `model` (optional): If a model is passed, it will link directly to that model, removing the need to provide a `name` or `url`. Models are specified in lowercase as `{app_name}.{model_name}`.

Either model or name and URL are required for each menu item.

If the app specified in `custom_links` does not exist, it will create a new section for that app in the sidebar.

#### Example:
```python
"custom_links": {
    "advance": [
        {"name": "File Manager", "url": "/admin/filemanager/", "icon": "fa-solid fa-folder", "order": 1},
        {"model": "user.group", "icon": "fa-solid fa-user", "order": 2}
    ]
}
```

In this example:
- The "advance" section contains two menu items: "File Manager" and "User". If the "advance" section does not exist, it will be created. If exists then it will add the menu items to the existing section.

### 4. Submenus with Models
If you want a submenu to link to specific models, you can specify the `model` directly. This removes the need for a `url` or `name` in the submenu item.

#### Example:
```python
"core": [
    {
        "name": "User Management",
        "icon": "fa-solid fa-users",
        "submenu": [
            {"model": "auth.user", "order": 1},
            {"model": "auth.group", "order": 2}
        ]
    }
]
```

In this example, the submenu under "User Management" links directly to `auth.user` and `auth.group` models.

---

## 5. **Model Submenus**

### `model_submenus`
The `model_submenus` setting allows you to link specific models to submenus under other models or app sections. The configuration for model submenus is similar to that of `custom_links`, allowing you to specify both `model` and `submenu` for any app.

Each submenu can also contain a `model` key and/or a `submenu` structure.

- **Format:**
  ```python
  "model_submenus": {
      "app_name.model_name": [
          {"model": "app_name.model_name", "order": 1},
          {"model": "another_app.another_model", "order": 2}
      ]
  }
  ```

- **Example:**
  ```python
  "model_submenus": {
      "core.post": [
          {"model": "core.postcategory", "order": 1}
      ]
  }
  ```

In this configuration:
- The `core.post` model has a submenu linking to the `core.postcategory` model.

Submenus can also have their own submenu structure, just like the `custom_links` setting.

---

## 6. **Default Orders**

### `default_orders`
The `default_orders` setting defines the order in which menus and models are displayed in the admin interface. This helps control the sequence of items shown in the sidebar and the admin list views. A higher value indicates higher priority (i.e., the item appears at the top).

- **Format:**
  ```python
  "default_orders": {
      "app_name": order_value,
      "app_name.model_name": order_value
  }
  ```

- **Example:**
  ```python
  "default_orders": {
      "core": 10,
      "core.page": 2,
      "core.post": 1,
      "user": 20
  }
  ```

In this example:
- The `user` app has the highest priority (order `20`) so appear it first.
- The `core.page` model has the highest order (`1`), meaning it will be shown first.

---

## 7. **Icons**

### `icons`
The `icons` setting allows you to define icons for models and their submenus using Font Awesome class names. Icons are applied to models directly and help improve the visual presentation of the dashboard.

- **Format:**
  ```python
  "icons": {
      "app_name.model_name": "fa-icon-class"
  }
  ```

- **Example:**
  ```python
  "icons": {
      "core.page": "fa-regular fa-file",
      "core.post": "fa-regular fa-newspaper",
  }
  ```

This configuration assigns icons to `core.page`, `core.post`, and `healthpackage.lab` using Font Awesome icon classes.

- **Note:** Icons are only applied to models. Submenus do not have icons.

## 8. **Full Configuration Example**

Here is an example of a complete `DASHHUB_SETTINGS` configuration:

```python
DASHUB_SETTINGS = {
    "site_logo": "/static/logo.svg",
    "site_icon": "/static/favicon.ico",
    "theme_color": "#31aa98",
    "border_radius": "5px",
    "hide_models": [
        "auth",  # Hides all models in the auth app
        "auth.group"  # Hides the group model in the auth app
    ],
    "custom_links": {
        "auth": [
            {
                "model": "auth.post" # Links directly to the auth.post model
            },
            {
                "name": "User Management",
                "icon": "fa-solid fa-users",
                "submenu": [
                    {"model": "auth.user", "order": 1},
                    {"model": "auth.group", "order": 2}
                ]
            }
        ],
    },
    "submenus_models": ["auth.group"],
    "default_orders": {
        "auth": 10,
        "auth.group": 4,
    },
    "icons": {
        "auth": "fa-regular fa-user",
        "auth.user": "fa-regular fa-user",
    },
    "custom_js": [
        "/static/js/admin.js",
    ],
    "custom_css": [
        "/static/css/admin.css",
    ]
}
``` 

## Dependencies

- Django 3.2+
- Bootstrap 5
- Font Awesome 5 
- jQuery

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

GitHub Repository: [https://github.com/klixsoft/django-dashub](https://github.com/klixsoft/django-dashub)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
