# character-simulator

A simple terminal-based interactive story simulator.

## Usage

```
python main.py clark
```

Type messages to Clark Kent and receive responses. Type `quit` to exit.

## Fetching new characters

Use the `fetch_character.py` script to download character profiles from the
ComicVine API:

```
python fetch_character.py
```

The script requires an API key which should be set in the `COMICVINE_API_KEY`
environment variable before running.
