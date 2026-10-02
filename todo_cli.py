#!/usr/bin/env python3
"""A small command-line todo application."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_FILE = Path("todos.json")


def load_todos(file_path: Path) -> list[dict[str, Any]]:
    """Load todos from JSON, returning an empty list if the file is missing."""
    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not read {file_path}: {exc}") from exc

    if not isinstance(data, list):
        raise RuntimeError(f"{file_path} does not contain a valid todo list.")

    return data


def save_todos(file_path: Path, todos: list[dict[str, Any]]) -> None:
    """Save todos to JSON."""
    try:
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(todos, file, indent=2)
            file.write("\n")
    except OSError as exc:
        raise RuntimeError(f"Could not save {file_path}: {exc}") from exc


def next_id(todos: list[dict[str, Any]]) -> int:
    """Return the next available integer ID."""
    return max((int(todo["id"]) for todo in todos), default=0) + 1


def add_todo(file_path: Path, title: str) -> None:
    todos = load_todos(file_path)
    todo = {
        "id": next_id(todos),
        "title": title.strip(),
        "completed": False,
    }
    todos.append(todo)
    save_todos(file_path, todos)
    print(f"Added todo #{todo['id']}: {todo['title']}")


def list_todos(file_path: Path) -> None:
    todos = load_todos(file_path)

    if not todos:
        print("No todos found.")
        return

    for todo in todos:
        status = "✓" if todo.get("completed", False) else " "
        print(f"[{status}] {todo['id']}: {todo['title']}")


def complete_todo(file_path: Path, todo_id: int) -> None:
    todos = load_todos(file_path)

    for todo in todos:
        if int(todo["id"]) == todo_id:
            if todo.get("completed", False):
                print(f"Todo #{todo_id} is already complete.")
                return

            todo["completed"] = True
            save_todos(file_path, todos)
            print(f"Completed todo #{todo_id}: {todo['title']}")
            return

    raise ValueError(f"Todo #{todo_id} was not found.")


def delete_todo(file_path: Path, todo_id: int) -> None:
    todos = load_todos(file_path)

    for index, todo in enumerate(todos):
        if int(todo["id"]) == todo_id:
            removed = todos.pop(index)
            save_todos(file_path, todos)
            print(f"Deleted todo #{todo_id}: {removed['title']}")
            return

    raise ValueError(f"Todo #{todo_id} was not found.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A simple command-line todo application."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_FILE,
        help="Path to the JSON storage file (default: todos.json).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new todo.")
    add_parser.add_argument("title", help="Todo title.")

    subparsers.add_parser("list", help="List all todos.")

    complete_parser = subparsers.add_parser(
        "complete", help="Mark a todo as completed."
    )
    complete_parser.add_argument("id", type=int, help="Todo ID.")

    delete_parser = subparsers.add_parser("delete", help="Delete a todo.")
    delete_parser.add_argument("id", type=int, help="Todo ID.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "add":
            if not args.title.strip():
                parser.error("Todo title cannot be empty.")
            add_todo(args.file, args.title)

        elif args.command == "list":
            list_todos(args.file)

        elif args.command == "complete":
            complete_todo(args.file, args.id)

        elif args.command == "delete":
            delete_todo(args.file, args.id)

        return 0

    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
