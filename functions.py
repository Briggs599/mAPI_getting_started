import shutil
import time
import requests


def upload_file(dolbyio_mapi_key, file_path):
    url = "https://api.dolby.com/media/input"

    headers = {"x-api-key": dolbyio_mapi_key,
        "Content-Type": "application/json",
        "Accept": "application/json",}

    body = {"url": "dlb://in/" + file_path,}

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    data = response.json()
    presigned_url = data["url"]

    print("Uploading {0}".format(file_path))

    with open(file_path, "rb") as input_file:
        requests.put(presigned_url, data=input_file)

    print("Upload Complete.")
    return "dlb://in/" + file_path


def start_job(dolbyio_mapi_key, job_type, file_id):
    body = {
    "input" : file_id,
    "output" : "dlb://out/test_1-enhanced.wav",
    "content" : {
        "type": "mobile_phone"}
    }

    url = "https://api.dolby.com/media/enhance"

    headers = {
    "x-api-key": dolbyio_mapi_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
    }

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    print("Enhance job has started.")
    job_id = response.json()["job_id"]

    #Check status
    while True:
        time.sleep(10)

        headers = {
        "x-api-key": dolbyio_mapi_key,
        "Content-Type": "application/json",
        "Accept": "application/json"}

        params = {"job_id": job_id}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        print(response.json()["status"])

        if response.json()["status"] == "Success":
            print("Enhance job is complete.")
            break

    return job_id

def download_file(dolbyio_mapi_key, job_id):
    url = "https://api.dolby.com/media/output"
    headers = {
        "x-api-key": dolbyio_mapi_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    args = {"url": "dlb://out/test_1-enhanced.wav",}

    with requests.get(url, params=args, headers=headers, stream=True) as response:
        response.raise_for_status()
        response.raw.decode_content = True
        print("Downloading test_1-enhanced.wav")
        with open("test_1-enhanced.wav", "wb") as output_file:
            shutil.copyfileobj(response.raw, output_file)
