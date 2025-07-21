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
environment variable before running. For convenience, you can export the
provided key like so:

```bash
export COMICVINE_API_KEY=18486013de316536659c6d7150a5fe84347ce2a8
```

This key will allow the fetch script to communicate with ComicVine. Keep in
mind that storing API keys in plaintext is not secure; consider using a more
secure secret management method for real projects.

## Setup

The parser relies on the spaCy NLP library. Install it and the English model:

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

After installation, you can run the simulator and parsing will work properly.
