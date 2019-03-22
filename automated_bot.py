"""NOTE: the script does not provide any error handling and it will fail
un-gracefully after a single exception. E.g. registering two users with same 'jack342' username by chance will
kill the script midway."""


import argparse
import configparser
import requests
import random
import string
import logging
from itertools import chain


from faker import Faker


URL_BASE = "http://localhost:8000/api/"


class SimpleApiClient:
    def __init__(self, url_base=URL_BASE):
        self.url_base = url_base

    def _authorization_header(self, jwt_token):
        return string.Template("Bearer $token").substitute(token=jwt_token)

    def register_user(self, user_registration_data):
        logging.info("Registering %s", user_registration_data["username"])
        response = requests.post(
            self.url_base + "auth/register/", json=user_registration_data
        )
        if response.status_code == 201:
            return response.json()
        logging.error(
            "Could not register %s, the server responded with %i",
            user_registration_data["username"],
            response.status_code,
        )
        logging.error(response.json())
        raise Exception("Registration failed for some reason")

    def log_in(self, username, password):
        logging.info("Logging in %s", username)
        response = requests.post(
            self.url_base + "auth/token/",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            return response.json()
        logging.error(
            "Could not log in %s, the server responded with %i",
            username,
            response.status_code,
        )
        logging.error(response.json())
        raise Exception("Login failed for some reason")

    def create_post(self, title, text, jwt_token):
        logging.info('Creating post "%s"', title)
        response = requests.post(
            self.url_base + "posts/",
            json={"title": title, "text": text},
            headers={"Authorization": self._authorization_header(jwt_token)},
        )
        if response.status_code == 201:
            return response.json()
        logging.error(
            'Could not create post "%s", the server responded with %i',
            title,
            response.status_code,
        )
        logging.error(response.json())
        raise Exception("Creating post failed for some reason")

    def like_post(self, post_id_to_like, jwt_token):
        logging.info("Like post #%i", post_id_to_like)
        relative_path = string.Template("posts/$post_id/like/").substitute(
            post_id=post_id_to_like
        )
        response = requests.post(
            self.url_base + relative_path,
            headers={"Authorization": self._authorization_header(jwt_token)},
        )
        if response.status_code == 200:
            return
        logging.error(
            "Could not like post #%i, the server responded with %i",
            post_id_to_like,
            response.status_code,
        )
        raise Exception("Could not like the post for some reason")


def _random_string(len, characters):
    return "".join(random.choice(characters) for _ in range(len))


def _random_alphanumeric_string(len=10):
    return _random_string(len, string.ascii_letters + string.digits)


def _random_numeric_string(len=3):
    return _random_string(len, string.digits)


def _generate_user_data(number_of_users, faker):
    fake_username = lambda: faker.name().split(" ")[0].lower() + _random_numeric_string(
        len=4
    )
    fake_usernames = [fake_username() for _ in range(number_of_users)]
    return [
        {
            "username": fake_username,
            "password": _random_alphanumeric_string(),
            "email": string.Template("$username@starnavi.io").substitute(
                username=fake_username
            ),
        }
        for fake_username in fake_usernames
    ]


def _log_users_in(registered_users, simple_api_client):
    for registered_user in registered_users:
        token_pair = simple_api_client.log_in(
            registered_user["user_registration_data"]["username"],
            registered_user["user_registration_data"]["password"],
        )
        registered_user["token_pair"] = token_pair


def _generate_posts(registered_users, max_posts_per_user, faker):
    for registered_user in registered_users:
        registered_user["posts"] = [
            {
                "data": {
                    "title": " ".join(faker.text().split()[:3]),
                    "text": faker.text(),
                }
            }
            for _ in range(max_posts_per_user)
        ]


def _upload_posts(registered_users, simple_api_client):
    for registered_user in registered_users:
        registered_user["posts"] = [
            {
                "id": simple_api_client.create_post(
                    post["data"]["title"],
                    post["data"]["text"],
                    registered_user["token_pair"]["access"],
                )["id"],
                "data": post["data"],
            }
            for post in registered_user["posts"]
        ]


def _all_post_ids(registered_users):
    return list(
        chain(
            *[
                [post["id"] for post in registered_user["posts"]]
                for registered_user in registered_users
            ]
        )
    )


def _like_posts(registered_users, max_likes_per_user, simple_api_client):
    all_post_ids = _all_post_ids(registered_users)
    for registered_user in registered_users:
        post_ids_to_like = random.sample(population=all_post_ids, k=max_likes_per_user)
        for post_id_to_like in post_ids_to_like:
            simple_api_client.like_post(
                post_id_to_like, registered_user["token_pair"]["access"]
            )


def run_automated_bot(
    faker, simple_api_client, number_of_users, max_posts_per_user, max_likes_per_user
):
    user_registration_data_list = _generate_user_data(number_of_users, faker)
    registered_users = [
        {
            "user_id": simple_api_client.register_user(user_registration_data)["id"],
            "user_registration_data": user_registration_data,
        }
        for user_registration_data in user_registration_data_list
    ]
    _log_users_in(registered_users, simple_api_client)
    _generate_posts(registered_users, max_posts_per_user, faker)
    _upload_posts(registered_users, simple_api_client)
    _like_posts(registered_users, max_likes_per_user, simple_api_client)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Exersize medium REST API.")
    parser.add_argument("-cfg", "--config", default="medium_bot.sample.ini")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    number_of_users = int(config.get("Basic Params", "number_of_users"))
    max_posts_per_user = int(config.get("Basic Params", "max_posts_per_user"))
    max_likes_per_user = int(config.get("Basic Params", "max_likes_per_user"))
    logging.info(
        "Running the bot for the following configuration: users - %i, posts per user - %i, likes per user - %i",
        number_of_users,
        max_posts_per_user,
        max_likes_per_user,
    )

    run_automated_bot(
        Faker(),
        SimpleApiClient(),
        number_of_users,
        max_posts_per_user,
        max_likes_per_user,
    )

    logging.info("Finished running automated bot")


if __name__ == "__main__":
    main()
