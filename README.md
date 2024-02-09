# Semantic Image Search API
A RESTful API that allows for quickly searching images based on their content using natural language by leveraging [CLIP](https://openai.com/research/clip), OpenAI's image and language multimodal model.

Code testing coverage is 98%.

## Technology Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- PostgreSQL with [pgvector](https://github.com/pgvector/pgvector) as a vector index for storing and comparing embeddings.
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [HuggingFace's instance of CLIP](https://huggingface.co/docs/transformers/model_doc/clip)
- [AWS S3](https://aws.amazon.com/s3/) bucket for image storage

## Running Locally with a Virtual Environment
You will need to:
1. Set up an AWS S3 bucket with appropriate permissions for an external service to make API calls to it.
2. Specify environment variables in a `.env` file (see below).
3. Create a virtual environment in the root of the project: `python3 -m venv venv`.
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the dependencies: `pip3 install -r requirements.txt`
7. Create a local relational database for storing image urls, embeddings, and metadata. Update the value of `SQLALCHEMY_DATABASE_URI` in the `.env` file accordingly.
8. Enable the pgvector extension in the database by connecting to it and running `CREATE EXTENSION vector;`

### Environment Variables
These are the environment variables you will need to specify in a `.env` file:

```
# Database
SQLALCHEMY_DATABASE_URI = <your-database-uri> # postgresql://postgres:password@db:5433/semantic_pic if using this project's compose.yaml values

# App auth
ADMIN_PW = <strong-admin-password> # For authenticating the protected POST and DELETE routes via Authorization header.

# AWS
AWS_ACCESS_KEY = <your aws access key>
AWS_SECRET_ACCESS_KEY = <your aws secret access key>
REGION =  <your aws region>
BUCKET_NAME = <your aws s3 bucket name>

# CORS
ALLOWED_ORIGINS=[<list of allowed origins>]
```

### Running the Development Server
- To run the dev server, run `uvicorn app.main:app --reload`

### Swagger Doc
- Once the dev server is running, go to localhost:8000/docs to view the Swagger docs. You can use this to test out the API locally. 

## Running Locally with Docker Compose
Follow steps 1 and 2 from "Running Locally with a Virtual Environment" above. Then:
1. Make sure you have Docker installed.
2. Run `docker compose up --build` in the root directory to build the images and run the containers.

### Swagger Doc
- Once the containers are running, go to http://0.0.0.0:8000/docs to view the Swagger docs. You can use this to test out the API locally. 

## Tests
Tests are configured to run against a test database and test S3 bucket. To run the tests, you will need to:
- Configure a test S3 bucket in AWS with appropriate permissions for an external service to make API calls to it.
- Create a test relational database locally. Enable the pgvector extension in the database by connecting to it and running `CREATE EXTENSION vector;`
- Update the `pytest.ini` file in the root of the project. This contains environment variables that, during testing, will override those specified in the `.env`:
    ```
    [pytest]
    env =
        BUCKET_NAME=<your-test-bucket-name>
        SQLALCHEMY_DATABASE_URI=<your-test-database-uri>
    ```

### Running Tests
To run all tests and generate a coverage report, run `pytest --cov --cov-report=html:coverage` in the root of the project if using a virtual environment, or inside the API container if using Docker.