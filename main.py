# daily_log.py
from colorama import init, Fore, Style
from datetime import datetime
import argparse
import os
from log_writers import LocalLogWriter, JoplinLogWriter

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create a daily log in Markdown format.")
    parser.add_argument(
        "-f", "--file",
        default="daily_log.md",
        help="Path to the Markdown log file (default: daily_log.md)"
    )
    parser.add_argument(
        "-j", "--joplin",
        action="store_true",
        help="Also append the log as a note in Joplin (requires joppy and JOPLIN_API_KEY env variable)"
    )
    parser.add_argument(
        "-n", "--note-id",
        default=None,
        help="Joplin note ID to append the log to (used only with --joplin)"
    )
    args = parser.parse_args()
    md_filepath = args.file
    use_joplin = args.joplin
    note_id = args.note_id

    # Initialize colorama for cross-platform colored output
    init()
    print("Enter your daily log entries. Type each point one per line.")
    print("Press Enter on an empty line to finish a section.\n")

    section_headers = [
        "✨ What I Did (Highlights)",
        "📚 Key Learnings",
        "🚀 Next Steps (Tomorrow)",
        "🚧 Blockers / Challenges",
        "🔗 Links / References",
        "😊 Mood / Reflection"
    ]

    user_entries = {}
    for header in section_headers:
        print(Fore.CYAN + header + ":" + Style.RESET_ALL)
        section_points = []
        while True:
            line = input("- ")
            if not line.strip():
                break
            section_points.append(line.strip())
        user_entries[header] = section_points
        print()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    md_lines = [f"## 🗓️ Daily Log - {timestamp}\n"]
    non_empty_sections = [
        header for header in section_headers if user_entries.get(header)
    ]
    for header in non_empty_sections:
        md_lines.append(f"**{header}**")
        if header == "🚀 Next Steps (Tomorrow)":
            for point in user_entries[header]:
                md_lines.append(f"- [ ] {point}")
        else:
            for point in user_entries[header]:
                md_lines.append(f"- {point}")
        md_lines.append("")  # Blank line after section

    log_content = "\n".join(md_lines) + "\n"

    if non_empty_sections:
        try:
            if use_joplin:
                writer = JoplinLogWriter(note_id=note_id)
            else:
                writer = LocalLogWriter(md_filepath)
            writer.write(log_content, timestamp)
        except Exception as e:
            print(Fore.RED + f"Failed to write log: {e}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "No entries provided. Nothing was added to the log file." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
