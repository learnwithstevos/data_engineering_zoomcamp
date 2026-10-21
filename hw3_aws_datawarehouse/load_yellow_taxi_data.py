import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import boto3
from botocore.exceptions import ClientError
import time


BUCKET_NAME = "learnwithstevo-demo-bucket"
REGION = "us-east-1"

# boto3 will automatically pick up credentials from env vars,
# ~/.aws/credentials, or an IAM role — no key file needed.
s3 = boto3.client("s3", region_name=REGION)


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]
DOWNLOAD_DIR = "."

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_file(month):
    url = f"{BASE_URL}{month}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{month}.parquet")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def create_bucket(bucket_name):
    try:
        # Check if the bucket exists and we have access to it
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' exists and is accessible. Proceeding...")
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            # Bucket doesn't exist, create it
            try:
                if REGION == "us-east-1":
                    # us-east-1 does not accept a LocationConstraint
                    s3.create_bucket(Bucket=bucket_name)
                else:
                    s3.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={"LocationConstraint": REGION},
                    )
                print(f"Created bucket '{bucket_name}'")
            except ClientError as create_err:
                print(f"Failed to create bucket '{bucket_name}': {create_err}")
                sys.exit(1)
        elif error_code == 403:
            print(
                f"A bucket with the name '{bucket_name}' exists, but it is not "
                "accessible. Bucket name is taken. Please try a different bucket name."
            )
            sys.exit(1)
        else:
            print(f"Unexpected error checking bucket '{bucket_name}': {e}")
            sys.exit(1)


def verify_s3_upload(key_name):
    try:
        s3.head_object(Bucket=BUCKET_NAME, Key=key_name)
        return True
    except ClientError:
        return False


def upload_to_s3(file_path, max_retries=3):
    key_name = os.path.basename(file_path)

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            s3.upload_file(file_path, BUCKET_NAME, key_name)
            print(f"Uploaded: s3://{BUCKET_NAME}/{key_name}")

            if verify_s3_upload(key_name):
                print(f"Verification successful for {key_name}")
                return
            else:
                print(f"Verification failed for {key_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to S3: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, MONTHS))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_s3, filter(None, file_paths))  # Remove None values

    print("All files processed and verified.")