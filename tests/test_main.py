import pytest
from dao.mongodb_connector import MongoDBConnector
from main import calcolo_esempio

def test_calcolo_esempio():
    with pytest.raises(ZeroDivisionError):
        calcolo_esempio(2, 0)

def test_connection():
    conn = MongoDBConnector()
    conn.ping()
    print("Test connection")
    conn.close()