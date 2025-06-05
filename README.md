# n8n Databricks Apps

Run n8n as Databricks Apps.

## Description

The application uses localtunnel to expose the locally running `n8n` instance to the internet. It is set up to integrate with a PostgreSQL database hosted on a Databricks instance.

## Prerequisites

- Node.js and npm installed
- Localtunnel installed (as a dependency)
- Access to a Databricks instance with PostgreSQL configured

## Environment Configuration

The application is configured using environment variables specified in `app.yaml`. Key configurations include:

- `N8N_PORT`: Port for the `n8n` service (default: 8000)
- `N8N_HOST`: The host address for `n8n` (default: 0.0.0.0)
- `WEBHOOK_URL`: The URL format for the webhook, using localtunnel
- Database credentials and connection details

## Installation

1. Clone this repository to your Databricks workspace.
2. Change WEBHOOK_URL with your unique domain.
3. Deploy to Databricks Apps

Deployment will:
- Retrieve the tunnel password and display it in logs.
- Start a localtunnel on the specified port with a subdomain derived from the `WEBHOOK_URL`.
- Run the `n8n` service.

## Scripts

- `tunnel`: Starts the localtunnel.
- `get-password`: Retrieves the tunnel password.
- `set-env`: Waits for the tunnel to be ready.
- `n8n`: Runs the `n8n` service.
- `start`: Combines the above scripts to start the application.

## Dependencies

- `localtunnel`: For tunneling local services to the internet.
- `n8n`: The workflow automation tool.

## License

This project is licensed under the MIT License.
