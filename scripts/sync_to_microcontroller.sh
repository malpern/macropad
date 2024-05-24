#!/bin/bash

MAC_PATH="/Users/malpern/Documents/Programming/MacroPad/zz-MACROPAD-DESKTOP"
MICROCONTROLLER_PATH="/Volumes/MACROPAD"
LOG_FILE="${MAC_PATH}/scripts/logfile.log"
LOGGING_ENABLED=false  # Set logging to off by default

# Print status update
log() {
    if [ "$LOGGING_ENABLED" = true ]; then
        echo "$1" | tee -a "$LOG_FILE"
    else
        echo "$1"
    fi
}

log "Starting sync from $MAC_PATH to $MICROCONTROLLER_PATH..."

# Function to perform rsync with retries
sync_files() {
    local RETRY_COUNT=5
    local RETRY_DELAY=10

    # Check if paths exist
    if [ ! -d "$MAC_PATH" ]; then
        log "Source path $MAC_PATH does not exist."
        return 1
    fi

    if [ ! -d "$MICROCONTROLLER_PATH" ]; then
        log "Destination path $MICROCONTROLLER_PATH does not exist."
        return 1
    fi

    for ((i=1; i<=RETRY_COUNT; i++)); do
        # Sync files to the microcontroller and log output
        rsync -avz --delete \
        --size-only \
        --exclude='.*' \
        --exclude='watch_and_sync.sh' \
        --exclude='*.log' \
        "$MAC_PATH/" "$MICROCONTROLLER_PATH/" | tee -a "$LOG_FILE"
        if [ $? -eq 0 ]; then
            log "Sync successful."
            return 0
        fi
        log "Sync failed. Attempt $i of $RETRY_COUNT. Retrying in $RETRY_DELAY seconds..."
        sleep $RETRY_DELAY
    done

    log "Sync failed after $RETRY_COUNT attempts."
    return 1
}

# Perform the sync
sync_files
