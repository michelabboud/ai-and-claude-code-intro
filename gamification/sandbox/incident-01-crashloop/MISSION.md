# 🚨 Incident 01: CrashLoopBackOff

**Difficulty**: ⭐⭐ Apprentice
**Points**: 25
**Estimated Time**: 15-20 minutes

---

## 📋 Incident Report

```
PRIORITY: P2 (High)
STATUS: Ongoing
AFFECTED: Production API service
ERROR: CrashLoopBackOff in Kubernetes

Timeline:
- 14:32: Deployment succeeded
- 14:33: Pods start failing
- 14:34: All 3 replicas in CrashLoopBackOff
- 14:35: YOU are assigned to fix this
```

---

## 🎯 Mission

A Python Flask API was just deployed to Kubernetes. All pods are crashing immediately with `CrashLoopBackOff`.

**Your task**: Diagnose and fix the issue so the application runs successfully.

---

## 🏗️ Architecture

- **App**: Simple Flask API (Python 3.11)
- **Endpoints**:
  - `GET /` - Hello world
  - `GET /health` - Health check
  - `GET /data` - Fetch from database
- **Database**: PostgreSQL
- **Deployment**: Docker + Kubernetes manifests

---

## 🚀 Getting Started

```bash
# Start the broken environment
docker-compose up -d

# Check logs (you'll see crashes)
docker-compose logs app

# The app container will keep restarting
# Your job: figure out WHY and fix it!
```

---

## 🔍 Symptoms

- App container starts
- Crashes within seconds
- Restart loop continues
- Kubernetes would show: CrashLoopBackOff

---

## ✅ Success Criteria

- App starts successfully
- All endpoints respond correctly
- Health check returns 200 OK
- Database connection works
- No crashes for 60 seconds

```bash
# Test your fix
./check-solution.sh
```

---

## 💡 Hints Available

Need help? Use the hint system:

```bash
./hints.sh 1  # High-level hint (-5 pts)
./hints.sh 2  # Specific area hint (-5 pts)
./hints.sh 3  # Detailed hint (-5 pts)
```

---

## 🎓 Learning Objectives

- Reading container logs
- Debugging CrashLoopBackOff
- Environment variable configuration
- Database connection troubleshooting
- Docker and Kubernetes basics

---

## 🏆 Scoring

- **Base**: 25 points
- **Speed bonus**: <10 min → +10 pts
- **No hints**: +15 pts
- **Hint penalty**: -5 pts each

---

Ready to debug? The clock starts when you run `docker-compose up -d`! ⏱️
