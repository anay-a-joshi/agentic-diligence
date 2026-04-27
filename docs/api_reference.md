# API Reference

## POST /analyze/{ticker}
Triggers the multi-agent pipeline.
**Response:** `AnalysisResult` (see `app/models/analysis.py`)

## POST /chat
Conversational Q&A over cached filings.
**Body:** `{ticker, message}`
**Response:** `{response, citations[]}`

## GET /export/pdf/{ticker}
Returns the generated IC memo PDF.

## GET /export/xlsx/{ticker}
Returns the LBO Excel model.
