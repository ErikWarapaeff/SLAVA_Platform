# Reproducibility

The active analytics source is `ErikWarapaeff/SLAVA_Platform` on `main`. The
released benchmark data is maintained separately as
`RANEPA-ai/SLAVA-OpenData-2800-v1` on Hugging Face. Record that exact dataset
revision, file checksums, the code commit, dependency lock, model identity, and
scoring configuration for every result.

This repository has no versioned result manifest or registered S3 release
location yet. Until one is added, generated spreadsheets, model responses,
MongoDB contents, and figures are working artifacts rather than a
reproducible release. Keep bulk artifacts outside Git and publish only links,
checksums, provenance, and compact evidence allowed by the source licenses.

Run the deterministic CPU-only validation without MongoDB, Streamlit, network
access, or model calls:

```bash
poetry install --no-root
PYTHONPATH=. poetry run pytest -q
```
