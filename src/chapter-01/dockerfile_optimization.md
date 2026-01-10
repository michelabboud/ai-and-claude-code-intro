# Dockerfile Optimization Examples

## Chapter 1: Introduction to AI - AI-Assisted Code Generation

This document shows how AI can help optimize Dockerfiles.

## Before: Unoptimized Dockerfile

```dockerfile
# Problems with this Dockerfile:
# 1. Uses full Python image (1GB+)
# 2. Installs dev dependencies in production
# 3. No layer caching optimization
# 4. Runs as root (security risk)
# 5. No multi-stage build

FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install pytest black flake8

CMD ["python", "app.py"]
```

## After: AI-Optimized Dockerfile

```dockerfile
# Optimized Dockerfile with:
# 1. Multi-stage build for smaller image
# 2. Alpine base for minimal footprint
# 3. Layer caching optimized
# 4. Non-root user for security
# 5. Only production dependencies

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production
FROM python:3.11-alpine

WORKDIR /app

# Create non-root user
RUN adduser -D appuser

# Copy only what's needed from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser app.py .

# Switch to non-root user
USER appuser

# Set path for user-installed packages
ENV PATH=/home/appuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["python", "app.py"]
```

## Size Comparison

| Image Type | Size |
|------------|------|
| Original (python:3.11) | ~1.1 GB |
| Optimized (python:3.11-alpine) | ~120 MB |
| **Reduction** | **~90%** |

## Security Improvements

1. **Non-root user**: Container runs as unprivileged user
2. **Minimal base image**: Smaller attack surface
3. **No dev tools**: pytest, black, flake8 not in production
4. **No pip cache**: Reduced image size and no cached credentials

## How AI Helped

When asked to optimize the Dockerfile, Claude:
1. Identified all anti-patterns
2. Suggested multi-stage build
3. Recommended Alpine base
4. Added security best practices
5. Optimized layer caching
6. Added health checks

### Example Prompt

```
Optimize this Dockerfile for production:
- Minimize image size
- Improve security
- Optimize build caching
- Follow Docker best practices

[paste Dockerfile]
```

---

**Part of**: AI and Claude Code - A Comprehensive Guide for DevOps Engineers  
**Created by**: Michel Abboud with Claude Sonnet 4.5 (Anthropic)  
**Copyright**: © 2026 Michel Abboud. All rights reserved.  
**License**: CC BY-NC 4.0
