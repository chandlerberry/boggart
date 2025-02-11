# Code generated by sqlc. DO NOT EDIT.
# versions:
#   sqlc v1.28.0
# source: db.sql
import pydantic
from typing import Any, AsyncIterator, Optional

import sqlalchemy
import sqlalchemy.ext.asyncio

from boggart import models


CREATE_GENERATED_IMAGE = """-- name: create_generated_image \\:one
INSERT INTO generated_images (image_file, time_created, prompt, caption)
VALUES (:p1, CURRENT_TIMESTAMP AT TIME ZONE 'UTC', :p2, :p3)
RETURNING id
"""


GET_ALL_CAPTION_EMBEDDINGS = """-- name: get_all_caption_embeddings \\:many
SELECT caption_embedding as embedding, image_id FROM embeddings
"""


class GetAllCaptionEmbeddingsRow(pydantic.BaseModel):
    embedding: Optional[Any]
    image_id: int


GET_ALL_CAPTIONS = """-- name: get_all_captions \\:many
SELECT
    g.id,
    g.caption,
    g.image_file
FROM generated_images g
"""


class GetAllCaptionsRow(pydantic.BaseModel):
    id: int
    caption: str
    image_file: str


GET_ALL_PROMPT_EMBEDDINGS = """-- name: get_all_prompt_embeddings \\:many
SELECT prompt_embedding as embedding, image_id FROM embeddings
"""


class GetAllPromptEmbeddingsRow(pydantic.BaseModel):
    embedding: Optional[Any]
    image_id: int


GET_ALL_PROMPTS = """-- name: get_all_prompts \\:many
SELECT 
    g.id,
    g.prompt,
    g.image_file
FROM generated_images g
"""


class GetAllPromptsRow(pydantic.BaseModel):
    id: int
    prompt: str
    image_file: str


GET_ALL_PROMPTS_AND_CAPTIONS = """-- name: get_all_prompts_and_captions \\:many
SELECT 
    g.id,
    g.prompt,
    g.caption,
    g.image_file
FROM generated_images g 
ORDER BY g.id ASC
"""


class GetAllPromptsAndCaptionsRow(pydantic.BaseModel):
    id: int
    prompt: str
    caption: str
    image_file: str


GET_IMAGE_FILE = """-- name: get_image_file \\:one
SELECT g.image_file
FROM generated_images g
WHERE g.id = :p1
"""


QUERY_CAPTION_EMBEDDINGS = """-- name: query_caption_embeddings \\:many
SELECT g.caption, g.prompt, g.image_file, e.caption_embedding
FROM embeddings e
JOIN generated_images g ON e.image_id = g.id
ORDER BY caption_embedding <=> :p1\\:\\:vector LIMIT :p2
"""


class QueryCaptionEmbeddingsRow(pydantic.BaseModel):
    caption: str
    prompt: str
    image_file: str
    caption_embedding: Optional[Any]


QUERY_PROMPT_EMBEDDINGS = """-- name: query_prompt_embeddings \\:many
SELECT g.prompt, g.caption, g.image_file, e.prompt_embedding
FROM embeddings e
JOIN generated_images g ON e.image_id = g.id
ORDER BY prompt_embedding <=> :p1\\:\\:vector LIMIT :p2
"""


class QueryPromptEmbeddingsRow(pydantic.BaseModel):
    prompt: str
    caption: str
    image_file: str
    prompt_embedding: Optional[Any]


STORE_EMBEDDINGS = """-- name: store_embeddings \\:exec
INSERT INTO embeddings (image_id, prompt_embedding, caption_embedding)
VALUES (:p1, :p2\\:\\:vector, :p3\\:\\:vector)
"""


UPDATE_IMAGE_LINK = """-- name: update_image_link \\:exec
UPDATE generated_images
SET image_file = :p2
WHERE id = :p1
"""


