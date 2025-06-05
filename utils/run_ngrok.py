import time
import atexit
import os
from dataclasses import dataclass
from typing import Optional
from pyngrok import ngrok, conf

@dataclass
class NgrokConfig:
    """Configuration for ngrok tunnel."""
    port: int
    domain: Optional[str] = None
    auth_token: Optional[str] = None
    config_path: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'NgrokConfig':
        """Create config from environment variables."""
        return cls(
            port=int(os.getenv('N8N_PORT', '8000')),
            domain=os.getenv('WEBHOOK_URL').replace('https://', ''),
            auth_token=os.getenv('NGROK_AUTHTOKEN'),
            config_path=os.getenv('NGROK_CONFIG_PATH')
        )

class NgrokTunnel:
    """Manages ngrok tunnel lifecycle."""
    def __init__(self, config: NgrokConfig):
        self.config = config
        self.tunnel = None
        self._configure_ngrok()
        atexit.register(self.shutdown)

    def _configure_ngrok(self):
        """Configure ngrok settings."""
        if self.config.config_path:
            conf.get_default().config_path = self.config.config_path
        if self.config.auth_token:
            conf.get_default().auth_token = self.config.auth_token

    def start(self) -> str:
        """Start the ngrok tunnel and return the public URL."""
        print(f"Starting ngrok tunnel for http://localhost:{self.config.port}...")
        
        try:
            tunnel_kwargs = {'addr': self.config.port}
            if self.config.domain:
                tunnel_kwargs['domain'] = self.config.domain
            
            self.tunnel = ngrok.connect(**tunnel_kwargs)
            public_url = self.tunnel.public_url
            
            print("--------------------------------------------------------------")
            print(f" * Public URL: {public_url}")
            print(f" * Forwarding to: http://localhost:{self.config.port}")
            print("--------------------------------------------------------------")
            print("Use this Public URL as the 'Test URL' in your n8n Webhook node.")
            print("Ngrok tunnel established!")
            
            return public_url
            
        except Exception as e:
            print(f"Failed to start ngrok tunnel: {e}")
            self.shutdown()
            raise

    def shutdown(self):
        """Gracefully shut down the ngrok tunnel."""
        if self.tunnel:
            try:
                print(f"Shutting down ngrok tunnel: {self.tunnel.public_url}")
                ngrok.disconnect(self.tunnel.public_url)
                print("Ngrok tunnel disconnected.")
            except Exception as e:
                print(f"Error disconnecting ngrok: {e}")
            finally:
                self.tunnel = None
        
        # As a fallback, ensure all tunnels are closed
        ngrok.kill()
        print("Ngrok processes killed (if any were running).")

    def run_forever(self):
        """Run the tunnel indefinitely until interrupted."""
        try:
            self.start()
            print("Press Ctrl+C to exit and shut down the tunnel.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nCtrl+C detected. Shutting down...")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            raise
        finally:
            self.shutdown()

def main():
    """Main entry point for running ngrok as a standalone process."""
    config = NgrokConfig.from_env()
    tunnel = NgrokTunnel(config)
    tunnel.run_forever()

if __name__ == "__main__":
    main()