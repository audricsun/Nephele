# A django app, for prove of concept

## Background

To test and validate some popular extension/framework for django in a real-world-app.


## Local Environment

```shell
make compose-up
```

### Database (PostgreSQL)
- **Service Name:** db
- **URL:** `localhost:5432`

### Adminer
- **Service Name:** adminer
- **URL:** `localhost:8080`

### RabbitMQ Broker
- **Service Name:** broker
- **URLs:**
  - `localhost:5672` (AMQP)
  - `localhost:15672` (Management)

### Mailhog
- **Service Name:** mailhog
- **URLs:**
  - `localhost:2525` (SMTP)
  - `localhost:8025` (Web UI)