#!/usr/bin/env python3
"""Print a report of books for a list of authors from the bookstore MongoDB database."""

import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Read Atlas credentials from the environment
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Author _id values to report on: author_002 and author_003 are from the
# loaded files, author_004 was added in Case Study 1 step 7
AUTHOR_IDS = ["author_002", "author_003", "author_004"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def print_report(authors, books, author_ids):
    """Print each author in author_ids with the title and year of their linked books.

    Args:
        1. authors: The pymongo collection holding author documents.
       2.  books: The pymongo collection holding book documents.
        3. author_ids: A list of author _id values to include in the report.
    """
    # Count how many of the requested authors exist in the collection
    query = {"_id": {"$in": author_ids}}
    print(f"Authors: {authors.count_documents(query)}")

    for author in authors.find(query).sort("_id"):
        print(f"\n{author['name']}")
        # Find every book whose author_ids list contains this author's _id
        for book in books.find({"author_ids": author["_id"]}).sort("published_year"):
            print(f"  {book['title']} ({book['published_year']})")


def main():
    """Connect to MongoDB Atlas, print the bookstore report, and close the client."""
    client = None
    try:
        # Connect to Atlas with the credentials from the environment
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        client.admin.command("ping")
        logger.info("Connected to MongoDB Atlas")

        # Select the database and collections created in Case Study 1
        db = client["bookstore"]
        print_report(db["authors"], db["books"], AUTHOR_IDS)
    except PyMongoError as e:
        logger.error("MongoDB error: %s", e)
    finally:
        # Always close the connection
        if client is not None:
            client.close()
            logger.info("Connection closed")


if __name__ == "__main__":
    main()
