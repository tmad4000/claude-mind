#!/bin/bash
# Start the Claude Mind dashboard

PORT=8080
URL="http://localhost:$PORT/demos/status_dashboard.html"

# Check if port is in use
if lsof -i :$PORT > /dev/null 2>&1; then
    echo "Port $PORT already in use."
    read -p "Kill existing process and restart? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -f "python3 -m http.server $PORT"
        sleep 1
    else
        echo "Opening existing dashboard..."
        open "$URL"
        exit 0
    fi
fi

echo "Starting dashboard on port $PORT..."
cd "$(dirname "$0")"
python3 -m http.server $PORT &
SERVER_PID=$!
sleep 1

# Check if server started successfully
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
