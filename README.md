```Async-Mojang``` is a Python package for accessing Mojang's services. This library can be used to convert UUIDs, get a profile's information, change your Minecraft username or skin, and much more. 

There is one component to this package:

- **Public API** - Used to parse information about Minecraft profiles and more. Authentication is not required.

## Installation
**Python 3.7 or higher is required.**

The easiest way to install the library is using `pip`. Just run the following console command:

```
python -m pip install async-mojang
```

## **Public API Quickstart**

```py
from mojang import API

# Create a Public API instance
api = API()

uuid = api.get_uuid("Notch")

if not uuid:
    print("Notch is not a taken username.")
else:
    print(f"Notch's UUID is {uuid}")

    profile = api.get_profile(uuid)
    print(f"Notch's skin URL is {profile.skin_url}")
    print(f"Notch's skin variant is {profile.skin_variant}")
    print(f"Notch's cape URL is {profile.cape_url}")
```