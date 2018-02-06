from fulcrum_reconciliation.create_app import create_app
from fulcrum_reconciliation.config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run()
