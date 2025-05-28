import time
import atexit
import sys
from pyngrok import ngrok, conf
import yaml
import os

# --- Configuration ---
N8N_LOCAL_PORT = os.getenv('N8N_PORT', 8000)  # Default n8n port
YAML_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.yaml')
# Optional: If ngrok binary isn't in PATH or you want to specify it
# conf.get_default().ngrok_path = "/path/to/your/ngrok"
# Optional: Set auth token programmatically if not configured via CLI
# You usually configure this once via `ngrok config add-authtoken <token>`
# ---------------------

active_tunnel = None

def shutdown_ngrok():
    """Gracefully shuts down the ngrok tunnel."""
    if active_tunnel:
        print(f"Shutting down ngrok tunnel: {active_tunnel.public_url}")
        try:
            ngrok.disconnect(active_tunnel.public_url)
            print("Ngrok tunnel disconnected.")
        except Exception as e:
            print(f"Error disconnecting ngrok: {e}")
    # As a fallback, ensure all tunnels are closed if disconnect fails
    # Pyngrok typically handles this on exit, but it's good practice
    ngrok.kill()
    print("Ngrok processes killed (if any were running).")

# Register the shutdown function to be called on script exit
atexit.register(shutdown_ngrok)

def write_ngrok_url_to_file(public_url):
    """Writes the ngrok public URL to a file named ngrok_url (for dynamic URLs)."""
    try:
        # Write the public URL to a file
        with open('/app/python/source_code/ngrok_url.txt', 'w') as file:
            file.write(public_url)
            print(f"Wrote ngrok URL to file: {public_url}")
    except Exception as e:
        print(f"Error writing ngrok URL to file: {e}")
        

try:
    print(f"Starting ngrok tunnel for http://localhost:{N8N_LOCAL_PORT}...")

    # Start an HTTP tunnel on the specified port
    # This blocks until the tunnel is established or fails
    # active_tunnel = ngrok.connect(N8N_LOCAL_PORT, "http")
    # active_tunnel = ngrok.connect(addr=N8N_LOCAL_PORT, 
    #                               domain=os.getenv('WEBHOOK_URL'))

    # public_url = active_tunnel.public_url
    # temp 
    public_url = "https://test.ngrok.io"
    
    # Only needed if tunnel URL is dynamic
    # write_ngrok_url_to_file(public_url)
    
    print("--------------------------------------------------------------")
    print(f"Ngrok tunnel established!")
    print(f" * Public URL: {public_url}")
    print(f" * Forwarding to: http://localhost:{N8N_LOCAL_PORT}")
    print("--------------------------------------------------------------")
    print("Use this Public URL as the 'Test URL' in your n8n Webhook node.")
    print("Press Ctrl+C to exit and shut down the tunnel.")

    # Keep the script running so the tunnel stays active.
    # You could replace this with other logic if needed.
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nCtrl+C detected. Shutting down...")
    # atexit handler will take care of shutdown
    sys.exit(0)
except Exception as e:
    print(f"\nAn error occurred: {e}")
    # atexit handler will attempt cleanup
    sys.exit(1)