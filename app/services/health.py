import toml
from pathlib import Path
from app.models.health import Healthcheck

def get_project_info():
    pyproject_path = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"

    try:
        pyproject = toml.load(pyproject_path)
        project_info = pyproject.get("project", {})
        name = project_info.get("name", "N/A")
        description = project_info.get("description", "N/A")
        version = project_info.get("version", "N/A")
        return {"name": name, "description": description, "version": version}
    except Exception as e:
        return {"name": "Unknown Project", "description": "No description available.", "version": "0.0.0"}

def get_health_status() -> Healthcheck:
    status: str = 'Healthy'
    project_info = get_project_info()
    return Healthcheck(status=status, project_info=project_info)
