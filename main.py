from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import sqlite3
import base64
import math


def get_probability(rating_1, rating_2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating_1 - rating_2) / 400))


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
    winner_flag: int


@app.post("/api/update_scores")
async def update_scores(data: UpdateImageScore):
    """
    sample JSON payload
    winner flag : 1 when Image 1 wins else 0

    {
    "image_id_1": 1,
    "image_id_2": 2,
    "image_score_1": 1000,
    "image_score_2": 1200,
    "winner_flag": 1
    }

    """
    conn = sqlite3.connect("my_images.db")
    cursor = conn.cursor()

    # To calculate the Winning Probability of Image 1
    probab_image_1 = get_probability(data.image_score_1, data.image_score_2)

    # To calculate the Winning Probability of Image 2
    probab_image_2 = get_probability(data.image_score_2, data.image_score_1)

    K = 32

    if (data.winner_flag == 1):
        image_1_new_score = data.image_score_1 + K * (1 - probab_image_1)
        image_2_new_score = data.image_score_2 + K * (0 - probab_image_2)
    else:
        image_1_new_score = data.image_score_1 + K * (0 - probab_image_1)
        image_2_new_score = data.image_score_2 + K * (1 - probab_image_2)

    # update score for image 1
    cursor.execute(
        "UPDATE images SET score = ? WHERE id = ?",
        (round(image_1_new_score, 2), data.image_id_1)
    )
    conn.commit()

    # update score for image 2
    cursor.execute(
        "UPDATE images SET score = ? WHERE id = ?",
        (round(image_2_new_score, 2), data.image_id_2)
    )
    conn.commit()

    conn.close()

    return {"message": "Scores updated successfully"}
