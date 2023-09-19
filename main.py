from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import sqlite3
import base64


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/images")
async def get_image_set():
    conn = sqlite3.connect("my_images.db")
    cursor = conn.execute("SELECT COUNT(*) from images")
    total_count = cursor.fetchone()[0]
    random_num_1 = random.randint(1, total_count)
    random_num_2 = random.randint(1, total_count)
    while (random_num_2 == random_num_1):
        random_num_2 = random.randint(1, total_count)

    cursor_img_1 = conn.execute(
        "SELECT image_name, image_data, score FROM images WHERE id = ?", (random_num_1,))
    image_1_name, image_1_data, image_1_score = cursor_img_1.fetchone()
    image_1_data_base64 = base64.b64encode(image_1_data).decode("utf-8")

    cursor_img_2 = conn.execute(
        "SELECT image_name, image_data, score FROM images WHERE id = ?", (random_num_2,))
    image_2_name, image_2_data, image_2_score = cursor_img_2.fetchone()
    image_2_data_base64 = base64.b64encode(image_2_data).decode("utf-8")

    conn.close()

    return {
        "image_1": {
            "name": image_1_name,
            "image_data": image_1_data_base64,
            "score": image_1_score
        },
        "image_2": {
            "name": image_2_name,
            "image_data": image_2_data_base64,
            "score": image_2_score
        }
    }


class UpdateImageScore(BaseModel):
    image_id_1: int
    image_id_2: int
    image_score_1: float
    image_score_2: float


@app.post("/api/update_scores")
async def update_scores(data: UpdateImageScore):
    conn = sqlite3.connect("my_images.db")
    cursor = conn.cursor()

    # update score for image 1
    cursor.execute(
        "UPDATE images SET score = ? WHERE id = ?",
        (data.image_score_1, data.image_id_1)
    )
    conn.commit()

    # update score for image 2
    cursor.execute(
        "UPDATE images SET score = ? WHERE id = ?",
        (data.image_score_2, data.image_id_2)
    )
    conn.commit()

    conn.close()

    return {"message": "Scores updated successfully"}
