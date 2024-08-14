#!/bin/bash
echo "Stopping model..."
pkill -f "python waitress_model_sd.py"
echo "Model stopped."
