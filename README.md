## 🌐 Senior Python Engineer - Coding Assessment

## 🌐 LinkSpeed - Submission by James Mannix

### A FastAPI Full Stack Application including Notebook Server

---------------------------------------------------------------------------

#### ✅ Fully Asynchronous: Code/Design-Patterns, DB Driver, SQLAlchemy

#### ✅ Full-featured, Best Practice FastAPI App Structure and Code

#### ✅ Clean, Best-Practice Docker Compose Stack

#### ✅ Best-practice Data Loading, Query Optimization, Architecture

#### ✅ Cleanly-integrated Jupyter Notebook Server and .ipynb Solution

#### ✅ Complete working solution from cloning repo to MapBox visualization

---------------------------------------------------------------------------

#### 🔥 Today is Wednesday June 4th and it is 7:30 AM Pacific time.

#### 🔥 PLEASE STAY TUNED AND CHECK BACK TONIGHT OR TOMORROW!

#### 🔥 I am completing the extra problems and polishing a few odds and ends up!

#### 🔥 Thank you  for the opportunity!   James/Jim

---------------------------------------------------------------------------

## Quick Set Up

### Clone the repository and then cd into it.

You are now in the 'project root'. Most commands and actions, if not otherwise specified, should be done from this
directory. The project root is the directory with docker-compose.yml in it.

    git clone git@github.com:jimmygizmo/linkspeed.git

    cd linkspeed


---------------------------------------------------------------------------

## Start The LinkSpeed Stack

On the first startup, Magma (the FastAPI Microservices Python app) will create all the database objects
including the logical database itself, if necessary. The stack should work immediately. If not, simply restart it.

    docker-compose up 

### Operate the API and auto-generated API documentation (OpenAPI and Redocly)

You access port 48000 on localhost, since we map the default FastAPI port 8000 to 48000 outside the container.
Bedrock always uses ports in the 40-thousand ranges when mapping outside the Compose stack:
5432 -> 45432. 443 -> 44443, 8000 -> 48000, 80 -> 44080, etc.

    For OpenAPI interactive docs and API tools, navigate to:
    https://127.0.0.1:48000/docs

    For Redocly interactive docs, navigate to:
    https://127.0.0.1:48000/redoc

    Use the REST API:
    https://127.0.0.1:48000/
    https://127.0.0.1:48000/

    * YES, ONLY ONE ENDPOINT WITH THE FIRST RELEASE - Auth and other basic endpoints will be added very soon!


### Shut down the stack

    hit ctrl-C    (in the same console)

#### Visit [SmartMetal.ai](http://smartmetal.ai/ "SmartMetal.ai") for more information.
#### The Bedrock Stack is the foundation on which SmartMetal.ai is built.

---------------------------------------------------------------------------

## Development Environment

This section will soon get a lot of detailed and valuable information for Bedrock developers.


---------------------------------------------------------------------------

### This repository will be deleted or made private after the assessment and/or upon request.

---------------------------------------------------------------------------

