#!/usr/bin/env python3
"""
Batch API client for offline transcription processing
"""

import base64
import json
import time
import uuid
from typing import Dict, List, Optional

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class BatchTranscriptionClient:
    """Client for batch transcription API"""

    def __init__(self, api_url: str, api_key: str):
        """
        Initialize batch transcription client

        Args:
            api_url: Base URL for batch API (e.g., https://api.talkscriber.com/api/jobs)
            api_key: API key for authentication
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError(
                "requests library is required for batch mode. "
                "Install with: pip install requests"
            )

        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

    def create_batch_job(
        self,
        audio_file_path: str,
        language: str = "en",
        task: str = "transcribe",
        features: Optional[List[str]] = None,
        model: str = "L3",
        store_conversation: bool = False,
        channels: Optional[List] = None,
        meta_info: Optional[Dict] = None,
    ) -> Dict:
        """
        Create a new batch transcription job

        Args:
            audio_file_path: Path to audio file
            language: Language code (default: "en")
            task: "transcribe" or "translate" (default: "transcribe")
            features: List of features to enable (e.g., ["sentiment", "redaction"])
            model: Model type (default: "L3")
            store_conversation: Whether to store conversation (default: False)
            channels: Channel configuration
            meta_info: Additional metadata

        Returns:
            Job response dict with job_id
        """
        # Read and encode audio file
        try:
            with open(audio_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
                encoded_audio = base64.b64encode(audio_data).decode("utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        except Exception as e:
            raise Exception(f"Error reading audio file: {e}")

        # Prepare payload
        job_name = str(uuid.uuid4())
        payload = {
            "service_type": "batch",
            "name": job_name,
            "model_type": model,
            "features": features or [],
            "language": language,
            "task": task,
            "store_conversation": store_conversation,
            "channels": channels or [],
            "data": encoded_audio,
            "meta_info": meta_info or {},
        }

        # Send POST request
        try:
            response = requests.post(
                self.api_url, headers=self.headers, data=json.dumps(payload), timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise Exception("Authentication failed. Please check your API key.")
            elif response.status_code == 403:
                raise Exception("Access forbidden. Please check your permissions.")
            elif response.status_code == 400:
                raise Exception(f"Bad request: {response.text}")
            else:
                raise Exception(f"HTTP error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def get_batch_job_status(self, job_id: str) -> Dict:
        """
        Get status of a batch job

        Args:
            job_id: Job ID to check

        Returns:
            Job status dict
        """
        try:
            response = requests.get(
                f"{self.api_url}/{job_id}", headers=self.headers, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise Exception(f"Job not found: {job_id}")
            else:
                raise Exception(f"HTTP error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get job status: {e}")

    def wait_for_job_completion(
        self, job_id: str, poll_interval: int = 2, timeout: int = 3600
    ) -> Dict:
        """
        Poll job status until completion

        Args:
            job_id: Job ID to wait for
            poll_interval: Seconds between status checks (default: 2)
            timeout: Maximum wait time in seconds (default: 3600)

        Returns:
            Final job status dict with results
        """
        start_time = time.time()
        last_status = None
        status_start_time = time.time()

        print(f"[INFO]: Waiting for job completion...")
        print(f"[INFO]: Job ID: {job_id}")

        while True:
            # Check timeout
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                raise Exception(f"Job timed out after {timeout} seconds")

            # Get job status
            try:
                job_status = self.get_batch_job_status(job_id)
            except Exception as e:
                print(f"[ERROR]: Failed to get job status: {e}")
                time.sleep(poll_interval)
                continue

            current_status = job_status.get("status")

            # Check for completion
            if current_status == "DONE":
                elapsed = time.time() - start_time
                print(f"[INFO]: Job completed successfully in {elapsed:.2f} seconds")
                return job_status

            # Check for failures
            if current_status in [
                "FAILED_TS_TRANSCRIBE",
                "FAILED",
                "FAILED_TRANSCRIBE",
            ]:
                raise Exception(f"Job failed with status: {current_status}")

            # Print status changes
            if current_status != last_status:
                print(f"[INFO]: Job status: {current_status}")
                last_status = current_status
                status_start_time = time.time()
            elif time.time() - status_start_time >= 60:
                # Print update every 60 seconds if status unchanged
                print(f"[INFO]: Still processing... (status: {current_status})")
                status_start_time = time.time()

            # Wait before next poll
            time.sleep(poll_interval)


def create_batch_job(
    api_url: str,
    api_key: str,
    audio_file_path: str,
    language: str = "en",
    task: str = "transcribe",
    features: Optional[List[str]] = None,
    **kwargs,
) -> Dict:
    """
    Convenience function to create a batch job

    Args:
        api_url: Batch API URL
        api_key: API key
        audio_file_path: Path to audio file
        language: Language code
        task: "transcribe" or "translate"
        features: List of feature names
        **kwargs: Additional parameters

    Returns:
        Job response dict
    """
    client = BatchTranscriptionClient(api_url, api_key)
    return client.create_batch_job(
        audio_file_path=audio_file_path,
        language=language,
        task=task,
        features=features,
        **kwargs,
    )


def get_batch_job_status(api_url: str, api_key: str, job_id: str) -> Dict:
    """
    Convenience function to get job status

    Args:
        api_url: Batch API URL
        api_key: API key
        job_id: Job ID

    Returns:
        Job status dict
    """
    client = BatchTranscriptionClient(api_url, api_key)
    return client.get_batch_job_status(job_id)


def wait_for_job_completion(
    api_url: str, api_key: str, job_id: str, poll_interval: int = 2, timeout: int = 3600
) -> Dict:
    """
    Convenience function to wait for job completion

    Args:
        api_url: Batch API URL
        api_key: API key
        job_id: Job ID
        poll_interval: Seconds between polls
        timeout: Maximum wait time

    Returns:
        Final job status with results
    """
    client = BatchTranscriptionClient(api_url, api_key)
    return client.wait_for_job_completion(job_id, poll_interval, timeout)
