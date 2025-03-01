# Django-Jestit Documentation

Django-Jestit is a streamlined set of Django applications and a lightweight REST framework designed to simplify user authentication, authorization, and efficient API testing. This documentation provides descriptions and examples to help you get started quickly.

## Why Django-Jestit?

We built Django-Jestit to address the complexity and overhead of existing REST frameworks. Many frameworks are feature-heavy, making them cumbersome for projects that require simplicity, speed, and robust security.

## Key Differentiators

- **Lightweight Framework:** Django-Jestit is minimalistic, providing an easy way to add REST APIs to your Django models without unnecessary complexity.
- **Built-in Security:** Security is integral to Django-Jestit. We offer an alternative to Django's built-in permissions system, automatically protecting your REST APIs and data.
- **Robust Object-Level Permission System:** Unlike Django's native model-level permissions, Django-Jestit provides a simple yet robust permission system at the object level. This allows fine-grained control, enabling permissions to be applied to individual objects and extended to both user and group levels.
- **Effortless Integration:** Adding REST endpoints to your models is straightforward, enabling rapid development without compromising security or performance.

With Django-Jestit, you get a simple, efficient framework with powerful security features designed for developers who value speed and control.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Authit - Authentication and Authorization](#authit)
   - [JWT Authentication Middleware](#jwt-authentication)
   - [Models](#models)
   - [REST API](#authit-rest-api)
4. [Jestit - REST Framework](#jestit)
   - [URL Decorators](#url-decorators)
   - [GraphSerializer](#graphserializer)
5. [Testit - Testing Suite](#testit)
   - [Writing Tests](#writing-tests)
   - [Running Tests](#running-tests)
6. [Taskit - Task Runner](#taskit)
7. [Utilities](#utilities)
8. [Contributing](#contributing)
9. [License](#license)

## Overview

Django-Jestit is a collection of Django-based applications focused on authentication, task management, and testing. These tools are built to enhance development efficiency by providing utilities for common requirements such as user management, token-based authentication, and automated testing.

## Installation

```bash
pip install django-jestit
```

## Detailed Documentation

For detailed information about each module and its usage, refer to the documentation within the `docs` folder:

- [AuthIt Documentation](docs/authit.md): Authentication and authorization management with JWT support.
- [Jestit REST Documentation](docs/rest.md): Provides RESTful API capabilities for Django models.
- [TestIt Documentation](docs/testit.md): Offers tools and utilities for testing Django applications.
- [TaskIt Documentation](docs/taskit.md): Handles task management and processing with Redis.
- [Jestit Decorators Documentation](docs/decorators.md): Describes decorators to enhance Django views with HTTP routing, validation, etc.
- [Helpers Documentation](docs/helpers.md): Lists various helper utilities for common tasks.
- [Metrics Documentation](docs/metrics.md): Details on recording and retrieving metrics using Redis.
- [Cron Scheduler Documentation](docs/cron.md): Explains task scheduling using a cron syntax.

## Contributing

We welcome contributions! Please create an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
