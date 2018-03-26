# fulcrum_reconciliation
Simple flask app that tracks the reconciliation process on Fulcrum. Reconciliation allows users to update status of responses to invalid on Fulcrum's website, so that bad data isn't paid for.

This only reconciles survey's that have `'callout'` in their name (case doesn't matter). This is because the good ids list that is constructed is only made from callout reports. Any other surveys need to be reconciled manually

### Run Steps

1. Run the app using the `run_app_script.py` file. This will start a local flask web app at port 5000, at http://127.0.0.1:5000

2. Navigate to the udpate all surveys route, at http://127.0.0.1:5000/survey_management/update_all_surveys. This will update all of the surveys based on information from Fulcrum, allowing the reconcilliation of the correct surveys later 

3. Navigate to the route for configuring the previous month's ids, at http://127.0.0.1:5000/survey_management/configure_previous_month_ids. This creates an id file from the surveys from the previous month

4. Navigate to the route that reconciles the surveys, at http://127.0.0.1:5000/survey_management/reconcile_surveys. This will add the current months good ids to the ids file, and then reconcile all of the callout surveys that haven't been reconciled yet.

### Errors that could arise

The biggest one is reconciling a survey that didn't have it's good ids added to the good id list. If a survey doesn't have a data check file, but has callout in it's name and is complete but not reconciled, then it is going to get reconciled by the program and have every complete removed.
