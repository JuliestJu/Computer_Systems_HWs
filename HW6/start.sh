
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

echo "Starting Docker Compose..."
docker-compose up --build

if [ $? -eq 0 ]; then
    echo "Docker Compose started successfully."
else
    echo "Failed to start Docker Compose."
    exit 1
fi
