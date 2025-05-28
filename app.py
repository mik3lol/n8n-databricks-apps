from utils.jsrunners import NodeJsEntrypoint
import subprocess
import sys
import time
import os

def wait_for_ngrok_ready(process):
    """Wait for ngrok to be ready by monitoring its output."""
    while True:
        line = process.stdout.readline()
        if not line:
            print("Error: ngrok process terminated unexpectedly")
            sys.exit(1)
        
        # Print ngrok output to console
        print(line.decode().strip())
        
        # Check for the success message
        if "Ngrok tunnel established!" in line.decode():
            return True

if __name__ == "__main__":    
    # Start ngrok process with pipe to capture output
    ngrok_process = subprocess.Popen(
        ['python', 'utils/run_ngrok.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # Wait for ngrok to be ready before starting n8n
    if wait_for_ngrok_ready(ngrok_process):
        print("Ngrok is ready, starting n8n...")
        entrypoint = NodeJsEntrypoint()
        entrypoint.with_command("npx n8n").run()