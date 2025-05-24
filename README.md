# 📝 daily_log_creator

A helper Python script to aid daily logging in markdown format.

## 🚀 Usage

Run the script:

```bash
uv run main.py
```

By default, logs are appended to `daily_log.md` in the current directory.

### 📄 Specify a custom log file

You can specify a different markdown file using the `-f` or `--file` option:

```bash
uv run main.py --file path/to/your_log.md
```

or

```bash
uv run main.py -f my_daily_log.md
```

### ℹ️ How it works

- The script will prompt you for each section of your daily log.
- Enter each point one per line. Press Enter on an empty line to finish a section.
- If all sections are left empty, nothing is written to the log file.
- The log is appended in a markdown format with emoji section headers.

---
