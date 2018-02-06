from classes import AutoReconciler
import os
import dotenv

# Load in any environment variables
env_path = os.path.join(os.getcwd(), '.env')
dotenv.load_dotenv(env_path)

# Set authorization key value for request headers
API_KEY = os.environ.get('FULCRUM_PRODUCTION_API_KEY')

auto_reconciler = AutoReconciler(API_KEY, 'production')
auto_reconciler.list_completed_surveys()
auto_reconciler.good_ids_list = auto_reconciler.configure_good_ids_list()

auto_reconciler.reconcile_completed_surveys()

print('Finished')
