#!/bin/bash

# Define the list of websites
websites=("https://google.com" "https://facebook.com" "https://twitter.com" "https://x.com")

# Define the log file name
log_file="website_status.log"

# Clear the log file
> $log_file

# Check each website
for site in "${websites[@]}"; do
  # Send an HTTP GET request and get the status code
  status_code=$(curl -o /dev/null -s -w "%{http_code}" "$site")
  
  # Check if the status code is 200
  if [ "$status_code" -eq 200 ]; then
    echo "$site is UP (Status Code: $status_code)" | tee -a $log_file
  else
    echo "$site is DOWN (Status Code: $status_code)" | tee -a $log_file
  fi
done

# Display the message about log file creation
echo "Results have been logged to $log_file"
