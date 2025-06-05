## Senior Python Engineer - Coding Assessment

## 🌐 LinkSpeed - Submission by James Mannix

### A FastAPI Full Stack Application including Notebook Server

---------------------------------------------------------------------------

#### ✅ Fully asynchronous code (with Dependency Injection) & async driver

#### ✅ Full-featured, best-practice FastAPI app structure, modular code

#### ✅ Clean, best-practice Docker Compose stack

#### ✅ Best-practice data loading, query-optimization, optimized processing

#### ✅ Cleanly-integrated Jupyter Notebook Server and .ipynb solution

#### ✅ PostGIS Postgres and all best-practice geospatial library usage

#### ✅ Automatic DB initialization. Automatic smart data seeding

#### ✅ Complete working solution from cloning repo to MapBox visualization

---------------------------------------------------------------------------

#### 🔵 PLEASE NOTE: The Architecture Chart and the extra questions are pending.

#### 🔵 As time allows for other job interviews, I will update more if possible.

#### 🔵 Thank you for this opportunity!

---------------------------------------------------------------------------

## Quick Set Up

### 1. Clone the repository and then cd into it.

You will be in the project/repository root. The root is the directory with docker-compose.yml in it.


    git clone git@github.com:jimmygizmo/linkspeed.git

    cd linkspeed


---------------------------------------------------------------------------
### 2. Launch the Docker Compose Full Stack, thus launching:
- Async FastAPI Python application in a Python container
- PostGIS PostgreSQL DB Server in a PostGIS container
- Jupyter Notebook Server in a Python container


    docker compose up

IMPORTANT: Data-seeding is automatic but takes 3-4 minutes. Upon FIRST STARTUP only, watch the log for status on data
loading. You will see "✅ Links loaded" and then "✅ SpeedRecords loaded". You can then use the API.

---------------------------------------------------------------------------

### 3. Navigate with your Web Browser to the Jupyter Server and the solution .ipynb file

    ----> NAVIGATE TO THE JUPYTER SERVER:

    http://localhost:9797

    Open this file if it is not already open for you: ---- traffic.ipynb


    ----> NAVIGATE TO THE OPENAPI/SWAGGER API TOOLS & DOCS:

    http://localhost:3131/docs


    ----> NAVIGATE TO THE API ITSELF:

    http://localhost:3131


    ----> SINGLE LINK (for day/period), AGGREGATED, WITH METADATA (GeoJSON):

    http://localhost:3131/aggregates/16981048?day=wednesday&period=am_peak


    ----> ALL LINKS (for day/period), AGGREGATED, WITH METADATA (GeoJSON):

    http://localhost:3131/aggregates?day=wednesday&period=am_peak


    ----> SLOW LINKS (under threshold for given days), AGGREGATED, WITH METADATA (GeoJSON):

    http://localhost:3131/patterns/slow_links?period=am_peak&threshold=20&min_days=1

---------------------------------------------------------------------------

This is a very polished project/submission, but I am still working on the extra questions and
architecture chart as my very limited time allows. (I can create top-quality charts and diagrams.)
I will provide further updates as I can, but especially upon request.
Thank you for the opportunity to be considered for this role!

---------------------------------------------------------------------------

#### * *This repository will be deleted or made private after the assessment and/or upon request.*

---------------------------------------------------------------------------

