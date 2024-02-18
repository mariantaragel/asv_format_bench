from .data_format import DataFormat
import pandas as pd
import dask.dataframe as dd

class Json(DataFormat):

    format_name = "JSON Lines"
    filetype = "jsonl"

    complevel: int

    def __init__(self, data_set, compression=None, complevel=None) -> None:
        super().__init__(data_set, compression)
        self.filename = f"test.{self.filetype}"
        self.pathname = f"{self.filename}/*.part"
        self.complevel = complevel

    def save(self):
        self.data_set.to_json(
            self.filename,
            orient="records",
            lines=True,
            index=False,
            compression={"method": self.compression, "level": self.complevel}
        )

    def parallel_save(self):
        dask_df = dd.from_pandas(self.data_set, npartitions=4)
        dd.to_json(dask_df, self.filename, orient="records", lines=True, index=False)

    def read(self):
        pd.read_json(self.filename, lines=True, compression=self.compression)

    def parallel_read(self):
        dd.read_json(self.pathname).compute()