import pytest
from .conftest import UserData, AdminUserData

def test_create_url(client, headers):
    json_data = {
        'url_key': UserData.url_key,
        'redirect_url': UserData.redirect_url
    }
    response = client.post('/', json=json_data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['owner_id'] == UserData.id
    assert data['url_key'] != json_data['url_key']
    UserData.url_key = data['url_key']

def test_admin_create_url(client, admin_headers):
    json_data = {
        'url_key': AdminUserData.url_key,
        'redirect_url': AdminUserData.redirect_url
    }
    response = client.post('/', json=json_data, headers=admin_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['owner_id'] == AdminUserData.id
    assert data['url_key'] == json_data['url_key']

def test_get_urls(client, headers):
    response = client.get('/', headers=headers)
    assert response.status_code == 403

def test_admin_get_urls(client, admin_headers):
    response = client.get('/', headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_get_url(client):
    response = client.get(f'/{UserData.url_key}')
    assert response.status_code == 200

def test_admin_get_url(client):
    response = client.get(f'/{AdminUserData.url_key}')
    assert response.status_code == 200

def test_update_url(client, headers):
    json_data = {
        'url_key': 'zzz',
        'redirect_url': 'https://github.com/MekodoDE',
        'is_active': False,
        'owner_id': '53374ee1-6f77-4f16-99e3-d7957e7c9ad7'
    }
    response = client.put(f'/{UserData.url_key}', json=json_data, headers=headers)
    print(response.get_json())
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert data['url_key'] == UserData.url_key
    assert data['redirect_url'] == UserData.redirect_url
    assert data['is_active'] == json_data['is_active']
    assert data['owner_id'] == UserData.id

def test_admin_update_url(client, admin_headers):
    json_data = {
        'url_key': 'hello',
        'redirect_url': 'https://github.com/MekodoDE',
        'is_active': False,
        'owner_id': '53374ee1-6f77-4f16-99e3-d7957e7c9ad7'
    }
    response = client.put(f'/{AdminUserData.url_key}', json=json_data, headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert data['url_key'] == json_data['url_key']
    AdminUserData.url_key = json_data['url_key']
    assert data['redirect_url'] == json_data['redirect_url']
    assert data['is_active'] == json_data['is_active']
    assert data['owner_id'] == json_data['owner_id']

def test_delete_url(client, headers):
    response = client.delete(f'/{UserData.url_key}', headers=headers)
    assert response.status_code == 204

    response = client.get(f'/{UserData.url_key}')
    assert response.status_code == 404

def test_admin_delete_url(client, admin_headers):
    response = client.delete(f'/{AdminUserData.url_key}', headers=admin_headers)
    assert response.status_code == 204

    response = client.get(f'/{AdminUserData.url_key}')
    assert response.status_code == 404