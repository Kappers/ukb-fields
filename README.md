# `ukb-fields`

Simple Python utilities to look up UK Biobank fields, e.g. text description and categorical values.

Refer to [https://biobank.ndph.ox.ac.uk/ukb/list.cgi](https://biobank.ndph.ox.ac.uk/ukb/list.cgi)

### Requirements

- (mini)conda, tested with v24.3.0)
- Python, tested with v3.10.14)


### Quick-start

```bash
# Create a conda environment
> conda env create -f environment.yml
> conda activate ukb-fields

# Run script directly, by default it prints a CSV
>  python ukb_field_lookup.py 4-0.3
field_id;title;dtype;categories;encoding_id
4;Biometrics duration;INT;0;0

> python ukb_field_lookup.py 4 5-1.0 --print
  field_id  title                         categories  description
----------  --------------------------  ------------  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
         4  Biometrics duration                    0  Time taken for participant to do the tests in the biometric station of the Assessment Centre visit.
         5  Sample collection duration             0  Time taken for participant to complete the blood phlebotomy station of the Assessment Centre visit. This is longer than the time during which they were actively giving blood.


# Or make use of helper functions
> python
>>> from ukb_field_lookup import get_ukb_field, get_encoding_values
>>> get_ukb_field(4)
    {'field_id': 4, 'title': 'Biometrics duration', 'dtype': 'INT', 'categories': 0, 'description': 'Time taken for participant ...'}
>>> >>> get_encoding_values(100261)
    [-1, 1, 2, 3, 4]
```


--

Contact: `t.kaplan AT qmul.ac.uk`
