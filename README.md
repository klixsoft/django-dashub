<h1 align="center" id="title">Practet Dashboard</h1>

<p align="center"><img src="https://socialify.git.ci/scthakuri/practet-dashboard/image?font=Inter&amp;forks=1&amp;issues=1&amp;language=1&amp;name=1&amp;owner=1&amp;pattern=Circuit%20Board&amp;pulls=1&amp;stargazers=1&amp;theme=Light" alt="project-image"></p>

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

Since Practet Dashboard is not yet available on PyPI, you need to install it directly from GitHub.

```bash
pip install git+https://github.com/scthakuri/practet-dashboard.git
```

Alternatively, you can clone the repository and install it manually:
```bash
git clone https://github.com/scthakuri/practet-dashboard.git
cd practet-dashboard
```

## Configuration

To use Practet Dashboard, add it to your Django project's installed apps:

```python
INSTALLED_APPS = [
    'practet_dashboard',
    'django.contrib.admin',
    ...
]
```

## Customization

### Site Configuration

- `site_title` (str): The title of the site displayed in the header
- `site_logo` (str): The Full URL of the logo displayed in the header
- `site_icon` (str): The Full URL of the favicon displayed in the browser tab
- `theme_color` (str): Hex color code for the primary theme color.

### UI Enhancement

- `related_modal` (bool): Enable related modal for improved usability for related objects.

### Menu Ordering

- `order_menus` (list): A list of app names to order the menu items. The default order is the order of the installed apps.
  - `app` (str): The name of the app
  - `order` (int): The order of the app in the menu
  - `models` (list): List of models with custom order inside the app.

### Enable Submenu for Models

- `submenus_models` (list): List of models that will have submenus.

### Custom Links

- `custom_links` (list): List of custom links to display in the sidebar.
  - `name` (str): The name of the link
  - `url` (str): The URL of the link
  - `icon` (str): The Font Awesome icon class
  - `submenu` (list): List of submenus for the custom link
    - `name` (str): The name of the submenu
    - `url` (str): The URL of the submenu

## Example Configuration

```python
PRACTET_DASHBOARD_SETTINGS = {
    "site_title": "Practet Dashboard",
    "site_logo": "https://cdn.practet.com/static/logo-new.webp",
    "site_icon": "https://practet.com/static/favicon/favicon.ico",
    "theme_color": "#e31837",
    "related_modal_active": True,
    "order_menus": [
        {"app": "user", "order": 1},
        {"app": "advance", "order": 3},
        {
            "app": "oauth2_provider",
            "order": 2,
            "models": [
                {"model": "Applications", "order": 1},
                {"model": "Grant", "order": 2},
            ],
        },
    ],
    "submenus_models": ["user.user"],
    "custom_links": {
        "advance": [
            {
                "name": "File Manager",
                "url": "/admin/filehub/",
                "icon": "fas fa-folder",
                "submenu": [
                    {"name": "File Manager", "url": "/admin/filehub/"},
                    {"name": "Settings", "url": "/admin/filehub/settings/"},
                ],
            }
        ]
    }
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

GitHub Repository: [https://github.com/scthakuri/practet-dashboard](https://github.com/scthakuri/practet-dashboard)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
