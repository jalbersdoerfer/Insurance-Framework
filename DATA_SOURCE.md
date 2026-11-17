# Data Source

## Period life table Germany (Destatis)

| Item | Value |
|---|---|
| Publisher | Statistisches Bundesamt (Destatis), Wiesbaden |
| Database | GENESIS-Online |
| Table | 12621-0001 – *Sterbetafel (Periodensterbetafel): Deutschland, Jahre, Geschlecht, Vollendetes Alter* |
| Table URL | https://genesis.destatis.de/datenbank/online/statistic/12621/table/12621-0001 |
| Period | 2023/2025 (three-year period life table) |
| Published | 7 July 2026 (Statistischer Bericht „Sterbetafeln 2023/2025“) |
| Coverage | Germany as a whole, male and female, completed ages 0–100 |
| Raw file | `12621-0001_de.csv` (not included in this repository) |

## How to obtain the raw data

The raw data is not stored in this repository. To reproduce it:

1. Open the GENESIS table URL above.
2. Under *Jahre (Zeitraum)* select **only 2023/25**.
3. Under *Geschlecht* select *männlich* and *weiblich*; select all *Vollendetes Alter* values.
4. Select the content `Sterbewahrscheinlichkeit [q(x)]`.
5. Use *Download* and choose the **CSV** format (German locale, `;` separator, decimal comma).
6. Save the file as `data/raw/12621-0001_de.csv`.

## Processing

Script: `transform_mortality_data.py`

```bash
python build_sterbetafel.py --input data/raw/12621-0001_de.csv \
    --output data/processed/sterbetafel.csv
```

What the script does:

- Reads data rows only; title, header, legend and footer rows are ignored.
- Takes the age from column 1, q(x) male from column 2 and q(x) female from column 16. Every value in the GENESIS export is followed by a flag column, hence the gaps.
- Converts decimal commas to points and writes a comma-separated CSV.
- Validates the result: no missing probabilities, no duplicate ages, all ages are present, all q(x) within [0, 1].

### Output: `mortality_table.csv`

| Column | Meaning |
|---|---|
| `age` | Completed age x in years (0–100) |
| `qx_male` | Probability that a man aged exactly x dies before reaching age x+1 |
| `qx_female` | Same for women |

Definition (Destatis): q(x) = Sterbewahrscheinlichkeit vom Alter x bis x+1.

## Notes

- This is a **period** life table: a snapshot of mortality in 2023–2025, not a projection and not a cohort table. It makes no assumption about future mortality.
- The table ends at age 100. Whether q(100) describes exactly age 100 or an open-ended interval is not stated.
- The age labels refer to completed years of age.
