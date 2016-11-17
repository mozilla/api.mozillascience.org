#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scienceapi.settings")

    from django.core.management import execute_from_command_line

    args = sys.argv

    execute_from_command_line(args)

    if args[1] == "makemigrations":
        print("Generating database schema diagram as `db_schema.png`")
        execute_from_command_line([
            "./manage.py",
            "graph_models",
            "users",
            "projects",
            "events",
            "resources",
            "study_groups",
            "-o",
            "db_schema.png"
        ])
