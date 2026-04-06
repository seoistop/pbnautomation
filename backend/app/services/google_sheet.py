from __future__ import annotations

import json
from typing import Iterable

import gspread
from google.oauth2.service_account import Credentials

from ..config import get_settings


def _get_client():
    settings = get_settings()
    if not settings.GOOGLE_SERVICE_ACCOUNT_JSON:
        raise RuntimeError("Google service account JSON missing")
    info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    credentials = Credentials.from_service_account_info(info, scopes=scopes)
    return gspread.authorize(credentials)


def fetch_sites_from_sheet() -> Iterable[dict[str, str]]:
    settings = get_settings()
    if not settings.GOOGLE_SHEET_ID:
        raise RuntimeError("GOOGLE_SHEET_ID not configured")
    client = _get_client()
    sheet = client.open_by_key(settings.GOOGLE_SHEET_ID).sheet1
    records = sheet.get_all_records()
    for row in records:
        yield {
            "name": row.get("name") or row.get("domain"),
            "domain": row.get("domain"),
            "username": row.get("user") or row.get("username"),
            "app_password": row.get("pass") or row.get("password"),
            "ux_block_id": row.get("post_id") or row.get("ux_block_id"),
        }
