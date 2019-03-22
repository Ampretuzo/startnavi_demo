import argparse
import configparser
import requests


URL_BASE = "http://localhost:8000/api/"


def run_automated_bot(number_of_users, max_posts_per_user, max_likes_per_user):
    # resp = requests.post(URL_BASE + 'auth/register/', json={
    #     'username': 'uname',
    #     'email': 'uname@domain.com',
    #     'password': 'uname1234'
    # })
    # print(resp.json())
    pass


def main():
    parser = argparse.ArgumentParser(description="Exersize medium REST API.")
    parser.add_argument("-cfg", "--config", default="medium_bot.sample.ini")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    number_of_users = int(config.get("Basic Params", "number_of_users"))
    max_posts_per_user = int(config.get("Basic Params", "max_posts_per_user"))
    max_likes_per_user = int(config.get("Basic Params", "max_likes_per_user"))

    run_automated_bot(number_of_users, max_posts_per_user, max_likes_per_user)


if __name__ == "__main__":
    main()
