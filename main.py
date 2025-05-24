# daily_log.py
from colorama import init, Fore, Style
from datetime import datetime
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create a daily log in Markdown format.")
    parser.add_argument(
        "-f", "--file",
        default="daily_log.md",
        help="Path to the Markdown log file (default: daily_log.md)"
    )
    args = parser.parse_args()
    md_filepath = args.file

    # Initialize colorama for cross-platform colored output
    init()  # Autoreset can be used, but here we manually reset after each print
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

    # Create a timestamp for the entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Build Markdown content lines
    md_lines = [f"# 🗓️ **Daily Log - {timestamp}**\n"]
    non_empty_sections = [
        header for header in section_headers if user_entries.get(header)
    ]
    for header in non_empty_sections:
        md_lines.append(f"### {header}")
        for point in user_entries[header]:
            md_lines.append(f"- {point}")
        md_lines.append("")  # Blank line after section

    # Only write if at least one section is non-empty
    if non_empty_sections:
        with open(md_filepath, "a", encoding="utf-8") as f:
            f.write("\n".join(md_lines) + "\n")
        print(Fore.GREEN + f"Your entry has been added to {md_filepath}!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "No entries provided. Nothing was added to the log file." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
