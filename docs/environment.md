# Environment Configuration

## Bot
### Docker Container Environment Vars
- openai_api_key
- openai_dalle_model
- openai_dalle_image_size
- openai_dalle_image_quality
- discord_bot_key
- discord_image_channel
- backblaze_endpoint_url
- backblaze_application_key_id
- backblaze_application_key
- backblaze_bucket_name
- postgres_username
- postgres_password
- postgres_database
- postgres_host
- postgres_port

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

### Docker Environment Variables
- postgres_username
- postgres_password
- postgres_database