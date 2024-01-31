# Semantic Search Service
A RESTful API that allows for quickly searching images in a data store based on their content, leveraging [CLIP](https://openai.com/research/clip), OpenAI's image and language multimodal model.

## Technology Stack
- [FastAPI](https://fastapi.tiangolo.com/)
- PostgreSQL with [`pgvector`(https://github.com/pgvector/pgvector)] as a vector index for storing and comparing embeddings.
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [HuggingFace's instance of CLIP](https://huggingface.co/docs/transformers/model_doc/clip)
- [AWS S3](https://aws.amazon.com/s3/) bucket for image storage

## Environment Variables
These are the environment variables you will need to specify:

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

## TODO:
- Add tests.
- Add a license.
- Add a docker file for deployment.
- Implement logging framework.