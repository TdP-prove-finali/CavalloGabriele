import configparser
from pymongo import MongoClient
from pymongo.database import Database

class MongoDBConnector:
    _client: MongoClient = None
    _database: Database = None

    def __init__(self):
        raise NotImplementedError("This is a singleton")


    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._client is None:
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

            cls._client = MongoClient(
                host=host,
                port=port,
                username=username,
                password=password,
                maxPoolSize=max_pool_size,
                authSource=database_name
            )

            cls._database = cls._client[database_name]

        return cls._client

    @classmethod
    def get_database(cls) -> Database:
        if cls._database is None:
            MongoDBConnector.get_client()
        return cls._database

    @classmethod
    def ping(cls) -> bool:
        cls._client.admin.command("ping")
        return True

    @classmethod
    def close(cls) -> None:
        cls._client.close()