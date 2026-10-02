# Python CLI Todo App

A small command-line todo application built with Python. Todos are stored locally in a JSON file.

## Features

- Add todos
- List todos
- Mark todos as complete
- Delete todos
- Persistent JSON storage
- `argparse` CLI
- Python type hints
- Graceful error handling

## Requirements

- Python 3.9+

No third-party packages are required.

## Usage

### Add a todo

```bash
python todo_cli.py add "Finish DevForge task"
```

### List todos

```bash
python todo_cli.py list
```

Example:

```text
[ ] 1: Finish DevForge task
[✓] 2: Read Python documentation
```

### Complete a todo

```bash
python todo_cli.py complete 1
```

### Delete a todo

```bash
python todo_cli.py delete 2
```

### Use a custom JSON file

```bash
python todo_cli.py --file my_tasks.json add "Build API"
python todo_cli.py --file my_tasks.json list
```

## Project structure

```text
todo-cli/
├── todo_cli.py
├── README.md
├── .gitignore
└── LICENSE
```

## Data format

The application creates `todos.json` automatically:

```json
[
  {
    "id": 1,
    "title": "Finish DevForge task",
    "completed": false
  }
]
```

## Error handling

The application reports invalid todo IDs, malformed JSON, missing files, file access errors, and empty todo titles without crashing with a traceback.

## License

MIT
