FEATURE_ENGINEERING_SCRIPT_PATH := color_brains/data_enrichment/rgb_feature_enrichment_flow.py
RUN_MODEL_SCRIPT_PATH := color_brains/model/rgb_model_flow.py

run-feature-flow:
    # run feature flow
	python $(FEATURE_ENGINEERING_SCRIPT_PATH) run

run-model:
	# run model
	python $(RUN_MODEL_SCRIPT_PATH) run