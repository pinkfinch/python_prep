# images = [
#     {"id": 1, "project_id": 10, "url_path": "abc/1.png", "active": True},
#     {"id": 2, "project_id": 10, "url_path": "abc/2.png", "active": False},
#     {"id": 3, "project_id": 22, "url_path": "xyz/3.png", "active": True},
#     {"id": 4, "project_id": 10, "url_path": "abc/4.png", "active": True},
# ]
# called like this:
# list_active_images(images, 10, "https://cdn.example.com/")
#
# Expected output:
#
# [
#     {"id": 1, "url": "https://cdn.example.com/abc/1.png"},
#     {"id": 4, "url": "https://cdn.example.com/abc/4.png"},
# ]

import requests
import logging
from datetime import datetime
import re

logger = logging.getLogger("weather")

def list_active_images(images, project_id, base_url):

    if not images:
        raise ValueError("Invalid images object passed in")
    if not base_url:
        raise ValueError("Invalid baseurl")

    if not isinstance(images, list):
        raise TypeError("Invalid images type")

    if not isinstance(base_url, str):
        raise TypeError("Invalid base_url type")

    active_images = []
    for image in images:
        img_id = image.get("id")
        url_path = image.get("url_path", "")
        active_flag = image.get("active", False)
        proj_id = image.get("project_id")
        if project_id != proj_id: continue

        if active_flag and url_path:
            full_url = base_url.rstrip("/") + "/" + url_path.lstrip("/")
            active_images.append({"id": img_id, "url": full_url})

    return active_images


# images = [
#     {"id": 1, "project_id": 10, "url_path": "abc/1.png", "active": True, "size_kb": 120},
#     {"id": 2, "project_id": 10, "url_path": "abc/2.png", "active": False, "size_kb": 80},
#     {"id": 3, "project_id": 22, "url_path": "xyz/3.png", "active": True, "size_kb": 300},
#     {"id": 4, "project_id": 10, "url_path": "abc/4.png", "active": True, "size_kb": 200},
# ]

# Write a function:
# def get_active_images_summary(images, project_id, base_url):
#     ...
# It should:
#
# Return only active images for the given project_id.
# For each image, construct the full URL by combining base_url + url_path.
# Return a summary dictionary containing:
#
# {
#     "total_images": <number of active images>,
#     "total_size_kb": <sum of size_kb>,
#     "images": [
#         {"id": ..., "url": ...},
#         ...
#     ]
# }
# Handle missing fields gracefully (e.g., missing url_path or size_kb).
#
# ex:
# get_active_images_summary(images, 10, "https://cdn.example.com/")
# {
#     "total_images": 2,
#     "total_size_kb": 320,
#     "images": [
#         {"id": 1, "url": "https://cdn.example.com/abc/1.png"},
#         {"id": 4, "url": "https://cdn.example.com/abc/4.png"}
#     ]
# }


def get_active_images_summary(images, project_id, base_url):
    if not images:
        raise ValueError("No images sent in")
    if not base_url:
        raise ValueError("No base_url sent in")
    if not isinstance(images, list):
        raise TypeError("Images needs to be a list")
    if not isinstance(base_url, str):
        raise TypeError("Base url needs to be sent in")

    active_images = []
    total_size = 0
    for image in images:
        img_id = image.get("id")
        proj_id = image.get("project_id")
        url_path = image.get("url_path")
        active_flag = image.get("active", False)
        size = image.get("size_kb", 0)

        if not img_id or proj_id != project_id or not url_path or not active_flag:
            continue
        final_url = base_url.rstrip("/") + "/" + url_path.lstrip("/")
        active_images.append({"id":img_id, "url":final_url })
        total_size += size


    return  {
        "total_images": len(active_images),
        "total_size_kb": total_size,
        "images" : active_images
    }


def get_active_images_summary_large(images_iter, project_id, base_url):
    """
    Scalable version of get_active_images_summary.
    Accepts any iterable (list, generator, DB cursor) of image dicts.
    Returns a summary dict with total images, total size, and images list.
    """
    if not base_url:
        raise ValueError("No base_url provided")
    if not isinstance(base_url, str):
        raise TypeError("base_url must be a string")

    base_url = base_url.rstrip("/")
    total_size = 0
    active_images = []

    for img in images_iter:
        img_id = img.get("id")
        proj_id = img.get("project_id")
        url_path = img.get("url_path")
        active_flag = img.get("active", False)
        size = img.get("size_kb", 0)

        # Skip invalid or non-matching images
        if img_id is None or proj_id != project_id or not url_path or not active_flag:
            continue

        # Construct full URL
        full_url = base_url + "/" + url_path.lstrip("/")

        # Append image summary
        active_images.append({"id": img_id, "url": full_url})

        # Increment total size
        total_size += size

    return {
        "total_images": len(active_images),
        "total_size_kb": total_size,
        "images": active_images
    }

