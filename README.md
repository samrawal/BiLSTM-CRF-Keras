* Project Structure
.
├── data
│   └── n2c2
│       ├── clamp
│       ├── interim
│       ├── processed
│       └── raw
├── docs
│   └── resources
├── models
└── src
    ├── data
    ├── model
    │   └── ipynb
    └── utils
        ├── __pycache__
        └── ipynb

16 directories

* TODO
** Gold File Issue
- Some gold file annotations have spaces in between them (see `$PROJ_PATH/.unused/log/n2c2_preprocessing.log`).
- For now, closing those gaps in the gold files (handling in `n2c2-parser`)
- TODO: Figure out long-term fix

