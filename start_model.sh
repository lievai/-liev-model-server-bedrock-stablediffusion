#!/bin/bash
echo "Starting model..."
nohup python waitress_model_sd.py > ./logs/waitress_model_sd.log 2>&1 &
echo "Model started."
