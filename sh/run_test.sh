python -m app.setup
pytest test/ --cov=app \
             --cov=settings \
             --cov-report=xml:/app/reports/xml \
             --cov-report=html:/app/reports/html
