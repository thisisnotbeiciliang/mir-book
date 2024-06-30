# mir-book

This is the README file for _mir-book_ hosted online at https://thisisnotbeiciliang.github.io/mir-book. 

All the text for each chapter of the book lives inside the folders `./audio-models`, `./real-world-examples`, and `./resources` directories. All figures associated to the chapters are stored in and linked from the `./figures` directory. Landing page corresponds to the `intro.md` file. A collection of bibliography from all the chapters exist in the `references.bib` file.

## Configuration

- The table of contents (TOC) defines the order of chapters as they appear in the book.
To change the TOC, please edit the `_toc.yml` file with correct information on filenames and their relative locations in this repository.
Documentation on controlling the TOC structure can be found on the [Jupyter Book website](https://jupyterbook.org/customize/toc.html).
- Same applies for more general configuration using `_config.yml`.
Documentation on configuring book settings can be found on the [Jupyter Book website](https://jupyterbook.org/customize/config.html).

## Deploy

The site is built using the `jupyter-book` command.

### Local build

To build the book and preview your changes locally you can run the following command:
```
jupyter-book build .
```
Now you can open the path provided by jupyter-book as output in your terminal.

### Clean up the recent build

When you test your edits by building the book multiple times, it is better to clean up the last build before generating a new one.
You can either manually delete the `./_build` folder every time, or run this command:
```
jupyter-book clean .
```
More details on this process can be read on the [Jupyter Book's GitHub repository](https://github.com/executablebooks/jupyter-book/blob/master/docs/advanced/advanced.md#clean-your-books-generated-files).

### Check external links in the book

When editing or reviewing this book locally, you can run the Sphinx link checker with Jupyter Book to check if the external links mentioned in the book are valid.
To run the link checker, use the following command:

```
jupyter-book build . --builder linkcheck
```

The link checker checks if the each link resolves and prints the status on your terminal so that you can check and resolve any incorrect links.
Read more about this on the [Jupyter Book's GitHub repository](https://github.com/executablebooks/jupyter-book/blob/master/docs/advanced/advanced.md#check-external-links-in-your-book).

### Host online

Follow [publish your book online](https://jupyterbook.org/en/stable/start/publish.html) with Github Page.