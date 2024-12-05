from tars.scheduler import Scheduler
from tars.common import TASKTYPE

# Create a scheduler
scheduler = Scheduler()

# Add stages
scheduler.add_stage(TASKTYPE.DATA_GENERATION, "LayerNorm")
scheduler.add_stage(TASKTYPE.GOLDEN, "LayerNorm")
scheduler.add_stage(TASKTYPE.KERNEL, "LayerNorm")

# Submit tasks
future_inputs = scheduler.submit_task(TASKTYPE.DATA_GENERATION, "LayerNorm", batch_size=4, feature_size=128)
future_inputs.add_done_callback(lambda fut: scheduler.submit_task(TASKTYPE.GOLDEN, "LayerNorm", fut.result()))
future_inputs.add_done_callback(lambda fut: scheduler.submit_task(TASKTYPE.KERNEL, "LayerNorm", fut.result()))

# Run the workflow
scheduler.wait_for_all()

# Retrieve results
golden_output = scheduler.get_results(TASKTYPE.GOLDEN, "LayerNorm")
kernel_output = scheduler.get_results(TASKTYPE.KERNEL, "LayerNorm")

# Print outputs
print("Golden Output:", golden_output)
print("Kernel Output:", kernel_output)
