#!/bin/bash
cd /home/kavia/workspace/code-generation/taskflow-114435-f90b217a/react_js_frontend_workspace/react_js_frontend
npm run build
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
   exit 1
fi

