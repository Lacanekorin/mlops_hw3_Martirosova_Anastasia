#!/bin/bash

# Blue-Green Deployment Switch Script
# This script helps switch traffic between blue (v1.0.0) and green (v1.1.0) versions

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./switch-version.sh [blue|green]"
    echo "Current configuration:"
    grep -A 2 "# Blue version" nginx.conf
    exit 1
fi

case "$VERSION" in
    blue)
        echo "Switching to BLUE version (v1.0.0)..."
        sed -i.bak 's/# server ml-service-blue:8080;/server ml-service-blue:8080;/' nginx.conf
        sed -i.bak 's/server ml-service-green:8080;/# server ml-service-green:8080;/' nginx.conf
        ;;
    green)
        echo "Switching to GREEN version (v1.1.0)..."
        sed -i.bak 's/server ml-service-blue:8080;/# server ml-service-blue:8080;/' nginx.conf
        sed -i.bak 's/# server ml-service-green:8080;/server ml-service-green:8080;/' nginx.conf
        ;;
    *)
        echo "Error: Invalid version. Use 'blue' or 'green'"
        exit 1
        ;;
esac

echo "Reloading Nginx configuration..."
docker-compose exec nginx nginx -s reload

echo "Version switched to $VERSION successfully!"
echo ""
echo "Verify the switch:"
echo "curl http://localhost/health"
