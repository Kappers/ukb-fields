"""
UK Biobank field lookup

Handy for identifying categorical columns, either by helper or directly executable.

Example:
    >>> from ukb_field_lookup import get_ukb_field, get_encoding_values
    >>> get_ukb_field(4)
    {'field_id': 4, 'title': 'Biometrics duration', 'categories': 0, 'description': 'Time taken for participant ...'}
    >>> >>> get_encoding_values(100261)
    [-1, 1, 2, 3, 4]

"""

__author__ = "Thomas Kaplan"

import argparse
import pandas as pd
import pdb
import sys
import tabulate

DATA_FIELD_PROPERTIES_PATH = "schemas/data_field_properties.txt"
ENCODING_DICTIONARIES_PATH = "schemas/encoding_dictionaries.txt"
NOT_ENCODED = "NOT-ENCODED"

ENCODING_VALUES_HIER_INT_PATH = "schemas/values_for_hierarchical_integer_encodings.txt"
ENCODING_VALUES_HIER_STR_PATH = "schemas/values_for_hierarchical_string_encodings.txt"
ENCODING_VALUES_SIMP_INT_PATH = "schemas/values_for_simple_integer_encodings.txt"
ENCODING_VALUES_SIMP_STR_PATH = "schemas/values_for_simple_string_encodings.txt"
ENCODING_VALUES_SIMP_TIME_PATH = "schemas/values_for_simple_date_encodings.txt"
ENCODING_VALUES_SIMP_FLOAT_PATH = "schemas/values_for_simple_time_encodings.txt"
ENCODING_VALUES_SIMP_DATE_PATH = (
    "schemas/values_for_simple_real_(floating-point)_encodings.txt"
)
ENCODING_PATHS = [
    ENCODING_VALUES_HIER_INT_PATH,
    ENCODING_VALUES_HIER_STR_PATH,
    ENCODING_VALUES_SIMP_INT_PATH,
    ENCODING_VALUES_SIMP_STR_PATH,
    ENCODING_VALUES_SIMP_TIME_PATH,
    ENCODING_VALUES_SIMP_FLOAT_PATH,
    ENCODING_VALUES_SIMP_DATE_PATH,
]

VERBOSE = False

OUT_HEADER = ["field_id", "title", "categories", "description"]


def _is_singleton(field_id: int, schema_df: pd.DataFrame) -> bool:
    """Check whether a single record is identified for a field

    :param field_id int: UKB field ID
    :param schema_df pd.DataFrame: Indexed records within the schema
    :returns bool: if a single record is found in the schema
    """
    if schema_df.empty:
        if VERBOSE:
            print(f"No fields found for ID={field_id}")
        return False
    elif schema_df.shape[0] > 1:
        if VERBOSE:
            print(
                f"Multiple fields ({schema_df.shape[0]}) found for the same ID={field_id}"
            )
        return False
    return True


def get_encoding_values(encoding_id: int) -> list:
    """Retrieve values for a given encoded field

    :param encoding_id int: Encoding ID for a UKB field
    :returns list: possible values, empty if encoding ID cannot be reconciled
    """
    for enc_path in ENCODING_PATHS:
        enc_df = pd.read_csv(enc_path, delimiter="\t", encoding="ISO-8859-1")
        if encoding_id in enc_df.encoding_id.values:
            encodings = enc_df[enc_df.encoding_id == encoding_id]
            return encodings.value.values.tolist()
    return []


def get_ukb_field(field_id: int) -> dict:
    """Find metadata associated with the UKB field

    :param field_id int: UKB field ID
    :returns dict: metadata if found, else an empty dict
    """
    data_prop_df = pd.read_csv(DATA_FIELD_PROPERTIES_PATH, delimiter="\t")
    enc_dict_df = pd.read_csv(ENCODING_DICTIONARIES_PATH, delimiter="\t")

    prop_df = data_prop_df[data_prop_df.field_id == field_id]
    if not _is_singleton(field_id, prop_df):
        return {}
    prop = prop_df.iloc[0]

    enc_id = prop.encoding_id
    enc_df = enc_dict_df[enc_dict_df.encoding_id == enc_id]
    if not _is_singleton(field_id, enc_df):
        return {}

    enc = enc_df.iloc[0]
    if enc.title == NOT_ENCODED:
        categs = 0
    else:
        categs = enc.num_members

    pdb.set_trace()

    return dict(zip(OUT_HEADER, [field_id, prop.title, categs, prop.notes]))


def main(args):
    if args.verbose:
        global VERBOSE
        VERBOSE = True

    recs = [get_ukb_field(field_id) for field_id in args.field_ids]
    recs = [r for r in recs if r]

    if args.print:
        if VERBOSE:
            print()
        print(tabulate.tabulate(recs, headers="keys"))
        sys.exit(0)

    out_df = pd.DataFrame(recs, columns=OUT_HEADER)
    print(
        out_df.drop(columns=["description"], axis=1).to_csv(None, sep=";", index=False)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "field_ids", metavar="N", nargs="+", type=int, help="UKB field index"
    )
    parser.add_argument("--print", action="store_true", help="Print in tabulated form")
    parser.add_argument(
        "--verbose", action="store_true", help="Print debugging information"
    )
    args = parser.parse_args()
    main(args)
