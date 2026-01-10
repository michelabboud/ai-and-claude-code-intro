#!/bin/bash
# Auto-grader for incident-01-crashloop

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         🔍 CHECKING SOLUTION: CRASHLOOP INCIDENT         ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

SCORE=0
ISSUES=0

# Check if containers are running
echo "1️⃣  Checking if containers are running..."
if docker-compose ps | grep -q "Up"; then
    if docker-compose ps app | grep -q "Up"; then
        echo "   ✅ App container is running"
        SCORE=$((SCORE + 10))
    else
        echo "   ❌ App container is not running"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "   ❌ Containers not started. Run: docker-compose up -d"
    exit 1
fi

echo ""
echo "2️⃣  Checking application endpoints..."

# Wait a bit for app to be ready
sleep 3

# Test root endpoint
if curl -s http://localhost:5000/ | grep -q "Hello"; then
    echo "   ✅ Root endpoint (/) works"
    SCORE=$((SCORE + 5))
else
    echo "   ❌ Root endpoint (/) failed"
    ISSUES=$((ISSUES + 1))
fi

# Test health endpoint
if curl -s http://localhost:5000/health | grep -q "healthy"; then
    echo "   ✅ Health endpoint (/health) works"
    SCORE=$((SCORE + 5))
else
    echo "   ❌ Health endpoint (/health) failed"
    ISSUES=$((ISSUES + 1))
fi

# Test data endpoint
if curl -s http://localhost:5000/data | grep -q "PostgreSQL"; then
    echo "   ✅ Data endpoint (/data) works"
    SCORE=$((SCORE + 5))
else
    echo "   ❌ Data endpoint (/data) failed"
    ISSUES=$((ISSUES + 1))
fi

echo ""
echo "3️⃣  Checking database connection..."

# Check if database is accessible from app
if docker-compose exec -T app python -c "import psycopg2; psycopg2.connect('$DATABASE_URL'); print('OK')" 2>/dev/null | grep -q "OK"; then
    echo "   ✅ Database connection verified"
    SCORE=$((SCORE + 5))
else
    echo "   ⚠️  Database connection check skipped (container issue)"
fi

echo ""
echo "4️⃣  Stability check (60 second uptime)..."
echo "   ⏳ Waiting 60 seconds..."

sleep 60

if docker-compose ps app | grep -q "Up"; then
    echo "   ✅ App remained stable for 60 seconds"
    SCORE=$((SCORE + 10))
else
    echo "   ❌ App crashed during stability check"
    ISSUES=$((ISSUES + 1))
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo " 📊 RESULTS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Issues Found: $ISSUES"
echo "  Base Score: $SCORE / 40"
echo ""

if [ "$ISSUES" -eq 0 ]; then
    echo "  ✅ SUCCESS! All checks passed!"
    echo ""
    echo "  🏆 Final Score: $SCORE points"
    echo ""
    echo "  Next steps:"
    echo "  1. Review what you fixed"
    echo "  2. Update progress tracker:"
    echo "     cd ../../progress-tracker"
    echo "     python tracker.py complete-sandbox incident-01-crashloop"
    echo ""
else
    echo "  ⚠️  INCOMPLETE: $ISSUES issue(s) remaining"
    echo ""
    echo "  Hints available:"
    echo "    ./hints.sh 1"
    echo "    ./hints.sh 2"
    echo "    ./hints.sh 3"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════"
echo ""
