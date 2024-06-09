#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : __main__.py
# Author             : QU35T-code (Exegol)
# Date created       : 07 jun 2024

import requests
import sqlite3
import json
import tweepy
import os
import sys

from typing import List, Dict, Any

DB_FILE = '/home/exegolx/exegolx.db'
URL = 'https://hub.docker.com/v2/repositories/nwodtuhs/exegol/tags?page=1&ordering=last_updated'

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

client = tweepy.Client(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)


def fetch_docker_tags(url: str) -> Dict[str, Any]:
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Failed to fetch Docker tags: {response.status_code}")


def create_db() -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS docker_images
                 (id INTEGER PRIMARY KEY, image_id INT, image_name TEXT, size INT, last_updated TEXT)''')
    conn.commit()
    conn.close()


def insert_image(image_id: int, image_name: str, size: int, last_updated: str) -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO docker_images (image_id, image_name, size, last_updated) VALUES (?, ?, ?, ?)',
              (image_id, image_name, size, last_updated))
    conn.commit()
    conn.close()


def update_last_pushed(image_id: int, last_updated: str) -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE docker_images SET last_updated = ? WHERE image_id = ?', (last_updated, image_id))
    conn.commit()
    conn.close()


def check_and_notify(tags: List[Dict[str, Any]]) -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for tag in tags:
        c.execute('SELECT last_updated FROM docker_images WHERE image_id = ?', (tag['id'],))
        row = c.fetchone()
        if row:
            last_updated = row[0]
            if last_updated != tag['last_updated']:
                print(f"New push detected for image {tag['name']}, last pushed: {tag['last_updated']}")
                image_name = tag['name']
                size = round(tag['full_size'] / (1024 ** 3) * 2.56, 2)
                message = (
                    f"🚀 A new version of the {image_name} image (~{size}GB) is now available on #Exegol. "
                    f"If you use it, don't forget to update it using the command : "
                    f"exegol update {image_name} !\n\nhttps://github.com/ThePorgs/Exegol"
                )
                client.create_tweet(text=message)
                print("A new tweet has been sent")
                update_last_pushed(tag['id'], tag['last_updated'])
        else:
            insert_image(tag['id'], tag['name'], tag['full_size'], tag['last_updated'])
    conn.close()


def main() -> None:
    create_db()
    tags_data = fetch_docker_tags(URL)
    tags = tags_data.get('results', [])
    check_and_notify(tags)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("Proof of work")
        exit(0)
    main()
