CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS generated_images (
    id serial primary key,
    image_file text not null,
    time_created timestampz not null,
    prompt text not null,
    caption text not null
);

CREATE TABLE IF NOT EXISTS embeddings (
    id serial primary key,
    image_id serial not null,
    prompt_embedding vector(1024),
    caption_embedding vector(1024),
    foreign key (image_id) references generated_images(id)
);