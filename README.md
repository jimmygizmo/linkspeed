## 🌐 Senior Python Engineer - Coding Assessment

## 🌐 LinkSpeed - Submission by James Mannix

### A FastAPI Full Stack Application including Notebook Server

---------------------------------------------------------------------------

#### 🔥 Fully Asynchronous Code, Components and Architecture

#### ✅ Full-featured, Best Practice FastAPI App Structure and Code

#### ✅ Clean, Best-Practice Docker Compose Stack

#### ✅ Best-practice Data Loading, Query Optimization, Architecture

#### ✅ Cleanly-integrated Jupyter Notebook Server and .ipynb Solution

#### ✅ Complete working solution from cloning repo to MapBox visualization

---------------------------------------------------------------------------

#### 🔥 Today is Wednesday June 4th and it is 7:30 AM Pacific time.

#### 🔥 PLEASE STAY TUNED AND CHECK BACK TONIGHT OR TOMORROW!

#### 🔥 I am completing the extra problems and polishing a few odds and ends up!

#### 🔥 Thank you  for the opportunity!

---------------------------------------------------------------------------

## Quick Set Up

### 1. Clone the repository and then cd into it.

The project root is the directory with docker-compose.yml in it.


    git clone git@github.com:jimmygizmo/linkspeed.git

    cd linkspeed


---------------------------------------------------------------------------
### 2. Launch the Docker Compose Full Stack, thus launching:
- Async FastAPI Python application in a Python container.
- PostGIS PostgreSQL DB Server in a PostGIS container.
- Jupyter Notebook Server in a Python container.

#### NOTE: Database and tables are automatically created upon first startup and persisted by Docker.

    docker compose up



---------------------------------------------------------------------------
### 3. Create local virtual environment for running the DB seed script (data loader)
#### NOTE: Nice instructions for these simple steps are coming later today.
#### ESSENTIALLY: 1. Create a virtual env.    2. install reqs: /linkspeed/fastapi/requirements.txt


---------------------------------------------------------------------------
### 4. Load the Parquet data using the seed.py script
#### NOTE: Later today I may make this script even easier to locate or maybe make data-seeding automatic.

    NAVIGATE TO THE SEED SCRIPT (in FastAPI standard location):

    cd fastapi/magma/seed

    RUN THE SEED SCRIPT:

    python ./seed.py



---------------------------------------------------------------------------

### 4. Navigate with your Web Browser to the Jupyter Server and the solution .ipynb file

    ----> NAVIGATE TO THE JUPYTER SERVER:

    http://localhost:48888/

    Open file: ---- traffic.ipynb


    ----> NAVIGATE TO THE OPENAPI/SWAGGER API TOOLS & DOCS:

    http://localhost:48000/docs


    ----> NAVIGATE TO THE API ITSELF:

    http://localhost:48000


---------------------------------------------------------------------------

During today (June 4th) I will add some more clear information here about this solution/repository.
As I noted above, I am still putting some finishing touches on it and completing the extra questions.
The main solution in the Jupyter Notebook and the FastAPI application all work perfectly and are
expertly engineered. Thank you for the opportunity to present this!

---------------------------------------------------------------------------

### This repository will be deleted or made private after the assessment and/or upon request.

---------------------------------------------------------------------------

