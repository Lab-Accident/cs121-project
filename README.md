When starting MySQL, make sure you do --local-infile=1 to allow for data loading.

We recommend using the generated data we have provided. data-gen.py occasionally generates small errors (i.e., uncommon duplicates) that are qwick manual fixes.

# Data Sources

Our book data is sourced from [this Goodreads Kaggle dataset](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks). A semi-cleaned form of this dataset with some fields removed is `uncleaned_books.csv`, which we use in `data-gen.py` to generate the `.csv`s we load in `load-data.sql`.

We recommend using the generated data we have provided instead of generating new data with the script. `data-gen.py` occasionally generates small errors (i.e., infrequent duplicates). These are quick to manually fix, but there's no reason to do that given working files.

# Database Set-Up

To set up the database, first connect to your MySQL instance. Ensure that you include the `--local-infile=1` flag to ensure that file loading is enabled. Now, run these commands in order:

1. `source setup.sql;`
2. `source load-data.sql;`
3. `source setup-passwords.sql;`
4. `source setup-routines.sql;`
5. `source grant-permissions.sql;`

To test some queries, run:

- `source queries.sql`

# Application

To run the application, `quit` MySQL and run `python3 app.py` in your terminal.

The application prompts will lead you through.
