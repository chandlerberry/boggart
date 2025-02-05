-- name: CreateGeneratedImage :one
INSERT INTO generated_images (image_file, time_created, prompt, caption)
VALUES ($1, CURRENT_TIMESTAMP AT TIME ZONE 'UTC', $2, $3)
RETURNING id;

-- name: GetAllPrompts :many
SELECT 
    g.id,
    g.prompt,
    g.image_file
FROM generated_images g;

-- name: GetAllCaptions :many
SELECT
    g.id,
    g.caption,
    g.image_file
FROM generated_images g;

-- name: GetAllPromptsAndCaptions :many
SELECT 
    g.id,
    g.prompt,
    g.caption,
    g.image_file
FROM generated_images g 
ORDER BY g.id ASC;

-- name: GetImageFile :one
SELECT g.image_file
FROM generated_images g
WHERE g.id = $1;

-- name: UpdateImageLink :exec
UPDATE generated_images
SET image_file = sqlc.arg(new_image_file)
WHERE id = $1;

-- name: StoreEmbeddings :exec
INSERT INTO embeddings (image_id, prompt_embedding, caption_embedding)
VALUES ($1, sqlc.narg(prompt_embedding)::vector, sqlc.narg(caption_embedding)::vector);

-- name: QueryPromptEmbeddings :many
SELECT g.prompt, g.caption, g.image_file, e.prompt_embedding
FROM embeddings e
JOIN generated_images g ON e.image_id = g.id
ORDER BY prompt_embedding <=> sqlc.narg(prompt)::vector LIMIT sqlc.arg(num_results);

-- name: QueryCaptionEmbeddings :many
SELECT g.caption, g.prompt, g.image_file, e.caption_embedding
FROM embeddings e
JOIN generated_images g ON e.image_id = g.id
ORDER BY caption_embedding <=> sqlc.narg(prompt)::vector LIMIT sqlc.arg(num_results);

-- name: GetAllPromptEmbeddings :many
SELECT prompt_embedding as embedding, image_id FROM embeddings;

-- name: GetAllCaptionEmbeddings :many
SELECT caption_embedding as embedding, image_id FROM embeddings;