# Given two API responses containing image metadata, write a function to merge them, remove
# duplicates by id, and sort by id.

def merge_api_responses(image_list1, image_list2):
    image_dict = {}
    for img in image_list1 + image_list2:
        img_id = img.get("id")
        if img_id is not None and img_id not in image_dict:
            image_dict[img_id] = img

    images = image_dict.values()
    return sorted(images, key=lambda image:image.get("id"))

# call weather api and print the response for the last 3 days of weather in a particular location
{'latitude': 40.710335, 'longitude': -73.99309, 'generationtime_ms': 0.047206878662109375,
 'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 32.0,
 'hourly_units': {'time': 'iso8601', 'temperature_2m': '°C'},
 'hourly': {
     'time': ['2025-12-23T00:00', '2025-12-23T01:00', '2025-12-23T02:00', '2025-12-23T03:00', '2025-12-23T04:00', '2025-12-23T05:00', '2025-12-23T06:00', '2025-12-23T07:00', '2025-12-23T08:00', '2025-12-23T09:00', '2025-12-23T10:00', '2025-12-23T11:00', '2025-12-23T12:00', '2025-12-23T13:00', '2025-12-23T14:00', '2025-12-23T15:00', '2025-12-23T16:00', '2025-12-23T17:00', '2025-12-23T18:00', '2025-12-23T19:00', '2025-12-23T20:00', '2025-12-23T21:00', '2025-12-23T22:00', '2025-12-23T23:00', '2025-12-24T00:00', '2025-12-24T01:00', '2025-12-24T02:00', '2025-12-24T03:00', '2025-12-24T04:00', '2025-12-24T05:00', '2025-12-24T06:00', '2025-12-24T07:00', '2025-12-24T08:00', '2025-12-24T09:00', '2025-12-24T10:00', '2025-12-24T11:00', '2025-12-24T12:00', '2025-12-24T13:00', '2025-12-24T14:00', '2025-12-24T15:00', '2025-12-24T16:00', '2025-12-24T17:00', '2025-12-24T18:00', '2025-12-24T19:00', '2025-12-24T20:00', '2025-12-24T21:00', '2025-12-24T22:00', '2025-12-24T23:00', '2025-12-25T00:00', '2025-12-25T01:00', '2025-12-25T02:00', '2025-12-25T03:00', '2025-12-25T04:00', '2025-12-25T05:00', '2025-12-25T06:00', '2025-12-25T07:00', '2025-12-25T08:00', '2025-12-25T09:00', '2025-12-25T10:00', '2025-12-25T11:00', '2025-12-25T12:00', '2025-12-25T13:00', '2025-12-25T14:00', '2025-12-25T15:00', '2025-12-25T16:00', '2025-12-25T17:00', '2025-12-25T18:00', '2025-12-25T19:00', '2025-12-25T20:00', '2025-12-25T21:00', '2025-12-25T22:00', '2025-12-25T23:00', '2025-12-26T00:00', '2025-12-26T01:00', '2025-12-26T02:00', '2025-12-26T03:00', '2025-12-26T04:00', '2025-12-26T05:00', '2025-12-26T06:00', '2025-12-26T07:00', '2025-12-26T08:00', '2025-12-26T09:00', '2025-12-26T10:00', '2025-12-26T11:00', '2025-12-26T12:00', '2025-12-26T13:00', '2025-12-26T14:00', '2025-12-26T15:00', '2025-12-26T16:00', '2025-12-26T17:00', '2025-12-26T18:00', '2025-12-26T19:00', '2025-12-26T20:00', '2025-12-26T21:00', '2025-12-26T22:00', '2025-12-26T23:00', '2025-12-27T00:00', '2025-12-27T01:00', '2025-12-27T02:00', '2025-12-27T03:00', '2025-12-27T04:00', '2025-12-27T05:00', '2025-12-27T06:00', '2025-12-27T07:00', '2025-12-27T08:00', '2025-12-27T09:00', '2025-12-27T10:00', '2025-12-27T11:00', '2025-12-27T12:00', '2025-12-27T13:00', '2025-12-27T14:00', '2025-12-27T15:00', '2025-12-27T16:00', '2025-12-27T17:00', '2025-12-27T18:00', '2025-12-27T19:00', '2025-12-27T20:00', '2025-12-27T21:00', '2025-12-27T22:00', '2025-12-27T23:00', '2025-12-28T00:00', '2025-12-28T01:00', '2025-12-28T02:00', '2025-12-28T03:00', '2025-12-28T04:00', '2025-12-28T05:00', '2025-12-28T06:00', '2025-12-28T07:00', '2025-12-28T08:00', '2025-12-28T09:00', '2025-12-28T10:00', '2025-12-28T11:00', '2025-12-28T12:00', '2025-12-28T13:00', '2025-12-28T14:00', '2025-12-28T15:00', '2025-12-28T16:00', '2025-12-28T17:00', '2025-12-28T18:00', '2025-12-28T19:00', '2025-12-28T20:00', '2025-12-28T21:00', '2025-12-28T22:00', '2025-12-28T23:00', '2025-12-29T00:00', '2025-12-29T01:00', '2025-12-29T02:00', '2025-12-29T03:00', '2025-12-29T04:00', '2025-12-29T05:00', '2025-12-29T06:00', '2025-12-29T07:00', '2025-12-29T08:00', '2025-12-29T09:00', '2025-12-29T10:00', '2025-12-29T11:00', '2025-12-29T12:00', '2025-12-29T13:00', '2025-12-29T14:00', '2025-12-29T15:00', '2025-12-29T16:00', '2025-12-29T17:00', '2025-12-29T18:00', '2025-12-29T19:00', '2025-12-29T20:00', '2025-12-29T21:00', '2025-12-29T22:00', '2025-12-29T23:00'],
     'temperature_2m': [1.6, 1.5, 1.7, 1.7, 1.3, 1.5, 1.8, 2.3, 2.1, 2.5, 2.2, 2.0, 1.3, 1.4, 1.3, 1.0, 1.4, 2.0, 2.7, 3.6, 3.4, 3.4, 3.1, 2.9, 2.8, 2.7, 2.6, 2.4, 2.0, 2.2, 2.4, 2.1, 2.2, 2.5, 2.1, 1.7, 1.4, 1.7, 2.9, 3.9, 4.3, 4.4, 4.3, 4.1, 3.8, 2.4, 0.6, -0.4, -0.5, -0.5, -0.6, -0.6, -0.6, -0.7, -0.9, -1.0, -1.0, -1.0, -0.8, -0.8, -0.4, 0.1, 1.0, 1.4, 1.4, 2.3, 2.4, 2.6, 4.3, 4.4, 3.5, 2.9, 1.7, 0.2, -0.8, -1.4, -1.8, -2.1, -2.5, -2.9, -3.2, -3.5, -3.6, -3.4, -3.3, -3.3, -3.6, -3.6, -3.1, -2.7, -2.6, -2.4, -2.4, -2.5, -2.4, -2.2, -1.9, -1.6, -3.3, -3.1, -2.9, -2.7, -2.4, -2.6, -2.6, -2.7, -2.5, -2.6, -2.7, -2.8, -2.3, -1.4, -1.0, -0.9, -0.8, -0.7, -0.7, -1.0, -2.9, -3.5, -3.7, -4.0, -4.2, -4.0, -4.2, -4.2, -4.0, -3.1, -2.5, -2.2, -1.8, -1.5, -1.4, -0.7, 0.1, 0.7, 1.0, 1.1, 1.4, 2.1, 3.0, 3.6, 3.6, 3.4, 3.1, 3.0, 2.9, 2.9, 2.9, 2.9, 2.9, 3.0, 3.1, 2.7, 1.3, -0.6, -2.1, -2.7, -3.0, -3.1, -3.1, -3.0, -3.0, -3.1, -3.4, -3.6, -4.0, -4.3]}}

