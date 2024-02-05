# Semantic Image Search API
A RESTful API that allows for quickly searching images based on their content using natural language by leveraging [CLIP](https://openai.com/research/clip), OpenAI's image and language multimodal model.

Code testing coverage is 98%.

## Technology Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- PostgreSQL with [pgvector](https://github.com/pgvector/pgvector) as a vector index for storing and comparing embeddings.
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [HuggingFace's instance of CLIP](https://huggingface.co/docs/transformers/model_doc/clip)
- [AWS S3](https://aws.amazon.com/s3/) bucket for image storage

## Running Locally
You will need to:
- Create a virtual environment in the root of the project: `python3 -m venv venv`.
- Activate the virtual environment: `source venv/bin/activate`
- Install the dependencies: `pip3 install -r requirements.txt`
- Configure an AWS S3 bucket to store images in.
- Create a local relational database.

### Environment Variables
These are the environment variables you will need to specify in a `.env` file:

```
# Database
SQLALCHEMY_DATABASE_URI = <your-database-uri>

# App auth
ADMIN_PW = <strong-admin-password>

# AWS
AWS_ACCESS_KEY = <your-aws-access-key>
AWS_SECRET_ACCESS_KEY = <your-aws-secret-access-key>
REGION =  <your-aws-region>
BUCKET_NAME = <your-aws-s3-bucket-name>
```
### Running the Development Server
- To run the dev server, run `uvicorn app.main:app --reload`

## Tests
Tests are configured to run against a test database and test S3 bucket. You will need to:
- Configure a test S3 bucket in AWS.
- Create a test database locally. 
- Create a `pytest.ini` file in the root of the project. This will contain an environment variable with the name of your _test_ S3 bucket to override the production bucket name in the `.env` file:
    ```
    [pytest]
    env =
        BUCKET_NAME=<your-test-bucket-name>
        SQLALCHEMY_DATABASE_URI=<your-test-database-uri>
    ```

### Running Tests
To run all tests and generate a coverage report, run `pytest --cov --cov-report=html:coverage`.

## TODO:
- Add a license.
- Add a docker file for deployment.
- Implement logging framework.