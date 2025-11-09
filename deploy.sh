#!/bin/bash

# Attendance Bot - Deployment Script
# Usage: ./deploy.sh [start|stop|restart|logs|status]

set -e

CMD=${1:-start}

case "$CMD" in
    start)
        echo "🚀 Starting Attendance Bot..."
        
        # Check if .env exists
        if [ ! -f .env ]; then
            echo "❌ Error: .env file not found!"
            echo "📝 Please copy .env.example to .env and configure it:"
            echo "   cp .env.example .env"
            echo "   nano .env"
            exit 1
        fi
        
        # Build and start containers
        docker-compose up -d --build
        
        echo "✅ Attendance Bot started!"
        echo "📊 Check logs: ./deploy.sh logs"
        ;;
        
    stop)
        echo "🛑 Stopping Attendance Bot..."
        docker-compose down
        echo "✅ Attendance Bot stopped!"
        ;;
        
    restart)
        echo "🔄 Restarting Attendance Bot..."
        docker-compose down
        docker-compose up -d --build
        echo "✅ Attendance Bot restarted!"
        ;;
        
    logs)
        echo "📋 Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f bot
        ;;
        
    status)
        echo "📊 Attendance Bot Status:"
        docker-compose ps
        ;;
        
    *)
        echo "Usage: $0 {start|stop|restart|logs|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  logs    - Show bot logs"
        echo "  status  - Show container status"
        exit 1
        ;;
esac
