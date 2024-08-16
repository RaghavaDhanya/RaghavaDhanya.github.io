---
title: "Keeping Configurations Sane with Pydantic Settings"
date: 2023-11-14T11:54:11+05:30
tags: ["yaml", "configurations", "python", "pydantic"]
categories:
    - general
cover:
    image: /images/sane-configs-with-pydantic-settings/cover.jpg
    caption: "Configurations"
    alt: "Configurations"
---
Configurations are a crucial aspect of any software project. There are many sources of configurations, such as environment variables, configuration files, and command-line arguments. For file-based configurations in python, YAML and TOML (or INI) are popular choices. I prefer YAML, though it is not without flaws, some of which can be addressed by Pydantic anyway like type safety etc. 

Pydantic is a data validation library for Python. It is built on top of Python type hints and provides runtime validation of data. Pydantic is widely used for data validation for APIs, but it can also be used for configuration management. Pydantic has a settings management library called `pydantic-settings` that makes it easy to load configurations from multiple sources.

In this post, we'll go through some of my favorite ways to manage configurations using Pydantic and `pydantic-settings`. We'll start with a simple example of loading configurations from a YAML file and then move on to loading configurations from multiple sources.

```bash
pip install pydantic>=2 pydantic-settings pyyaml
```
I'm using pydantic-settings 2.1.0 and pydantic 2.3.0 in the rest of the post.

Let's start with a simple YAML configuration file.

```yaml
# config.yaml
host: localhost
port: 5432
username: user
password: password
```

We can define a Pydantic model to represent this configuration. We are just using pydantic, we'll use pydantic-settings in more complex examples.

```python
from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
```

We can then use the `pydantic` module to parse the YAML configuration file.

```python
import yaml
from pydantic import ValidationError

with open("config.yaml", "r") as file:
    try:
        config = DatabaseConfig(**yaml.safe_load(file))
    except ValidationError as e:
        print("Invalid configuration file", e.json())
```

We can now access the configuration values using the model attributes.

```python
print(config.host)
print(config.port)
print(config.username)
print(config.password)
```

The types have been validated. You can define default values, constraints, and more using Pydantic. You can refer to the [Pydantic documentation](https://docs.pydantic.dev/latest/) for more information. 

Now let's see how we can use `pydantic-settings` to load configurations from multiple sources.

### Environment Variables Source
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    username: str = "user"
    password: str = "password"

    model_config = SettingsConfigDict(env_prefix="APP_")

settings = Settings()
```
Now, the configurations can be loaded from environment variables with the `APP_` prefix. For example, `APP_HOST`, `APP_PORT`, `APP_USERNAME`, and `APP_PASSWORD`. 

```bash
export APP_HOST=example.com
export APP_PORT=8080
export APP_USERNAME=admin
export APP_PASSWORD=secret
```

But the configurations can no longer be loaded from the YAML file. To load from yaml we need to add another source.

### YAML File Source
```python
from abc import abstractmethod
from typing import Any, Dict, Tuple, Type

from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
import yaml


class BaseFileConfigSettingsSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: Type[BaseSettings], path: str):
        super().__init__(settings_cls)
        self._data = self.load_file(path)

    @abstractmethod
    def load_file(self, path: str) -> Dict[str, Any]:
        pass

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        if field_name in self._data:
            return self._data[field_name], field_name, True
        else:
            return field.default, field_name, False

    def __call__(self) -> Dict[str, Any]:
        settings = {}
        for field_name, field in self.settings_cls.model_fields.items():
            value, _, _ = self.get_field_value(field, field_name)
            settings[field_name] = value
        return settings


class YamlConfigSettingsSource(BaseFileConfigSettingsSource):
    def load_file(self, path: str) -> Dict[str, Any]:
        with open(path, "r") as f:
            return yaml.safe_load(f)
```

```python
class Settings(BaseSettings):
    ...

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            YamlConfigSettingsSource(settings_cls, "config.yaml"),
            init_settings,
        )
```

Now the configurations can be loaded from both environment variables and the YAML file. The environment variables take precedence over the YAML file. This is generally what I use in my projects. You can override the config file's values with environment variables. This can be easily extended to TOML or other file formats as long as you can parse them into a dictionary.

### Command-line Arguments Source
Another source of configurations can be command-line arguments. I achieved this by just extending the EnvSettingsSource class.

```python
import sys
from typing import Type

from pydantic_settings import BaseSettings
from pydantic_settings.sources import EnvSettingsSource


class CliArgsSource(EnvSettingsSource):
    def __init__(self, settings_cls: Type[BaseSettings], prefix: str = "config_"):
        super().__init__(settings_cls, env_prefix=prefix)
        self._prefix = prefix
        self.env_vars = self._load_args()

    def _load_args(self):
        args = sys.argv[1:]
        env_vars = {}
        for i in range(len(args)):
            if args[i].startswith(f"--{self._prefix}"):
                if "=" in args[i]:
                    key, value = args[i].split("=")
                    key = key[2:].strip()
                    env_vars[key] = value.strip()
                elif i + 1 < len(args) and not args[i + 1].startswith("--"):
                    key = args[i][2:].strip()
                    env_vars[key] = args[i + 1].strip()
        return env_vars
```
    
```python
class Settings(BaseSettings):
    ...

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            YamlConfigSettingsSource(settings_cls, "config.yaml"),
            CliArgsSource(settings_cls, "app_"),
            init_settings,
        )
```
Now you can pass command-line arguments like `--app_host=example.com` to override the configurations from the YAML file and environment variables. This way, you can have a single source of truth for all your configurations.

### Nested Configurations
Pydantic also supports nested models, which can be useful for complex configurations. Let's say you have a nested configuration like this:

```yaml
# config.yaml
database:
  host: localhost
  port: 5432
  username: user
  password: password
app:
  name: myapp
  version: 1.0
```

You can define nested models like this:

```python
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str

class AppConfig(BaseModel):
    name: str
    version: str

class Settings(BaseSettings):
    database: DatabaseConfig
    app: AppConfig

    model_config = SettingsConfigDict(env_prefix="APP_", env_nested_delimiter="__")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            CliArgsSource(settings_cls, "app_"),
            YamlConfigSettingsSource(settings_cls, "config.yaml"),
            init_settings,
        )
```

You can pass the nested configurations as environment variables with the separator `__`.

For example,
```bash
export APP_DATABASE__HOST=example.com
export APP_DATABASE__PORT=8080
export APP_DATABASE__USERNAME=admin
export APP_DATABASE__PASSWORD=secret
export APP_APP__NAME=myapp
export APP_APP__VERSION=1.0
```

And since we are using `EnvSettingsSource` as base class for `CliArgsSource`, you can pass nested configurations as command-line arguments like 
```bash
python app.py --app_database__host=example.com --app_database__port=8080 --app_database__username=admin --app_database__password=secret --app_app__name=myapp --app_app__version=1.0
```

### Conclusion
Pydantic and `pydantic-settings` provide a powerful way to manage configurations in Python. You can load configurations from multiple sources like environment variables, YAML files, and command-line arguments. You can also define nested configurations and customize the sources to suit your needs. This makes it easy to manage configurations in a consistent and type-safe way. I hope this post helps you keep your configurations sane in your Python projects.
