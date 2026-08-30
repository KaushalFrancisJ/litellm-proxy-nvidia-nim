import asyncio
import os
import time
from collections import Counter

import httpx
from dotenv import load_dotenv

load_dotenv()

URL = "https://integrate.api.nvidia.com/v1/chat/completions"

MODEL = "moonshotai/kimi-k2.6"

PAYLOAD = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": "Reply with exactly: hi"
        }
    ],
    "temperature": 0,
    "max_tokens": 5,
}


async def make_request(client, api_key, request_id):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    start = time.perf_counter()

    try:
        response = await client.post(
            URL,
            headers=headers,
            json=PAYLOAD,
        )

        latency = time.perf_counter() - start

        return {
            "id": request_id,
            "status": response.status_code,
            "latency": latency,
        }

    except Exception as e:
        latency = time.perf_counter() - start

        return {
            "id": request_id,
            "status": "ERROR",
            "latency": latency,
            "error": str(e),
        }


async def test_key(api_key, name, concurrent_requests=60):

    print(f"\n{'='*60}")
    print(f"Testing {name}")
    print(f"{'='*60}")

    limits = httpx.Limits(
        max_connections=concurrent_requests,
        max_keepalive_connections=concurrent_requests,
    )

    timeout = httpx.Timeout(60)

    async with httpx.AsyncClient(
        limits=limits,
        timeout=timeout,
        http2=True,
    ) as client:

        start = time.perf_counter()

        tasks = [
            make_request(client, api_key, i + 1)
            for i in range(concurrent_requests)
        ]

        results = await asyncio.gather(*tasks)

        total = time.perf_counter() - start

    counts = Counter(r["status"] for r in results)

    print("\nStatus Summary")

    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")

    latencies = [
        r["latency"]
        for r in results
        if isinstance(r["status"], int)
    ]

    if latencies:
        print("\nLatency")
        print(f"Average : {sum(latencies)/len(latencies):.2f}s")
        print(f"Minimum : {min(latencies):.2f}s")
        print(f"Maximum : {max(latencies):.2f}s")

    print(f"\nCompleted in {total:.2f}s")

    return counts


async def main():

    key1 = os.environ["NVIDIA_API_KEY1"]
    key2 = os.environ["NVIDIA_API_KEY2"]

    result1 = await test_key(
        key1,
        "KEY1",
        concurrent_requests=60,
    )

    print("\nImmediately testing KEY2...\n")

    result2 = await test_key(
        key2,
        "KEY2",
        concurrent_requests=60,
    )

    print("\n==============================")
    print("FINAL RESULT")
    print("==============================")

    print("KEY1:", dict(result1))
    print("KEY2:", dict(result2))


if __name__ == "__main__":
    asyncio.run(main())