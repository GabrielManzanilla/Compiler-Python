def evaluate_operation(operation):
		operation_type = type(operation)
		result = INSTATNCES[operation_type](operation)
		return result
