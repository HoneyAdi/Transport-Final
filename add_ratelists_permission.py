"""
Add ratelists permission to all existing tenants
"""
from webapp import app, db, Tenant, TenantPermission

def add_ratelists_permission():
    with app.app_context():
        for tenant in Tenant.query.all():
            existing = TenantPermission.query.filter_by(tenant_id=tenant.id, module_name='ratelists').first()
            if not existing:
                db.session.add(
                    TenantPermission(
                        tenant_id=tenant.id,
                        module_name='ratelists',
                        can_view=True,
                        can_create=True,
                        can_edit=True,
                        can_delete=True,
                        can_export=True,
                    )
                )
                print(f"Added ratelists permission for tenant: {tenant.name}")
            else:
                print(f"ratelists permission already exists for tenant: {tenant.name}")
        
        db.session.commit()
        print("Done!")

if __name__ == "__main__":
    add_ratelists_permission()
