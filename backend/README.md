# spacex

### Folder structure
```bash
.
├── app
│   ├── core                # Core domain & business logic (entities, use cases)
│   │   ├── domain          # Entities, value objects, domain exceptions
│   │   └── usecases        # Application services (e.g., retrieve or update domain data)
│   ├── infrastructure      # Technical details (DB, external APIs, caching, etc.)
│   │   ├── db              # Database config, migrations, connection handling
│   │   └── repositories    # Persistence adapters (e.g., SQLAlchemy repositories)
│   └── api                 # Presentation layer (FastAPI endpoints, request/response schemas)
│       └── routers         # Group routers by resource (rockets, launches, starlinks, etc.)
├── tests                   # All tests, mirroring the app structure
│   ├── core
│   │   ├── domain
│   │   └── usecases
│   ├── infrastructure
│   │   └── repositories
│   └── api
│       └── routers
├── main.py                 # HTTP Request handler - FastAPI 
├── requirements.txt        # Dependencies
└── README.md
```