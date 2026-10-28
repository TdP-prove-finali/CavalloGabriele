from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import get_type_hints
from bson import ObjectId
from dao.mongodb_connector import MongoDBConnector
from model.sim_output import SimulationOutput
from dataclasses import is_dataclass, fields

class SimulationDAO:

    @staticmethod
    def save_simulation(sim_output: SimulationOutput):
        """
        Salva gli output della simulazione sul db
        :param sim_output:
        :return:
        """
        database = MongoDBConnector.get_database()
        collection = database["simulations"]
        document = SimulationDAO.to_mongo_dict(sim_output)
        document["_id"] = sim_output.global_parameters.sim_id
        collection.replace_one(
            {"_id": document["_id"]},
            document,
            upsert=True
        )

    @staticmethod
    def create_sim_id():
        return str(ObjectId())

    @staticmethod
    def to_mongo_dict(obj):
        active = {}
        SKIP = object()

        def serialize(value, path="root"):
            # Tipi primitivi
            if value is None or type(value) in (str, int, float, bool):
                return value

            # Tipi BSON compatibili
            if isinstance(value, (datetime, ObjectId)):
                return value

            if isinstance(value, (date, Decimal)):
                return str(value)

            # Enum
            if isinstance(value, Enum):
                return serialize(value.value, path)

            # Riferimenti circolari: ignora
            obj_id = id(value)

            if obj_id in active:
                return SKIP

            active[obj_id] = path

            try:
                # Dataclass
                if is_dataclass(value) and not isinstance(value, type):
                    result = {}

                    for field in fields(value):
                        serialized = serialize(
                            getattr(value, field.name),
                            f"{path}.{field.name}"
                        )
                        if serialized is not SKIP:
                            result[field.name] = serialized

                    return result

                # Dizionari
                if isinstance(value, dict):
                    result = {}

                    for key, item in value.items():
                        if not isinstance(key, str):
                            continue

                        serialized = serialize(item, f"{path}.{key}")
                        if serialized is not SKIP:
                            result[key] = serialized

                    return result

                # Liste e tuple
                if isinstance(value, (list, tuple)):
                    result = []

                    for i, item in enumerate(value):
                        serialized = serialize(item, f"{path}[{i}]")
                        if serialized is not SKIP:
                            result.append(serialized)

                    return result

                # Classi Python tradizionali
                if hasattr(value, "__dict__") and not isinstance(value, type):
                    result = {}

                    for key, item in vars(value).items():
                        serialized = serialize(item, f"{path}.{key}")
                        if serialized is not SKIP:
                            result[key] = serialized

                    return result

                # Tipo non supportato: ignora
                return SKIP

            finally:
                active.pop(obj_id, None)

        result = serialize(obj)

        return {} if result is SKIP else result

    @staticmethod
    def from_mongo_dict(data, cls):
        if data is None:
            return None

        if isinstance(data, list):
            return [
                SimulationDAO.from_mongo_dict(item, cls)
                for item in data
            ]

        if cls in (int, float, str, bool):
            return cls(data)

        if not isinstance(data, dict):
            return data

        if is_dataclass(cls):
            type_hints = get_type_hints(cls)

            kwargs = {
                field.name: SimulationDAO.from_mongo_dict(
                    data[field.name],
                    type_hints.get(field.name, field.type)
                )
                for field in fields(cls)
                if field.name in data
            }

            return cls(**kwargs)

        # Classi Python tradizionali
        obj = cls.__new__(cls)

        for key, value in data.items():
            setattr(obj, key, value)

        return obj