# n8n Databricks Apps

Self-host [n8n](https://github.com/n8n-io/n8n) in [Databricks Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps). This repo provides Node.js installation of n8n, and container-ready configurations tailored for Databricks Apps. The project eases n8n installation in Databricks.

## 🚀 Overview

This project enables you to run n8n (a powerful workflow automation tool) on Databricks Apps by providing ready-to-deploy configuration for deploy n8n in Databricks Apps.

## 📁 Project Structure

```
n8n-databricks-apps/
├── package.json          # Node.js dependencies and scripts
├── app.yaml              # Databricks deployment configuration
├── README.md             # Project documentation
└── .gitignore           # Git ignore rules
```

## 🛠️ Features

- **n8n Installation**: Installs n8n via Node.js
- **Webhook Integration**: Pre-configured [Ngrok](https://ngrok.com/) webhook URL (requires setup) to enable webhook in n8n

## 🚀 Quick Start

### Prerequisites

- **Databricks Apps**: To host n8n, with proper access to secrets as resources
- **Ngrok Account**: Free or paid account with a reserved static URL and API token
- **Supabase Database**: [Supabase](https://supabase.com/) Postgre database to persist n8n workflow executions, history, and credentials (can also use other databases)
- **Secrets Configuration**: The following secrets must be configured in Databricks:
  - `n8n-encryption-key`: Encryption key for securing n8n data
  - `supabase-host`: Supabase database host URL
  - `supabase-user`: Supabase database username
  - `supabase-pw`: Supabase database password
  - `webhook-url`: Webhook endpoint URL
  - `ngrok-token`: Ngrok authentication token

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd n8n-databricks-apps
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the application**:
   ```bash
   npm start
   ```

The application will:
- Install n8n and ngrok dependencies
- Configure ngrok with your authentication token
- Connect to Supabase database for data persistence
- Launch n8n on port 8000 with encryption enabled
- Set up ngrok tunnel for webhook access
- Make n8n available at `http://0.0.0.0:8000`
- Enable automatic data pruning (7 days retention, max 20,000 executions)

## 📋 Configuration

### Environment Variables

The application uses the following environment variables (configured in `app.yaml`):

#### N8N Configuration
- `N8N_PORT`: Port for n8n to run on (default: 8000)
- `N8N_HOST`: Host binding (default: 0.0.0.0)
- `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE`: Enable community package tools (default: true)
- `N8N_ENCRYPTION_KEY`: Encryption key for securing credentials and data

#### Database Configuration (Supabase)
- `DB_TYPE`: Database type (postgresdb)
- `DB_POSTGRESDB_DATABASE`: Database name (n8ndb)
- `DB_POSTGRESDB_SCHEMA`: Database schema (n8n)
- `DB_POSTGRESDB_PORT`: Database port (5432)
- `DB_POSTGRESDB_HOST`: Database host (from secrets)
- `DB_POSTGRESDB_USER`: Database username (from secrets)
- `DB_POSTGRESDB_PASSWORD`: Database password (from secrets)
- `DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED`: SSL verification (false for development)

#### Data Management
- `EXECUTIONS_DATA_PRUNE`: Enable automatic data pruning (true)
- `EXECUTIONS_DATA_MAX_AGE`: Hours to keep execution data (168 = 7 days)
- `EXECUTIONS_DATA_PRUNE_MAX_COUNT`: Maximum executions to store (20000)

#### Webhook Configuration
- `WEBHOOK_URL`: Webhook endpoint URL (from secrets)
- `NGROK_TOKEN`: Ngrok authentication token (from secrets)

### Available Scripts

The `package.json` includes several useful scripts:

- `npm start`: Full application startup with ngrok tunnel
- `npm run n8n`: Run n8n only
- `npm run ngrok`: Start ngrok tunnel only
- `npm run set-token`: Configure ngrok authentication token

### Customizing Dependencies

To modify n8n or ngrok versions, update the `dependencies` section in `package.json`:

```json
{
  "dependencies": {
    "ngrok": "5.0.0",
    "n8n": "1.28.0"
  }
}
```

## 🔧 Development

### Adding Workflows

1. Create your n8n workflow in the n8n editor
2. Export the workflow as JSON
3. Save it in your preferred directory
4. Import the workflow into your n8n instance

### Extending the Application

You can extend the application by adding new scripts to `package.json`:

```json
{
  "scripts": {
    "dev": "n8n start --tunnel",
    "build": "npm install && npm run set-token",
    "test": "echo \"No tests specified\""
  }
}
```

## 🚀 Deployment on Databricks

### Using app.yaml

The `app.yaml` file is configured for Databricks deployment with:

- **N8N Configuration**: Port, host, and encryption settings
- **Database Integration**: Complete Supabase PostgreSQL configuration
- **Data Management**: Automatic pruning and execution limits
- **Security**: Encrypted credentials and SSL configuration
- **Webhook Setup**: Ngrok tunneling for external access
- **Secrets Management**: Secure credential storage using Databricks secrets

### Manual Deployment

1. **Configure Secrets**: Set up all required secrets in Databricks:
   - `n8n-encryption-key`: Generate a secure encryption key
   - `supabase-host`: Your Supabase database host
   - `supabase-user`: Database username
   - `supabase-pw`: Database password
   - `webhook-url`: Your webhook endpoint URL
   - `ngrok-token`: Your ngrok authentication token

2. **Upload Files**: Upload the project files to your Databricks workspace

3. **Deploy**: Run `npm install && npm start` in your Databricks environment

### Database Setup

Before deployment, ensure your Supabase database has:
- Database named `n8ndb`
- Schema named `n8n`
- Proper user permissions for the configured database user

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Fails**
   - Verify Supabase credentials in Databricks secrets
   - Check database host accessibility
   - Ensure SSL configuration matches your setup

2. **Encryption Key Issues**
   - Verify `n8n-encryption-key` secret is properly set
   - Ensure encryption key is consistent across deployments

3. **Webhook Configuration**
   - Check `webhook-url` and `ngrok-token` secrets
   - Verify ngrok tunnel is properly established

4. **Port Already in Use**
   - Change `N8N_PORT` in `app.yaml`
   - Kill existing processes on the port

5. **Data Pruning Issues**
   - Adjust `EXECUTIONS_DATA_MAX_AGE` for longer retention
   - Modify `EXECUTIONS_DATA_PRUNE_MAX_COUNT` for more executions

### Debug Mode

Enable verbose logging by running n8n with debug flags:

```bash
# Run n8n with debug logging
npm run n8n -- --debug

# Run with tunnel mode for easier webhook testing
npm run n8n -- --tunnel
```

## 📄 License

[Add your license information here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the n8n documentation: https://docs.n8n.io/
- Review [Databricks documentation](https://docs.databricks.com/) for Databricks-specific issues

---

**Note**: This project is designed for Databricks environments and may require adjustments for other platforms.
