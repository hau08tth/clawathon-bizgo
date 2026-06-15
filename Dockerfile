# ── Stage 1: Build Next.js frontend ──────────────────────────────────────────
FROM node:20-alpine AS frontend-deps
WORKDIR /app
COPY frontend/package.json ./
RUN npm install --legacy-peer-deps --force

FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY --from=frontend-deps /app/node_modules ./node_modules
COPY frontend/ .
# Empty → browser uses relative URLs → nginx routes /auth /gamification etc. to backend
ENV NEXT_PUBLIC_API_URL=""
RUN npm run build

# ── Stage 2: Combined runtime ─────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# System deps: nginx + supervisor + Node.js 20 + build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc libpq-dev nginx supervisor curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Backend Python deps
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Backend source
COPY backend/ /app/backend/

# Frontend standalone output
COPY --from=frontend-builder /app/.next/standalone /app/frontend/
COPY --from=frontend-builder /app/.next/static /app/frontend/.next/static
COPY --from=frontend-builder /app/public /app/frontend/public

# nginx: remove default site, add bizgro config
RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/conf.d/default.conf
COPY nginx/nginx.prod.conf /etc/nginx/conf.d/bizgro.conf

# supervisord config
COPY supervisord.conf /app/supervisord.conf

EXPOSE 8080

CMD ["/usr/bin/supervisord", "-n", "-c", "/app/supervisord.conf"]
