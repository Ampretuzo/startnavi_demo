import argparse
import configparser
import requests
import random
import string

from faker import Faker


URL_BASE = "http://localhost:8000/api/"


class SimpleApiClient:
    def __init__(self, url_base=URL_BASE):
        self.url_base = url_base

    def register_user(self, user_registration_data):
        response = requests.post(
            URL_BASE + "auth/register/", json=user_registration_data
        )
        if response.status_code == 201:
            return response.json()
        raise Exception("Registration failed for some reason")

    def log_in(self, username, password):
        response = requests.post(
            URL_BASE + "auth/token/", json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        raise Exception("Login failed for some reason")


def _random_alphanumeric_string(len=10):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(len))


def _random_numeric_string(len=3):
    characters = string.digits
    return "".join(random.choice(characters) for _ in range(len))


def _generate_user_data(number_of_users, faker):
    fake_username = lambda: faker.name().split(" ")[0].lower() + _random_numeric_string(
        len=2
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


def run_automated_bot(faker, number_of_users, max_posts_per_user, max_likes_per_user):
    user_registration_data_list = _generate_user_data(number_of_users, faker)
    simple_api_client = SimpleApiClient()
    registered_users = [
        {
            "user_id": simple_api_client.register_user(user_registration_data)["id"],
            "user_registration_data": user_registration_data,
        }
        for user_registration_data in user_registration_data_list
    ]
    _log_users_in(registered_users, simple_api_client)


def main():
    parser = argparse.ArgumentParser(description="Exersize medium REST API.")
    parser.add_argument("-cfg", "--config", default="medium_bot.sample.ini")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    number_of_users = int(config.get("Basic Params", "number_of_users"))
    max_posts_per_user = int(config.get("Basic Params", "max_posts_per_user"))
    max_likes_per_user = int(config.get("Basic Params", "max_likes_per_user"))

    run_automated_bot(Faker(), number_of_users, max_posts_per_user, max_likes_per_user)


if __name__ == "__main__":
    main()
