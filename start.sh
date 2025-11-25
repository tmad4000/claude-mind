#!/bin/bash
# Start the Claude Mind dashboard

echo "Starting dashboard..."
python3 -m http.server 8080 &
sleep 1
echo ""
echo "Dashboard ready at: http://localhost:8080/demos/status_dashboard.html"
echo ""
echo "Press Ctrl+C to stop"
open "http://localhost:8080/demos/status_dashboard.html"
wait
