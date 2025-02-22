# Define roles and their permissions
ROLES_PERMISSIONS = {
    "super_admin": ["manage_all_tenants", "manage_users", "view_public_info"],
    "admin": ["manage_tenant", "send_messages", "view_public_info"],
    "user": ["send_messages", "view_public_info"],
    "guest": ["view_public_info"],
}