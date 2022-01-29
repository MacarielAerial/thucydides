echo "Testing..."
pytest --cov-report xml:cov.xml --junitxml=test_report.xml
