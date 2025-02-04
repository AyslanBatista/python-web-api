from blog.database import mongo
import pymongo
from datetime import datetime
from blog.utils import slugify


def get_all_posts(published: bool = True):
    posts = mongo.db.posts.find({"published": published})
    return posts.sort("date", pymongo.DESCENDING)


def get_post_by_slug(slug: str) -> dict:
    post = mongo.db.posts.find_one({"slug": slug})
    return post


def update_post_by_slug(slug: str, data: dict) -> dict:
    update_data = data.copy()

    if "title" in update_data:
        new_slug = slugify(update_data["title"])

        if mongo.db.posts.find_one({"slug": new_slug}):
            raise ValueError("Já existe um post com esse título")

        update_data["slug"] = new_slug

    return mongo.db.posts.find_one_and_update(
        {"slug": slug}, {"$set": update_data}, return_document=True
    )


def delete_post_by_slug(slug:str) -> bool:
    mongo.db.posts.delete_one({"slug": slug})
        

def new_post(
    title: str, content: str, username: str, published: bool = True
) -> str:
    slug = slugify(title)

    exist_post = get_post_by_slug(slug)

    if exist_post:
        raise ValueError("There is already a post with that title.")

    new = mongo.db.posts.insert_one(
        {
            "title": title,
            "content": content,
            "username": username,
            "published": published,
            "slug": slug,
            "date": datetime.now(),
        }
    )
    return slug
