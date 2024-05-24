#!/bin/bash

MAC_PATH="/Users/malpern/Documents/Programming/MacroPad/zz-MACROPAD-DESKTOP"
MICROCONTROLLER_PATH="/Volumes/MACROPAD"
LOG_FILE="${MAC_PATH}/script/logfile.log"

# Print status update
echo "Starting sync from $MAC_PATH to $MICROCONTROLLER_PATH..." | tee -a "$LOG_FILE"

# Function to perform rsync with retries
sync_files() {
    local RETRY_COUNT=5
    local RETRY_DELAY=10

    # Check if paths exist
    if [ ! -d "$MAC_PATH" ]; then
        echo "Source path $MAC_PATH does not exist." | tee -a "$LOG_FILE"
        return 1
    fi

    if [ ! -d "$MICROCONTROLLER_PATH" ]; then
        echo "Destination path $MICROCONTROLLER_PATH does not exist." | tee -a "$LOG_FILE"
        return 1
    fi

    for ((i=1; i<=RETRY_COUNT; i++)); do
        # Sync files to the microcontroller and log output
        rsync -avz --delete \
        --exclude='.*' \
        --exclude='watch_and_sync.sh' \
        --exclude='*.log' \
        "$MAC_PATH/" "$MICROCONTROLLER_PATH/" | tee -a "$LOG_FILE"
        if [ $? -eq 0 ]; then
            echo "Sync successful." | tee -a "$LOG_FILE"
            return 0
        fi
        echo "Sync failed. Attempt $i of $RETRY_COUNT. Retrying in $RETRY_DELAY seconds..." | tee -a "$LOG_FILE"
        sleep $RETRY_DELAY
    done

    echo "Sync failed after $RETRY_COUNT attempts." | tee -a "$LOG_FILE"
    return 1
}

# Perform the sync
sync_files
sync_files