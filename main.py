import os
import sqlite3

# -------------------------------
# Generator imports (ORDER MATTERS)
# -------------------------------

from generators.organizations import generate_organization
from generators.users import generate_users
from generators.teams import generate_teams_and_memberships
from generators.team_memberships import generate_team_memberships
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.subtasks import generate_subtasks
from generators.comments import generate_comments
from generators.custom_fields import generate_custom_field_definitions
from generators.custom_field_values import generate_custom_field_values
from generators.tags import generate_tags
from generators.task_tags import generate_task_tags

# -------------------------------
# Paths
# -------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "output", "asana_simulation.sqlite")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


# -------------------------------
# Initialize database
# -------------------------------

def init_database():
    """
    Creates a fresh SQLite database using schema.sql
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.close()


# -------------------------------
# Main pipeline
# -------------------------------

def main():
    print("🚀 Initializing Asana simulation database...")
    init_database()

    print("🏢 Creating organization (Salesforce)...")
    org_id = generate_organization(DB_PATH)

    print("👥 Generating users...")
    generate_users(
        db_path=DB_PATH,
        org_id=org_id,
        domain="salesforce.com",
        n_users=5000
    )

    print("👥 Creating teams & initial memberships...")
    generate_teams_and_memberships(
        db_path=DB_PATH,
        org_id=org_id
    )

    print("🔁 Refining team memberships (non-uniform)...")
    generate_team_memberships(DB_PATH)

    print("📁 Creating projects...")
    generate_projects(DB_PATH)

    print("📌 Creating sections per project...")
    generate_sections(DB_PATH)

    print("📝 Creating tasks...")
    generate_tasks(DB_PATH)

    print("🧩 Creating subtasks...")
    generate_subtasks(DB_PATH)

    print("💬 Creating comments & stories...")
    generate_comments(DB_PATH)

    print("🏷️ Creating custom field definitions...")
    generate_custom_field_definitions(DB_PATH)

    print("📊 Assigning custom field values...")
    generate_custom_field_values(DB_PATH)

    print("🔖 Creating tags...")
    generate_tags(DB_PATH)

    print("🔗 Linking tags to tasks...")
    generate_task_tags(DB_PATH)

    print("✅ Asana simulation database created successfully!")
    print(f"📦 Database location: {DB_PATH}")


# -------------------------------
# Entry point
# -------------------------------

if __name__ == "__main__":
    main()
