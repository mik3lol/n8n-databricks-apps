# n8n Databricks Apps

Run n8n as Databricks Apps.

## Description

The application uses ngrok to expose the locally running `n8n` instance to the internet. It is set up to integrate with a PostgreSQL database hosted on a Databricks instance.

## Prerequisites

- Node.js and npm installed
- ngrok account with an auth token
- Access to a Databricks instance with PostgreSQL configured

## Environment Configuration

The application is configured using environment variables specified in `app.yaml`. Key configurations include:

- `N8N_PORT`: Port for the `n8n` service (default: 8000)
- `N8N_HOST`: The host address for `n8n` (default: 0.0.0.0)
- `WEBHOOK_URL`: The URL for the webhook (ngrok-free.app domain)
- `NGROK_TOKEN`: Your ngrok authentication token
- Database credentials and connection details

## Installation

1. Clone this repository to your Databricks workspace.
2. Set up your ngrok auth token in the environment variables.
3. Configure your WEBHOOK_URL with your ngrok-free.app domain.
4. Deploy to Databricks Apps

Deployment will:
- Configure ngrok with your auth token.
- Start ngrok tunnel on the specified port pointing to your webhook URL.
- Run the `n8n` service.

## Scripts

- `set-token`: Configures ngrok with your authentication token.
- `ngrok`: Starts the ngrok tunnel.
- `n8n`: Runs the `n8n` service.
- `start`: Combines the above scripts to start the application.

## Dependencies

- `ngrok`: For secure tunneling to the internet.
- `n8n`: The workflow automation tool.

## License

This project is licensed under the MIT License.
