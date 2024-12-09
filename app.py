from utils.jsrunners import NodeJsEntrypoint

if __name__ == "__main__":
    entrypoint = NodeJsEntrypoint()
    entrypoint.with_command("npx n8n").run()