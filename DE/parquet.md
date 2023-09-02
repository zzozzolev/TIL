## Concepts
- https://parquet.apache.org/docs/concepts/

## File Format
- https://parquet.apache.org/docs/file-format/
- http://cloudsqale.com/2020/05/29/how-parquet-files-are-written-row-groups-pages-required-memory-and-flush-operations/
- https://towardsdatascience.com/demystifying-the-parquet-file-format-13adb0206705

![storage layout](images/storage%20layout.png)
https://towardsdatascience.com/demystifying-the-parquet-file-format-13adb0206705

- it’s important to note that parquet is often described as a columnar format. However, due to the fact that it stores chunks of columns, a hybrid storage layout is a more precise description.
- A file consists of one or more row groups.

### Row Group
- A row group contains exactly one column chunk per column.
- A single Row Group contains data for all columns for some number of rows.
- The row group is divided into entities that are called "column chunks."

### Column Chunks
- Column chunks contain one or more pages.

## Row groups stats and Page index
- https://blog.cloudera.com/speeding-up-select-queries-with-parquet-page-indexes/

## Metadata
- https://parquet.apache.org/docs/file-format/metadata/

## Encoding
- https://dataninjago.com/2021/12/07/databricks-deep-dive-3-parquet-encoding/