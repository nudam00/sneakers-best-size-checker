# Sneakers Best Size Checker

> [!WARNING]
> **Legacy project**
>
> This project was built in 2022 as a personal tool for identifying sneaker
> sizes that met a configurable resale-margin threshold. It is no longer
> maintained and is preserved as a record of an early automation project.
>
> Marketplace APIs, pages, authentication flows, and anti-bot protections have
> changed since it was released. The application is therefore unlikely to work
> without updates.
>
> This is a preserved historical snapshot, not an example of how I build
> software today. The code predates my current engineering standards and lacks
> tests, CI/CD, pre-commit checks, type checking, task automation, and modern
> separation of concerns. It is kept public to document the original product
> idea and my development path—not as a recommended implementation.

Companion project: [Sneakers Price Checker](https://github.com/nudam00/sneakers-price-checker)

## Project context

The tool combined browser automation and HTTP requests with marketplace-specific
adapters, currency and fee calculations, sneaker-size conversion, and Excel
reporting. Given a list of products and their acquisition costs, it checked
StockX and Alias and reported the sizes whose estimated proceeds exceeded the
configured margin.

The repository remains public for historical context.

## Original workflow

1. Add SKUs, net acquisition prices, and optional product IDs to
   `input/sneakers.xlsx`.
2. Copy `input/settings.example.json` to `input/settings.json` and fill in the
   account, fee, margin, and exchange-rate values. The legacy Alias adapter also
   expects third-party client values listed in `.env.example`.
3. Run `python main.py` and complete any interactive marketplace login or
   anti-bot checks.
4. Review qualifying EU sizes in `output/sizes.xlsx`.

`input/settings.json` is ignored by Git because it contains account credentials.
Do not commit a populated copy.

## Components

- `main.py` orchestrates spreadsheet input, marketplace checks, size conversion,
  and report generation.
- `sites/stockx.py` uses Playwright to inspect StockX listings.
- `sites/alias.py` uses HTTP requests to query Alias/GOAT endpoints.
- `converters/sizes.json` maps US sizes to EU sizes by brand.
- `add.py` loads settings and performs size lookups.

## Historical setup

The dependency list is provided for reference and is intentionally unpinned
because the versions used by the original project were not recorded:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
playwright install firefox
cp input/settings.example.json input/settings.json
cp .env.example .env
python main.py
```

These steps document the original shape of the project; they are not a guarantee
that current marketplace integrations will function.

## Known limitations

- Selectors and undocumented endpoints are brittle and now likely outdated.
- Authentication is interactive and may require manual anti-bot challenges.
- Error handling and retry loops are basic and can hide failures.
- The code has no automated tests, CI/CD, pre-commit checks, or type checking.
- `DataFrame.append`, used by the project, was removed in pandas 2.0.
- Sample spreadsheets contain historical product data and are not a stable API.

## Status

Archived in spirit: no support, fixes, or compatibility updates are planned.