def fetch_weather_details(lat, long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": "temperature_2m",
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            hourly_data = data.get('hourly', {})
            time = hourly_data.get('time')
            temp = hourly_data.get('temperature_2m')

            zipped_data = zip(time, temp)
            format = '%Y-%m-%dT%H:%M'
            for tme, tmp in zipped_data:
                print(f"temperature at {datetime.strptime(tme, format)} is {tmp}")

    except requests.Timeout as t:
        logger.error("Timeout exception", exc_info=True)
    except requests.RequestException as e:
        logger.error("Request exception", exc_info=True)


fetch_weather_details(40.7128, -74.0060)

# payload = {
#     "email": "user@example.com",
#     "age": 25
# }
# errors payload:
# {
#     "valid": False,
#     "errors": [
#         "invalid email",
#         "age must be >= 18"
#     ]
# }
# Validate a request payload with required fields email and age. Return a structured error dictionary if invalid.

def validate_payload(payload):

    pattern = r'^[a-zA-Z0-9.-%+_]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    email = payload.get("email")
    age = payload.get("age")
    errors = []
    if email:
        if not re.match(pattern, email):
            errors.append("Invalid email")
    else:
        errors.append("No email address provided")

    if age is None:
        errors.append("No age provided")
    else:
        if age < 18:
            errors.append("age must be >= 18")


    return {
        "valid": len(errors) == 0,
        "errors": errors
    }











