# HTTPX Async Transport Pytest Issue

This repo serves demonstrate the following bug:
- custom transport is not called when used in conjunction with Async Client

# Installation

```
pip install -r requirements.txt
```

# Run

```
python main.py
```

# Run tests

They will fail because of the bug, but they should not

```
pytest test_main.py
```