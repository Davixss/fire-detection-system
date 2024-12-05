import requests
import json

class FlaskClient:

    # Execute Request
    def sendRequest(host, port, method, endpoint, data):

        # Handle request based on method passed
        def handleMethod(method, url, data):
            if method == 'GET':
                return requests.get(url, params=data)
            elif method == 'POST':
                return requests.post(url, json=data)
            elif method == 'PUT':
                return requests.put(url, json=data)
            elif method == 'DELETE':
                return requests.delete(url, params=data)
            else:
                return None
            
        # Send request
        try:
            url = f"http://{host}:{port}/{endpoint}"
            print(f">> [FLASK REQUEST]: {method} /{endpoint} with data: {data}")
            response = handleMethod(method, url, data)

            if response is not None:
                if response.status_code == 200:
                    print(json.loads(response.text))
                    return json.loads(response.text)
                elif response.status_code == 404:
                    print(f"[ERROR 404]: Resource /{endpoint} not found")
                else:
                    print(f"[ERROR {response.status_code}]: {response.text}")
            else:
                print(f"[ERROR 405]: Method {method} not allowed")

        except requests.exceptions.RequestException as e:
            print(f"Errore di connessione: {e}")
    