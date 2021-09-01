
def test_response(app, db, client):

    response = client.get('/resolve-doi/10.5281/zenodo.5335900', content_type='application/json')
    assert response.status_code == 200

    response = client.get('/resolve-doi/xx/xx', content_type='application/json')
    assert response.json == {'error': 'doi not found'}

    # url = "https://localhost:5000/records/kch"
    # response = client.post(url)
    # print("res" + str(response))
    # assert response.status_code == 200