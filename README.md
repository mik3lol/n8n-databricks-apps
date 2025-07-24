# n8n Databricks Apps

Self-host [n8n](https://github.com/n8n-io/n8n) in [Databricks Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps). This repo provides Node.js installation of n8n, and container-ready configurations tailored for Databricks Apps. Works in both [Databricks Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition) and paid versions.

## 🚀 Overview

This project enables you to run [n8n](https://github.com/n8n-io/n8n) (a powerful workflow automation tool) in [Databricks Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps) by providing ready-to-deploy setup Node.js project with configuration YAML. 

## 🛠️ Features

- **n8n Installation**: Installs n8n via Node.js
- **Webhook Integration**: Uses [Ngrok](https://ngrok.com/) webhook URL (requires setup) to enable webhook in n8n
- **Postgres Integration**: Uses Postgres database (e.g., [Supabase](https://supabase.com/) or [Databricks Lakebase](https://docs.databricks.com/aws/en/oltp/)) to persist n8n workflow executions, history, and credentials, ensuring reliable storage and recovery of application data.

## 📁 Project Structure

```
n8n-databricks-apps/
├── package.json          # Node.js dependencies and scripts
├── app.yaml              # Databricks deployment configuration
├── README.md             # Project documentation
└── .gitignore           # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- **Databricks Account**: Free or paid [Databricks](https://docs.databricks.com/aws/en/getting-started/free-edition) account with access to Databricks Apps
- **Ngrok Account**: Free or paid [Ngrok](https://ngrok.com/) account with a [reserved static URL](https://ngrok.com/blog-post/dns-zone-switch-configuration#now-try-out-a-branded-domain) and [authentication token](https://dashboard.ngrok.com/get-started/your-authtoken)
- **Postgres Database**: Free or paid [Supabase](https://supabase.com/) account or other Postgres databases such as [Databricks Lakebase](https://docs.databricks.com/aws/en/oltp/)
- **Secrets Configuration**: The following secrets must be configured in Databricks:
  - `n8n-encryption-key`: (optional) user-defined encryption key for securing n8n credentials
  - `supabase-host`: Supabase database host URL
  - `supabase-user`: Supabase database username
  - `supabase-pw`: Supabase database password
  - `webhook-url`: Webhook endpoint URL
  - `ngrok-token`: Ngrok authentication token

### Installation

1. **Clone this repository into your Databricks workspace ([doc](https://docs.databricks.com/aws/en/repos/repos-setup))**

2. **Create a custom Databricks Apps (if not exist) ([doc](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/create-custom-app))**

3. **Configure app**
   
   1. Sign up for [Ngrok](https://ngrok.com/) or other tunnel service and get tunnel URL and authentication token
   2. Sign up for [Supabase](https://supabase.com/) and set up database and get host, user, and password
   3. Add above credentials as [Databricks secrets](https://docs.databricks.com/aws/en/security/secrets/) and [make them app resources](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/secrets)
   4. Update `app.yaml` to reference your secrets

4. **Deploy n8n installation code to Databricks Apps ([doc](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy))**

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

### Installation Script

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

## 🔍 Troubleshooting

Monitor [application logs](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/monitor) for app events and error messages.

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the [repository](https://github.com/mik3lol/n8n-databricks-apps)
- Check the n8n documentation: https://docs.n8n.io/
- Review [Databricks documentation](https://docs.databricks.com/) for Databricks-specific issues

---

**Note**: This project is designed for Databricks environments and will require adjustments for other platforms.
