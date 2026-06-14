# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-11
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import numpy as np
import pandas as pd
import pytest
import xarray as xr

import my_code_base.esd.ensemble as ensemble


@pytest.fixture(scope="module")
def dummy_data():
    n_time, n_member = 400, 50
    data = np.random.random(n_member * n_time).reshape((n_time, n_member))
    model_ids = sorted(
        ["ACCESS-CM2", "ACCESS-ESM1", "BCC-CSM2-MR", "BCC-ESM1", "UKESM1-0-LL"] * 10
    )
    member_ids = [f"r{r}i{np.random.randint(1, 3)}p1f1" for r in range(1, 11)] * 5
    combined_ids = [
        f"{model_id}.{member_id}"
        for model_id, member_id in zip(model_ids, member_ids, strict=False)
    ]
    time = pd.date_range("1980-01-01", periods=n_time, freq="1MS")
    data_ = data, combined_ids, time
    return data_


def test__build_member_mapping_table():
    member_values = [
        "ACCESS-CM2.r1i1p1f1",
        "ACCESS-CM2.r2i1p1f1",
        "ACCESS-CM2.r3i1p1f1",
    ]
    member_id_elements = ["model", "run_number"]
    mapping_table = ensemble._build_member_mapping_table(
        member_values, member_id_elements
    )
    assert isinstance(mapping_table, pd.DataFrame)
    assert mapping_table.shape == (3, 2)
    assert mapping_table.index.name == "member"
    assert mapping_table.loc["ACCESS-CM2.r1i1p1f1", "model"] == "ACCESS-CM2"
    assert mapping_table.loc["ACCESS-CM2.r1i1p1f1", "run_number"] == "r1i1p1f1"


def test_ensemble_pandas_accessor(dummy_data):
    data, combined_ids, time = dummy_data
    df = pd.DataFrame(data=data, columns=combined_ids, index=time)
    df.ens.key_template = "source_id.member_id"
    assert isinstance(df.ens.groupby("source_id"), ensemble._ColumnGroupBy)
    assert len(df.ens.groupby("source_id")) == 5, "Shape not fit"
    assert len(df.ens.groupby("member_id")) == 10, "Shape not fit"
    df_avg = df.ens.groupby("source_id").mean()
    assert df_avg.columns.name == "source_id", (
        "column index should be called `source_id`"
    )


def test_ensemble_xarray_accessor(dummy_data):
    data, combined_ids, time = dummy_data
    ds = xr.Dataset(
        {"tas": (["time", "member"], data)},
        coords={
            "time": time,
            "member": combined_ids,
        },
    )
    ds.ens.key_template = "source_id.member_id"
    assert isinstance(ds.ens.groupby("source_id"), xr.core.groupby.DatasetGroupBy)
    assert len(ds.ens.groupby("source_id")) == 5, "Shape not fit"
    assert len(ds.ens.groupby("member_id")) == 10, "Shape not fit"
    ds_avg = ds.ens.groupby("source_id").mean()
    assert "source_id" in ds_avg.coords, "`source_id` not in coordinates"
