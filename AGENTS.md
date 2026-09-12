# Repository instructions

This repository contains analytics code for the released SLAVA benchmark; it
does not own a production deployment. Read `catalog-info.yaml`,
`docs/reproducibility.md`, and the dataset release metadata before changing a
metric or interpreting a result.

- Keep dataset versions, question classes, answer schemas, model revisions,
  and scorer versions explicit. Do not combine results produced under
  different contracts.
- The Hugging Face dataset release is the data source of truth. Do not commit
  copied datasets, model outputs, credentials, personal data, or bulk reports.
- Treat the Streamlit and MongoDB files as local research utilities. Do not
  infer a production environment or GitOps binding from them.
- Run `poetry run pytest -q` after changes. Merge-request tests must remain
  deterministic, CPU-only, and offline.
- Deliver changes through a reviewed branch and pull request.
