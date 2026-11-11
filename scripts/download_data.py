"""Download the study's datasets into data/ (gitignored).

Usage: uv run --group data python scripts/download_data.py [m5] [hm] [frn]

M5 and H&M come from Kaggle: accept each competition's rules on kaggle.com first, and keep
an API token in ~/.kaggle/kaggle.json. FreshRetailNet-50K comes from Hugging Face (CC BY 4.0).
"""

import sys
import urllib.request
import zipfile
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

M5 = "m5-forecasting-accuracy"
HM = "h-and-m-personalized-fashion-recommendations"
HM_FILES = ["articles.csv", "transactions_train.csv"]  # the images are not needed
FRN = "Dingdong-Inc/FreshRetailNet-50K"
# Kaggle stops at day 1941. The final test window (days 1942-1969) and the official
# WRMSSE weights come from Nixtla's mirror of the released M5 data.
M5_TRUTH_URL = "https://github.com/Nixtla/m5-forecasts/raw/main/datasets/m5.zip"
M5_TRUTH_FILES = ["sales_test_evaluation.csv", "weights_evaluation.csv"]


def kaggle_api():
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    return api


def unzip_all(folder: Path) -> None:
    for archive in folder.glob("*.zip"):
        with zipfile.ZipFile(archive) as z:
            z.extractall(folder)
        archive.unlink()


def download_m5() -> None:
    out = DATA / "m5"
    out.mkdir(parents=True, exist_ok=True)
    kaggle_api().competition_download_files(M5, path=out, quiet=False)
    unzip_all(out)
    archive = out / "m5_truth.zip"
    urllib.request.urlretrieve(M5_TRUTH_URL, archive)
    with zipfile.ZipFile(archive) as z:
        for name in M5_TRUTH_FILES:
            z.extract(name, out)
    archive.unlink()


def download_hm() -> None:
    out = DATA / "hm"
    out.mkdir(parents=True, exist_ok=True)
    api = kaggle_api()
    for name in HM_FILES:
        api.competition_download_file(HM, name, path=out, quiet=False)
    unzip_all(out)


def download_frn() -> None:
    from huggingface_hub import snapshot_download

    snapshot_download(repo_id=FRN, repo_type="dataset", local_dir=DATA / "frn")


SOURCES = {"m5": download_m5, "hm": download_hm, "frn": download_frn}

if __name__ == "__main__":
    for key in sys.argv[1:] or SOURCES:
        SOURCES[key]()
        print(f"{key}: done")
