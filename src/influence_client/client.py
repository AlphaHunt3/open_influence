"""Small async REST client. No automatic retries or data fan-out."""
from __future__ import annotations

import os
import re
from urllib.parse import quote, urlsplit

import httpx


class InfluenceError(Exception):
    """A safe API error with machine-readable status and retry guidance."""
    def __init__(self, code: str, message: str, status: int | None = None,
                 retry_after: str | None = None):
        self.code, self.status, self.retry_after = code, status, retry_after
        super().__init__(message)

    def as_dict(self):
        return {"error": {"code": self.code, "message": str(self),
                          "status": self.status, "retry_after": self.retry_after}}


def choice(value, allowed, field):
    if value not in allowed:
        raise InfluenceError("invalid_parameter", f"{field} must be one of: {', '.join(allowed)}", 422)
    return value


def count(value, maximum=100):
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise InfluenceError("invalid_parameter", f"limit must be an integer from 1 to {maximum}", 422)
    return value


def identifier(value, square=False):
    value = value.strip() if isinstance(value, str) else ""
    if not square:
        value = value.removeprefix("@")
    pattern = r"[A-Za-z0-9_-]{1,128}" if square else r"[A-Za-z0-9_]{1,15}"
    if not re.fullmatch(pattern, value):
        raise InfluenceError("invalid_parameter", "Invalid Square UID" if square else "Use an X handle of 1–15 letters, numbers or underscores", 422)
    return quote(value, safe="")


