# Environment Configuration

## Docker Compose Environment
The docker compose environment is managed with an environment file. Copy the environment file from [the examples folder](/example/env). And fill in the values accordingly.

### Environment Variable Explanation
**OPENAI_API_KEY**: API key *currently "legacy", will be switching to service account in the future"*

**OPENAI_DALLE_MODEL**: dall-e-3

**OPENAI_DALLE_IMAGE_SIZE**: string for the image dimensions, review the openai documentation for options, e.g. "1024x1024"

**OPENAI_DALLE_IMAGE_QUALITY**: Standard/Quality. *Review API pricing*

**DISCORD_BOT_KEY**: bot key from discord developer portal

**DISCORD_IMAGE_CHANNEL**: specify the channel the bot responds to image requests on

**OBJ_BUCKET**: storage bucketed created in MinIO, e.g. "boggart"

**AWS_ENDPOINT_URL**: Get from MinIO

**AWS_ACCESS_KEY_ID**: Get from MinIO

**AWS_SECRET_ACCESS_KEY**: Get from MinIO

**PGDATABASE**: Database name to set schema, e.g. "boggart"

**PGUSER**: Database user

**PGPASSWORD**: Database user password

**PGHOST**: hostname, if using the provided docker compose, use "http://minio:9000/"

**PGPORT**: 5432

## Postgres
### Schema
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS Users (
    UserID UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Username VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS GeneratedImages (
    ImageID SERIAL PRIMARY KEY,
    ImageLink VARCHAR(255) UNIQUE NOT NULL,
    TimeCreated TIMESTAMPTZ NOT NULL,
    UserID UUID NOT NULL,
    Prompt TEXT NOT NULL,
    Caption TEXT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
```