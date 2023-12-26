# Enhancements and Fixes
## Configuration is Key
- Podman secret configuration handling
- [DONE] Ansible Vault and Playbook for fully automated pod creation

## Once the build nonsense is out of the way...
- Asyncpg connection pool to reduce overhead when establishing connections to the database
- Custom bot class to properly use dependency injection with the database, and all that weird nonsense I was confused about...

## After getting all that working...
- Nginx Reverse Proxy for Pod