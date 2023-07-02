import requests as req
import json


ADRESS = '192.168.2.109'

RED = [250,0,0]
GREEN = [0,250,0]
BLUE = [0,0,250]
PURPLE = [250,0,250]
YELLOW = [0,250,250]

class TestClassServer:

    def test_get(self):
        response = req.get('http://' + ADRESS)
        assert response.status_code == 200
        print(response)

    def test_get_state(self):
        response = req.get('http://' + ADRESS + '/state')
        assert response.status_code == 200
        body: dict = response.json()

        assert 'leds' in  body.keys()
        assert 'time' in  body.keys()
        for led in body['leds']:
            assert len(body['time']) == len(led)

    def test_get_false_url(self):
        response = req.get('http://' + ADRESS + '/st')
        assert response.status_code == 400

    def test_post(self):
        lightshow = {'time': [  0.0,  1.0,   1.1,   4.0, 4.1,   5,  5.1],
                     'leds': [[BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE]]}

        response = req.post('http://' + ADRESS, data=json.dumps(lightshow), headers={'Content-type': 'application/json'})
        assert response.status_code == 201

        response = req.get('http://' + ADRESS + '/state')
        assert response.status_code == 200
        body: dict = response.json()

        assert 'leds' in  body.keys()
        assert 'time' in  body.keys()

        assert lightshow == body

    def test_post_bad_lightshow_more_time(self):
        lightshow = {'time': [  0.0,  1.0,   1.1,   4.0, 4.1,   5,  5.1, 6.0],
                     'leds': [[BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE]]}

        response = req.post('http://' + ADRESS, data=json.dumps(lightshow), headers={'Content-type': 'application/json'})
        assert response.status_code == 400

    def test_post_bad_lightshow_less_time(self):
        lightshow = {'time': [  0.0,  1.0,   1.1,   4.0, 4.1,   5],
                     'leds': [[BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE]]}

        response = req.post('http://' + ADRESS, data=json.dumps(lightshow), headers={'Content-type': 'application/json'})
        assert response.status_code == 400

    def test_post_bad_lightshow_to_many_leds(self):
        lightshow = {'time': [  0.0,  1.0,   1.1,   4.0, 4.1,   5,  5.1],
                     'leds': [[BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED, BLUE, BLUE]]}

        response = req.post('http://' + ADRESS, data=json.dumps(lightshow), headers={'Content-type': 'application/json'})
        assert response.status_code == 400

    def test_post_bad_lightshow_to_few_leds(self):
        lightshow = {'time': [  0.0,  1.0,   1.1,   4.0, 4.1,   5,  5.1],
                     'leds': [[BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED],
                              [BLUE, BLUE, GREEN, GREEN, RED, RED]]}

        response = req.post('http://' + ADRESS, data=json.dumps(lightshow), headers={'Content-type': 'application/json'})
        assert response.status_code == 400
