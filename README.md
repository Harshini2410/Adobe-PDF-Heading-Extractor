# Adobe PDF Heading Extractor

This project extracts structured headings (H1, H2, H3) from `.pdf` documents using Python and PyMuPDF.  
It is containerized using Docker, following Adobe's constraints:

- Processes all PDFs inside `/app/input/`
- Outputs structured `.json` to `/app/output/`
- Runs without network access

---

## Folder Structure

```
.
├── extractor.py          # Main Python script
├── requirements.txt      # Dependencies
├── Dockerfile            # Docker container setup
├── input/                # Put your PDFs here
│   └── sample.pdf
├── output/               # JSON files appear here
│   └── sample.json
```

---

## Build the Docker Image

```bash
docker build --platform=linux/amd64 -t adobe-solution:harshi123 .
```

---

## Run the Extractor

```bash
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" --network none adobe-solution:harshi123
```

- On **Windows CMD**, use `%cd%` instead of `${PWD}`
- On **macOS/Linux**, `${PWD}` works fine

---

## Input

Place all `.pdf` files you want to process into the `/input` folder.

---

## Output

Each PDF is converted into a `.json` file in `/output/`, e.g.:

```json
{
  "title": "Abstract:",
  "outline": [
    { "level": "H1", "text": "Abstract:", "page": 2 },
    { "level": "H1", "text": "Existing System:", "page": 5 }
    // ...
  ]
}
```

---

## Constraints Met

- No external network usage (`--network none`)
- Input/output handled via volume mounts only
- Lightweight base image (`python:3.10-slim`)
- Batch processes all `.pdf` files in `/input/`

---

## Authors

- [Harshini Nadendla](https://github.com/Harshini2410)
- [Spurthi Inturu](https://github.com/Spurthi7904)
- [Chakrish Vejendla](https://github.com/Vejandlachakrish)


---

## Acknowledgements

This project was developed as part of **Adobe's Hackathon Challenge – Round 1A**.

