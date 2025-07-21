"""Command line interface for the interactive story simulator."""
import argparse
from pathlib import Path
from datetime import datetime

from parser import parse_input
from responder import load_character, generate_response
from memory import load_memory, save_memory, update_memory


def start_conversation(character_name: str) -> None:
    """Run a terminal conversation loop with the specified character."""
    char_path = Path("characters") / f"{character_name}.json"
    if not char_path.exists():
        print(f"Character profile '{character_name}' not found.")
        return

    character = load_character(char_path)
    memory = load_memory(character_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path("logs") / f"conversation_{character_name}_{timestamp}.txt"
    log_path.parent.mkdir(exist_ok=True)

    print(f"Starting conversation with {character.get('name', character_name)}. Type 'quit' to exit.")
    with log_path.open("w", encoding="utf-8") as log_file:
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() in {"quit", "exit"}:
                break
            parsed = parse_input(user_input)
            update_memory(memory, parsed)
            response = generate_response(character, parsed, memory)
            print(response)
            log_file.write(f"You: {user_input}\n")
            log_file.write(f"{character_name.title()}: {response}\n")
            log_file.flush()

    save_memory(character_name, memory)
    print("Conversation ended.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive character simulator")
    parser.add_argument("character", help="Name of the character JSON (without extension)")
    args = parser.parse_args()
    start_conversation(args.character)


if __name__ == "__main__":
    main()
