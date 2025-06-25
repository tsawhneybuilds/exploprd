import asyncio
import openai
import httpx
import os
from dotenv import load_dotenv
import jose.jwt

async def main():
    """
    A minimal script to isolate the OpenAI client initialization.
    """
    print("--- Starting OpenAI Client Debug ---")
    
    # Load environment variables (for OPENAI_API_KEY)
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment.")
        return

    print(f"OpenAI library version: {openai.__version__}")
    print(f"HTTPX library version: {httpx.__version__}")

    try:
        print("\nAttempt 1: Initializing OpenAI client WITHOUT custom httpx client...")
        # This is the version that fails in the app
        client_default = openai.AsyncOpenAI(api_key=api_key)
        await client_default.close()
        print("✅ SUCCESS: Default client initialized and closed without error.")
    except Exception as e:
        print(f"❌ FAILED: Could not initialize default client. Error: {e}")

    print("-" * 20)

    try:
        print("\nAttempt 2: Initializing OpenAI client WITH custom httpx client (proxies disabled)...")
        # This is the fix we've been trying
        custom_httpx_client = httpx.AsyncClient(proxies={})
        client_custom = openai.AsyncOpenAI(
            api_key=api_key,
            http_client=custom_httpx_client
        )
        await client_custom.close()
        print("✅ SUCCESS: Custom client initialized and closed without error.")
    except Exception as e:
        print(f"❌ FAILED: Could not initialize custom client. Error: {e}")

    print("\n--- Debug Finished ---")

if __name__ == "__main__":
    asyncio.run(main()) 