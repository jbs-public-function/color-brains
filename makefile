FEATURE_ENGINEERING_SCRIPT_PATH := color_brains/data_enrichment/rgb_feature_enrichment_flow.py
RUN_MODEL_SCRIPT_PATH := color_brains/model/rgb_model_flow.py

run-feature-flow:
    # run feature flow
	python $(FEATURE_ENGINEERING_SCRIPT_PATH) run

run-model:
	# run model
	python $(RUN_MODEL_SCRIPT_PATH) run

view-results:
	# view results card
	python $(RUN_MODEL_SCRIPT_PATH) card view model_results --id results

view-outputs:
	# view results card
	python $(RUN_MODEL_SCRIPT_PATH) card view visualize_outputs --id visualize_outputs

run-tests:
	# run tests
	pytest
