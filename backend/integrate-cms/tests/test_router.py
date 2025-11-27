from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integrate_cms_router():
    response = client.get('/integrate-cms')
    assert response.status_code == 200