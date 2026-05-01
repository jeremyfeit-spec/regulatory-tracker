# Regulatory Tracker

Database of international regulatory and compliance changes that affect a core accounting software provider. **61 countries** across **EMEA, APAC, LATAM, and Canada**, bucketed into the **6 compliance jobs beyond core accounting**:

1. Tax Filing & Returns
2. VAT/GST Compliance
3. E-Invoicing
4. Payroll Tax & Social Contributions
5. Local GAAP & Statutory Reporting
6. Banking & Payments Compliance

## How it runs

A Cowork scheduled task fires **every Friday at 8am Pacific** (`regulatory-tracker-friday-digest`):

1. Reads the current state of `countries/*.json`
2. Uses web search to scan each country and compliance topic for changes published in the last 7 days
3. Writes new/updated entries back to `countries/<ISO>.json` — files stay on disk in this folder
4. Saves the weekly diff to `history/diff_YYYY-MM-DD.json`
5. Posts the digest to Slack `#international_weekly_regulatory_overview` via the Slack MCP

No API keys needed. No GitHub Actions. The whole thing runs through Cowork's connected tools.

## Folder layout

```
regulatory-tracker/
├── README.md
├── countries/           # 61 country JSON files (the live database)
├── config/
│   ├── countries.json   # country list, regions, the 6 compliance jobs
│   └── sources.yaml     # authoritative URLs per country + global feeds
└── history/             # weekly diff snapshots
```

## Country JSON schema

```json
{
  "iso": "GB",
  "name": "United Kingdom",
  "region": "EMEA",
  "currency": "GBP",
  "language": "en",
  "last_synced": "2026-04-30T13:00:00Z",
  "compliance": {
    "tax_filing":       [...],
    "vat_gst":          [...],
    "e_invoicing":      [...],
    "payroll":          [...],
    "local_gaap":       [...],
    "banking_payments": [...]
  }
}
```

Each entry:

```json
{
  "id": "GB-VAT-MTD-2022",
  "title": "Making Tax Digital for VAT",
  "summary": "All VAT-registered businesses must keep digital records...",
  "status": "live",
  "effective_date": "2022-04-01",
  "source": "https://www.gov.uk/...",
  "source_type": "official",
  "first_seen": "2026-04-30T13:00:00Z",
  "last_updated": "2026-04-30T13:00:00Z"
}
```

`status` values: `live` · `upcoming` · `in_progress` · `monitoring` · `repealed`
`source_type` values: `official` · `advisory` · `news` · `web`

## Coverage on the first run

The seed file ships with ~41 known regulations across the major markets (UK MTD, France PDP 2026, Germany ZUGFeRD 2025, Spain Verifactu, Italy SDI, Poland KSeF 2026, India GST e-invoicing, Singapore InvoiceNow, Mexico CFDI 4.0, Brazil NF-e + CBS/IBS reform, Canada CRA + RTR, etc.). The Friday job grows the database from there.

## Pushing to GitHub (optional)

If you want a snapshot in your private GitHub repo, push the folder by hand whenever:

```bash
cd ~/Documents/regulatory-tracker
git init
git add .
git commit -m "snapshot $(date -u +%Y-%m-%d)"
git remote add origin https://github.com/jeremyfeit-spec/regulatory-tracker.git
git push -u origin main
```
