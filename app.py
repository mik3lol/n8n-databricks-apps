import sys
import time
import subprocess
from threading import Thread
from typing import Optional
from utils.run_ngrok import NgrokConfig, NgrokTunnel

class ProcessMonitor:
    """Monitor and manage a subprocess with real-time output."""
    def __init__(self, cmd: list[str], name: str):
        self.cmd = cmd
        self.name = name
        self.process: Optional[subprocess.Popen] = None
        self.thread: Optional[Thread] = None
        
    def _monitor_output(self):
        """Monitor process output in a separate thread."""
        while self.process:
            line = self.process.stdout.readline()
            if not line and self.process.poll() is not None:
                break
            if line:
                print(f"[{self.name}] {line.decode().strip()}")
    
    def start(self, wait_for_ready: bool = False) -> bool:
        """Start the process and optionally wait for it to be ready."""
        print(f"Starting {self.name}...")
        self.process = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        # Start output monitoring in a separate thread
        self.thread = Thread(target=self._monitor_output, daemon=True)
        self.thread.start()
        
        return True
    
    def stop(self):
        """Stop the process."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
        if self.thread:
            self.thread.join()
            self.thread = None

def main():
    """Main entry point for the application."""
    try:
        # Start ngrok in the main process
        config = NgrokConfig.from_env()
        tunnel = NgrokTunnel(config)
        tunnel.start()  # This will block until ngrok is ready
        
        # Start n8n in a monitored subprocess
        n8n = ProcessMonitor(['npm', 'run', 'start'], 'n8n')
        n8n.start()
        
        # Keep the main process running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            n8n.stop()
            tunnel.shutdown()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()