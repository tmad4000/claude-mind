#!/bin/bash
# Start the Claude Mind dashboard

cd "$(dirname "$0")"

# Find an available port starting from 8080
PORT=8080
while lsof -i :$PORT > /dev/null 2>&1; do
    echo "Port $PORT in use, trying next..."
    ((PORT++))
    if [ $PORT -gt 8099 ]; then
        echo "No available ports found (tried 8080-8099)"
        exit 1
    fi
done

URL="http://localhost:$PORT/demos/status_dashboard.html"

echo "Starting dashboard on port $PORT..."
python3 -m http.server $PORT &
SERVER_PID=$!
sleep 1

if kill -0 $SERVER_PID 2>/dev/null; then
    echo ""
    echo "Dashboard ready at: $URL"
    echo ""
    open "$URL"
    echo "Press Ctrl+C to stop"
    wait $SERVER_PID
else
    echo "Failed to start server"
    exit 1
fi
