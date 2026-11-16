import math
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import get_type_hints, Mapping

import numpy as np
from bson import ObjectId, Decimal128
from dao.mongodb_connector import MongoDBConnector
from model.balance_snap import BalanceSnaphot
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
        """
        Serializza le informazioni della simulazione in modo ricorsivo.
        :param obj: Dati da serializzare
        :return:
        """
        active = {}

        def serialize(value, path="root"):

            # -------------------------------------------------
            # 1. Valori nulli
            # -------------------------------------------------
            if value is None:
                return None

            # -------------------------------------------------
            # 2. Tipi primitivi Python
            # -------------------------------------------------
            if isinstance(value, (str, bool, int, float)):
                if isinstance(value, float) and not math.isfinite(value):
                    raise ValueError(
                        f"Valore numerico non finito in {path}: {value}"
                    )

                return value

            # -------------------------------------------------
            # 3. Tipi NumPy / SciPy
            # -------------------------------------------------
            if isinstance(value, np.generic):
                return serialize(value.item(), path)

            if isinstance(value, np.ndarray):
                return serialize(value.tolist(), path)

            # -------------------------------------------------
            # 4. BalanceSnaphot
            # -------------------------------------------------
            if isinstance(value, BalanceSnaphot):
                sp, ce = value.serialize()

                return serialize(
                    {
                        "conto_economico": ce,
                        "stato_patrimoniale": sp
                    },
                    path
                )

            # -------------------------------------------------
            # 5. Tipi BSON compatibili
            # -------------------------------------------------
            if isinstance(value, (datetime, ObjectId, Decimal128)):
                return value

            # -------------------------------------------------
            # 6. Date e Decimal
            # -------------------------------------------------
            if isinstance(value, date):
                return value.isoformat()

            if isinstance(value, Decimal):
                if not value.is_finite():
                    raise ValueError(
                        f"Decimal non finito in {path}: {value}"
                    )

                return str(value)

            # -------------------------------------------------
            # 7. Enum
            # -------------------------------------------------
            if isinstance(value, Enum):
                return serialize(value.value, path)

            # -------------------------------------------------
            # 8. Rilevamento riferimenti circolari
            # -------------------------------------------------
            obj_id = id(value)

            if obj_id in active:
                raise ValueError(
                    f"Riferimento circolare rilevato in {path}. "
                    f"Oggetto già incontrato in {active[obj_id]}"
                )

            active[obj_id] = path

            try:

                # ---------------------------------------------
                # 9. Dataclass
                # ---------------------------------------------
                if is_dataclass(value) and not isinstance(value, type):
                    result = {}

                    for field in fields(value):
                        field_value = getattr(value, field.name)

                        result[field.name] = serialize(
                            field_value,
                            f"{path}.{field.name}"
                        )

                    return result

                # ---------------------------------------------
                # 10. Dizionari
                # ---------------------------------------------
                if isinstance(value, Mapping):
                    result = {}

                    for key, item in value.items():

                        if not isinstance(key, str):
                            raise TypeError(
                                f"Chiave non stringa in {path}: "
                                f"{key!r} ({type(key).__name__})"
                            )

                        result[key] = serialize(
                            item,
                            f"{path}.{key}"
                        )

                    return result

                # ---------------------------------------------
                # 11. Liste e tuple
                # ---------------------------------------------
                if isinstance(value, (list, tuple)):
                    result = []

                    for i, item in enumerate(value):
                        result.append(
                            serialize(item, f"{path}[{i}]")
                        )

                    return result

                # ---------------------------------------------
                # 12. Set
                # ---------------------------------------------
                if isinstance(value, (set, frozenset)):
                    return [
                        serialize(item, f"{path}[{i}]")
                        for i, item in enumerate(value)
                    ]

                # ---------------------------------------------
                # 13. Classi Python tradizionali
                # ---------------------------------------------
                if hasattr(value, "__dict__") and not isinstance(value, type):
                    result = {}

                    for key, item in vars(value).items():
                        result[key] = serialize(
                            item,
                            f"{path}.{key}"
                        )

                    return result

                # ---------------------------------------------
                # 14. Tipo non supportato
                # ---------------------------------------------
                raise TypeError(
                    f"Tipo non serializzabile in {path}: "
                    f"{type(value).__module__}."
                    f"{type(value).__name__} "
                    f"(valore={value!r})"
                )

            finally:
                active.pop(obj_id, None)

        result = serialize(obj)

        if not isinstance(result, dict):
            raise TypeError(
                "Il risultato della serializzazione deve essere un dizionario"
            )

        return result

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