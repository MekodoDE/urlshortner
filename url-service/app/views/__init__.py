from . import url

# Define resources to register
resources = (
    url,
)

def register_blueprints(api):
    """
    Initialize application with all modules.

    Parameters:
    - api: Flask-Smorest Api instance
    """
    # Register blueprints for all resources
    for resource_blp in (res.blp for res in resources):
        api.register_blueprint(resource_blp)
