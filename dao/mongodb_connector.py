import configparser
from pymongo import MongoClient
from pymongo.database import Database

class MongoDBConnector:
    def __init__(self):
        config = configparser.ConfigParser()

        if not config.read("../config/db.ini"):
            raise FileNotFoundError(
                f"Database configuration file not found"
            )

        mongodb_config = config["mongodb"]

        host = mongodb_config.get("host", "localhost")
        port = mongodb_config.getint("port", 27017)
        database_name = mongodb_config["database"]
        username = mongodb_config.get("username") or None
        password = mongodb_config.get("password") or None

        max_pool_size = mongodb_config.getint(
            "max_pool_size",
            20,
        )

        self._client = MongoClient(
            host=host,
            port=port,
            username=username,
            password=password,
            maxPoolSize=max_pool_size,
            authSource=database_name
        )

        self._database = self._client[database_name]

    @property
    def database(self) -> Database:
        return self._database

    def ping(self) -> bool:
        self._client.admin.command("ping")
        return True

    def close(self) -> None:
        self._client.close()