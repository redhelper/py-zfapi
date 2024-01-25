---
Service Owner:
  - Rafael Calvo (@redhelper)
Secondary:
  - TBD
---

# py-ZFAPI


A wrapper for the ZeroFOX API for retrieving and updating customer data. Created to ease the developer experience on python projects to connect to said service

[Link to Backstage Docs](https://devportal.zerofox.com/docs/default/system/py-zfapi/)

## Available endpoints

- Entities
  - `LIST /1.1/entities/`
  - `GET /1.1/entities/{entity_id}`
- Enterprises
  - `LIST /1.0/enterprises/`
  - `LIST /2.0/enterprises/`
  - `GET /1.0/enterprises/{entity_id}`
  - `GET /2.0/enterprises/{entity_id}`
- Alerts
  - `LIST /1.1/alerts/`
  - `LIST /2.0/alerts/`
  - `GET /1.1/alerts/{alert_id}`
  - `GET /2.0/alerts/{alert_id}`

## Usage

The service was made to be as easy to use as possible:

- Import the client
- Create a client specifying a token and an env to point to
- Make calls to the required endpoint
  - All endpoints will always return the status code and the resulting json response
  - By default it will retry any 5XX and http errors

```python
import json

from py-zfapi.client import ZFApi

# ZF-API config
ZFAPI_TOKEN = "YOUR-TOKEN-HEHE"
zfapi = ZFApi(ZFAPI_TOKEN)

# list 2 entities for Datasources [Internal] including deleted
status_code, result = zfapi.entities.list_v1(
    query_params={
        "enterprise_id": 2831,
        "show_deleted": True,
        "limit": 2,
    }
)
# status_code=200 
# result={
#   "count": 336,
#   "next": "https://api-qa.zerofox.com/1.1/entities/?enterprise_id=2831&limit=2&page=2&show_deleted=true",
#   "previous": null,
#   "num_pages": 168,
#   "entities": [
#       {
#           "id": 74700738,
#           "name": "A fcano product4",
#           "enterprise": 2831,
#           "(...)",
#       },
#       {
#           "id": 74699429,
#           "name": "Aaron Hewett",
#           "enterprise": 2831,
#           "(...)"
#       }
#   ]
# }

# get entites
status_code, result = zfapi.entities.get_v1(entity_id=74700738)
# status_code=200 
# result={
#    "id": 74700738,
#    "name": "A fcano product4",
#    "log": [...],
#    "policy_id": 62403,
#    "enterprise_id": 2831,
#    "names": [...],
#    "organizations": [...],
#    (...),
# }

# get enterprises
status_code, result = zfapi.enterprises.get_v2(enterprise_id=73584583)
# status_code=200 
# result={
#    "id": 73584583,
#    "name": "slack test",
#    "company_name": null,
#    "status": "not specified",
#    "enabled_networks": [...],
#    "rbac_enabled": null,
#    "industry": null,
#    "salesforce_id": null,
#    "response_enrollmentcode": null
# }
```

## Local development

- First install poetry

  - ```bash
    pip install poetry
    ```

- Then you can run the rest
  - ```bash
    make sync-deps # Sync dependencies
    make fmt       # Format your changes
    make lint      # Run linter
    
    # Run pytest
    make test
    make test path=tests/endpoints/test_enterprises.py                                                                                                                                                     
    make test path=tests/endpoints/test_enterprises.py::TestEnterprisesEndpoint::test_list_v1                                                                                                                                                     
    ```

### Adding a new endpoint

- See CONTRIBUTING.md (TBD)