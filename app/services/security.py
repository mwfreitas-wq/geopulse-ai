"""Proteções de segurança: limite de requisições por IP, cabeçalhos HTTP, validação de imagens e fila de auditorias."""
import asyncio
import time
from collections import defaultdict, deque
from typing import Deque, Dict

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings

_hits: Dict[str, Deque[float]] = defaultdict(deque)


def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit(name: str, limit_getter, window_seconds: int = 3600):
    """Dependência FastAPI: bloqueia o IP com HTTP 429 ao passar do limite na janela de tempo."""
    async def _dep(request: Request):
        limit = limit_getter() if callable(limit_getter) else int(limit_getter)
        if limit <= 0:
            return
        key = f"{name}:{client_ip(request)}"
        now = time.time()
        q = _hits[key]
        while q and now - q[0] > window_seconds:
            q.popleft()
        if len(q) >= limit:
            wait_min = max(1, int((window_seconds - (now - q[0])) / 60))
            raise HTTPException(
                status_code=429,
                detail=f"Limite de consultas atingido. Tente novamente em ~{wait_min} min ou fale com nosso atendimento."
            )
        q.append(now)
    return _dep


# Fila de auditorias: só N rodam ao mesmo tempo, as demais aguardam sua vez (protege o servidor e os custos de API)
_audit_semaphore = None


def audit_slot() -> asyncio.Semaphore:
    global _audit_semaphore
    if _audit_semaphore is None:
        _audit_semaphore = asyncio.Semaphore(max(1, settings.MAX_CONCURRENT_AUDITS))
    return _audit_semaphore


def detect_image_ext(data: bytes):
    """Valida a imagem pelos bytes reais (não confia no cabeçalho enviado pelo cliente)."""
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    return None


CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdn.tailwindcss.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "img-src 'self' data: blob: https:; "
    "media-src 'self' data: blob: https: http:; "
    "connect-src 'self'; "
    "frame-ancestors 'self'; base-uri 'self'; form-action 'self' https://www.mercadopago.com.br https://api.whatsapp.com"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.headers.setdefault("Content-Security-Policy", CSP)
        if settings.SITE_URL.startswith("https://"):
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        return response
