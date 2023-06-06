## Concepts
- https://parquet.apache.org/docs/concepts/

## File Format
- https://parquet.apache.org/docs/file-format/
- http://cloudsqale.com/2020/05/29/how-parquet-files-are-written-row-groups-pages-required-memory-and-flush-operations/
- A file consists of one or more row groups.
- A row group contains exactly one column chunk per column.
- A single Row Group contains data for all columns for some number of rows.
- Column chunks contain one or more pages.