class InfluenceClient:
    """Use as ``async with InfluenceClient() as client``.

    Responses keep all service fields; ``_client`` adds the actual charged
    credits (None when the service omits the billing header).
    """
    def __init__(self, api_key: str | None = None, base_url: str | None = None,
                 timeout: float = 30):
        self._key = (api_key if api_key is not None else os.getenv("XHUNT_API_KEY", "")).strip()
        base = (base_url or os.getenv("XHUNT_BASE_URL", "https://mcp.xhunt.ai")).rstrip("/")
        parsed = urlsplit(base)
        if (parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username
                or parsed.password or parsed.query or parsed.fragment or parsed.path not in ("", "/")):
            raise InfluenceError("invalid_configuration", "XHUNT_BASE_URL must be an HTTP(S) origin without credentials, path or query")
        if parsed.scheme == "http" and parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
            raise InfluenceError("invalid_configuration", "Use HTTPS except for localhost development")
        self._http = httpx.AsyncClient(base_url=base, timeout=timeout, follow_redirects=False,
                                      headers={"User-Agent": "influence-client/0.1.0", "Accept": "application/json"})

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.aclose()

    async def aclose(self):
        await self._http.aclose()

    async def _get(self, path, params=None, public=False):
        if not public and not self._key:
            raise InfluenceError("missing_api_key", "Set XHUNT_API_KEY. Create a personal key at https://mcp.xhunt.ai/account", 401)
        try:
            response = await self._http.get(path, params=params,
                headers={} if public else {"X-API-Key": self._key})
        except httpx.TimeoutException:
            raise InfluenceError("timeout", "Request timed out; no automatic retry was made. A timed-out data request may already have consumed credits.") from None
        except httpx.HTTPError:
            raise InfluenceError("connection_error", "Unable to reach the configured Influence service") from None
        try:
            payload = response.json()
        except ValueError:
            raise InfluenceError("invalid_response", "Service returned a non-JSON response", response.status_code) from None
        if not response.is_success:
            error = payload.get("error", {}) if isinstance(payload, dict) else {}
            code = error.get("code", "http_error") if isinstance(error, dict) else "http_error"
            hints = {401: "Check your personal API key at /account.",
                     429: "Inspect the error code: quota_exceeded needs more credits or a UTC reset; rate_limited needs a pause. No automatic retry was made.",
                     422: "Check sector, region, identifiers and limit.",
                     404: "No matching published record or endpoint was found."}
            # Never echo raw provider responses, request URLs or keys.
            raise InfluenceError(code, hints.get(response.status_code, "Influence service request failed"),
                                 response.status_code, response.headers.get("retry-after"))
        if not isinstance(payload, dict):
            raise InfluenceError("invalid_response", "Expected a JSON object", response.status_code)
        charged = response.headers.get("x-credits-charged", "")
        return {**payload, "_client": {"credits_charged": int(charged) if charged.isdigit() else None}}

    async def capabilities(self):
        """Public metadata, no key or credits needed."""
        return await self._get("/capabilities.json", public=True)

    async def usage(self):
        """Authenticated daily/monthly usage. Zero credits in auth-billing version."""
        return await self._get("/api/v1/usage")

    async def x_leaderboard(self, sector="web3", region="global", limit=10, kind="influence"):
        choice(kind, ("influence", "weekly_growth"), "kind")
        path = "/leaderboards/influence" if kind == "influence" else "/leaderboards/weekly-growth"
        return await self._get("/api/v1" + path, {"sector": choice(sector, ("ai", "web3"), "sector"),
            "region": choice(region, ("global", "en", "cn"), "region"), "limit": count(limit)})

    async def pro_leaderboard(self, platform="x", sector="web3", region="global", limit=10):
        choice(platform, ("x", "binance-square", "youtube"), "platform")
        choice(sector, ("ai", "web3"), "sector")
        choice(region, ("global", "en", "cn"), "region")
        if platform != "x" and region != "global":
            raise InfluenceError("invalid_parameter", "Pro regional pools apply only to X", 422)
        return await self._get(f"/api/v1/pro/leaderboards/{platform}",
                               {"sector": sector, "region": region, "limit": count(limit, 500)})

    async def x_profile(self, handle):
        return await self._get(f"/api/v1/kols/{identifier(handle)}")

    async def x_ranks(self, handle):
        return await self._get(f"/api/v1/kols/{identifier(handle)}/ranks")

    async def x_smart_followers(self, handle, sector="web3", limit=None):
        return await self._get(f"/api/v1/kols/{identifier(handle)}/smart-followers",
                               {"sector": choice(sector, ("ai", "web3"), "sector"), **({"limit": count(limit)} if limit is not None else {})})

    async def x_circle(self, handle, days=7, limit=None):
        if isinstance(days, bool) or not isinstance(days, int) or not 1 <= days <= 30:
            raise InfluenceError("invalid_parameter", "days must be an integer from 1 to 30", 422)
        return await self._get(f"/api/v1/kols/{identifier(handle)}/circle", {"days": days, **({"limit": count(limit)} if limit is not None else {})})

    async def x_social(self, handle, limit=None):
        return await self._get(f"/api/v1/kols/{identifier(handle)}/social", ({"limit": count(limit)} if limit is not None else {}))

    async def x_profile_history(self, handle, limit=None):
        return await self._get(f"/api/v1/kols/{identifier(handle)}/profile-history", {"limit": count(limit)} if limit is not None else {})

    async def x_abilities(self, handle, sector="web3", limit=None):
        return await self._get(f"/api/v1/kols/{identifier(handle)}/abilities", {"sector": choice(sector, ("ai", "web3"), "sector"), **({"limit": count(limit)} if limit is not None else {})})

    async def x_weekly(self, sector="web3", region="cn", limit=None, mode="attention"):
        choice(mode, ("attention", "new_entries"), "mode")
        choice(sector, ("ai", "web3"), "sector")
        choice(region, ("global", "en", "cn"), "region")
        if mode == "attention" and (sector != "web3" or region == "global"):
            raise InfluenceError("unsupported_combination", "attention only supports Web3 cn/en; use new_entries or weekly_growth for other pools", 422)
        return await self._get("/api/v1/weekly/kols", {"sector": sector, "region": region, "mode": mode, **({"limit": count(limit)} if limit is not None else {})})

    async def square_leaderboard(self, limit=10):
        return await self._get("/api/v1/binance-square/leaderboard", {"limit": count(limit)})

    async def square_profile(self, square_uid):
        return await self._get(f"/api/v1/binance-square/kols/{identifier(square_uid, True)}")

    async def square_abilities(self, square_uid):
        return await self._get(f"/api/v1/binance-square/kols/{identifier(square_uid, True)}/abilities")

    async def square_weekly(self, limit=None, metric="followers", region="global"):
        result = await self._get("/api/v1/binance-square/weekly/trending", {
            **({"limit": count(limit)} if limit is not None else {}), "metric": choice(metric, ("followers", "smart_followers"), "metric"),
            "region": choice(region, ("global", "en", "cn"), "region")})
        no_history = result.get("status") in ("insufficient_history", "stale_data") and result.get("items") == []
        if region != "global" and (result.get("meta") or {}).get("region") != region and not no_history:
            raise InfluenceError("unsupported_region", "Server did not confirm Square language filtering. Check capabilities.weekly_regions before requesting a language-specific list.")
        return result

    async def hot(self, kind="hot-kols", sector="web3", region="cn", limit=None):
        choice(kind, ("hot-kols", "hot-tweets", "rising-tweets"), "kind")
        choice(sector, ("ai", "web3"), "sector")
        choice(region, ("cn", "en"), "region")
        if kind == "rising-tweets" and sector != "web3":
            raise InfluenceError("unsupported_combination", "Rising tweets cover Web3 only", 422)
        return await self._get("/api/v1/trending/" + kind, {"sector": sector, "region": region,
                               **({"limit": count(limit)} if limit is not None else {})})

    async def youtube_leaderboard(self, sector="web3", limit=10):
        return await self._get("/api/v1/youtube/leaderboard", {
            "sector": choice(sector, ("ai", "web3"), "sector"), "limit": count(limit)})
