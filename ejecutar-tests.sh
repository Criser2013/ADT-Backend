pytest --html=./tests/resultados/run-$(date +%Y-%m-%d_%H-%M-%S)/reporte.html \
 --cov=./app --cov-report=html:./tests/cobertura/cobertura-$(date +%Y-%m-%d_%H-%M-%S)