class AsyncQuerier:
    def __init__(self, conn: sqlalchemy.ext.asyncio.AsyncConnection):
        self._conn = conn

    async def create_generated_image(
        self, *, image_file: str, prompt: str, caption: str
    ) -> Optional[int]:
        row = (
            await self._conn.execute(
                sqlalchemy.text(CREATE_GENERATED_IMAGE),
                {"p1": image_file, "p2": prompt, "p3": caption},
            )
        ).first()
        if row is None:
            return None
        return row[0]

    async def get_all_caption_embeddings(
        self,
    ) -> AsyncIterator[GetAllCaptionEmbeddingsRow]:
        result = await self._conn.stream(sqlalchemy.text(GET_ALL_CAPTION_EMBEDDINGS))
        async for row in result:
            yield GetAllCaptionEmbeddingsRow(
                embedding=row[0],
                image_id=row[1],
            )

    async def get_all_captions(self) -> AsyncIterator[GetAllCaptionsRow]:
        result = await self._conn.stream(sqlalchemy.text(GET_ALL_CAPTIONS))
        async for row in result:
            yield GetAllCaptionsRow(
                id=row[0],
                caption=row[1],
                image_file=row[2],
            )

    async def get_all_prompt_embeddings(
        self,
    ) -> AsyncIterator[GetAllPromptEmbeddingsRow]:
        result = await self._conn.stream(sqlalchemy.text(GET_ALL_PROMPT_EMBEDDINGS))
        async for row in result:
            yield GetAllPromptEmbeddingsRow(
                embedding=row[0],
                image_id=row[1],
            )

    async def get_all_prompts(self) -> AsyncIterator[GetAllPromptsRow]:
        result = await self._conn.stream(sqlalchemy.text(GET_ALL_PROMPTS))
        async for row in result:
            yield GetAllPromptsRow(
                id=row[0],
                prompt=row[1],
                image_file=row[2],
            )

    async def get_all_prompts_and_captions(
        self,
    ) -> AsyncIterator[GetAllPromptsAndCaptionsRow]:
        result = await self._conn.stream(sqlalchemy.text(GET_ALL_PROMPTS_AND_CAPTIONS))
        async for row in result:
            yield GetAllPromptsAndCaptionsRow(
                id=row[0],
                prompt=row[1],
                caption=row[2],
                image_file=row[3],
            )

    async def get_image_file(self, *, id: int) -> Optional[str]:
        row = (
            await self._conn.execute(sqlalchemy.text(GET_IMAGE_FILE), {"p1": id})
        ).first()
        if row is None:
            return None
        return row[0]

    async def query_caption_embeddings(
        self, *, prompt: Optional[Any], num_results: int
    ) -> AsyncIterator[QueryCaptionEmbeddingsRow]:
        result = await self._conn.stream(
            sqlalchemy.text(QUERY_CAPTION_EMBEDDINGS), {"p1": prompt, "p2": num_results}
        )
        async for row in result:
            yield QueryCaptionEmbeddingsRow(
                caption=row[0],
                prompt=row[1],
                image_file=row[2],
                caption_embedding=row[3],
            )

    async def query_prompt_embeddings(
        self, *, prompt: Optional[Any], num_results: int
    ) -> AsyncIterator[QueryPromptEmbeddingsRow]:
        result = await self._conn.stream(
            sqlalchemy.text(QUERY_PROMPT_EMBEDDINGS), {"p1": prompt, "p2": num_results}
        )
        async for row in result:
            yield QueryPromptEmbeddingsRow(
                prompt=row[0],
                caption=row[1],
                image_file=row[2],
                prompt_embedding=row[3],
            )

    async def store_embeddings(
        self,
        *,
        image_id: int,
        prompt_embedding: Optional[Any],
        caption_embedding: Optional[Any],
    ) -> None:
        await self._conn.execute(
            sqlalchemy.text(STORE_EMBEDDINGS),
            {"p1": image_id, "p2": prompt_embedding, "p3": caption_embedding},
        )

    async def update_image_link(self, *, id: int, new_image_file: str) -> None:
        await self._conn.execute(
            sqlalchemy.text(UPDATE_IMAGE_LINK), {"p1": id, "p2": new_image_file}
        )
