# Environment Configuration

## Docker Compose Environment
The docker compose environment is managed with an environment file. Copy the environment file from [the examples folder](/example/env). And fill in the values accordingly.

### Environment Variable Explanation
**OPENAI_API_KEY**: 

**OPENAI_DALLE_MODEL**: 

**OPENAI_DALLE_IMAGE_SIZE**: 

**OPENAI_DALLE_IMAGE_QUALITY**: 

**DISCORD_BOT_KEY**: 

**DISCORD_IMAGE_CHANNEL**: 

**OBJ_BUCKET**: 

**AWS_ENDPOINT_URL**: 

**AWS_ACCESS_KEY_ID**: 

**AWS_SECRET_ACCESS_KEY**: 

**PGDATABASE**: Database name for 

**PGUSER**: 

**PGPASSWORD**: 

**PGHOST**: 

**PGPORT**: 

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