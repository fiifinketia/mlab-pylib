import asyncio
import os
import json
import requests
from __utils import fetch_parameters

class TrainResults:
    """Results of training."""
    def __init__(self, pretrained_model: str, metrics: dict[str, float], files: []):
        self.pretrained_model = pretrained_model
        self.metrics = metrics
        self.files = files

def train(
    model_path:str,
    result_id: str,
    API_URL: str,
) -> TrainResults:
    """
    Train a model
    This function will provide the dataset path, parameters and result_id
    and will return the results of training.
    """

    parameters = fetch_parameters(config_path=f"{model_path}/config.txt")
    DATASET_PATH = str(parameters["dataset_url"]).strip() # type: ignore

    train_model = getattr(__import__(f"{model_path}.model", fromlist=["train"]), "train")

    try:
        async def main():
            model: TrainResults = train_model(dataset_path=DATASET_PATH, parameters=parameters, result_id=result_id)
            files = {}

            for file in model.files:
                filename = file.name
                files[filename] = file

            # Stringify metrics
            metrics = json.dumps(model.metrics)
            data = {
                "result_id": result_id,
                "metrics": metrics,
                "pretrained_model": model.pretrained_model,
            }


            response = requests.post(API_URL, data=data, files=files,timeout=120, verify=False)

            if response.status_code != 200:
                raise requests.HTTPError(f"Error uploading results. Status code: {response.status_code}, error: {response.text}")

        asyncio.run(main())
    except Exception as e:
        # Append error in error.txt file
        # First check if error.txt file exists
        if not os.path.exists(f"{result_id}/error.txt"):
            os.mkdir(result_id)
            with open(f"{result_id}/error.txt", "w", encoding="utf-8") as f:
                f.write(str(e))
        else:
            with open(f"{result_id}/error.txt", "a", encoding="utf-8") as f:
                f.write(str(e))
        error_file = open(f"{result_id}/error.txt", "rb")
        req_files = {
            "error.txt": error_file,
        }
        requests.post(API_URL+f"?error={True}", data={"result_id": result_id, "error": str(e)}, files=req_files, timeout=120)
